import os
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.files.storage import default_storage, Storage, FileSystemStorage
from django.utils.datastructures import SortedDict
from django.utils.functional import empty, memoize, LazyObject
from django.utils.module_loading import import_by_path
from django.utils.importlib import import_module
from django.utils._os import safe_join
from django.utils import six

from django.contrib.staticfiles import utils
from django.contrib.staticfiles.storage import AppStaticStorage
from django.contrib.staticfiles.finders import BaseFinder
_finders = SortedDict()

class FileSystemFinder(BaseFinder):
    """
    A static files finder that uses the ``STATICFILES_DIRS`` setting
    to locate files.
    """
    def __init__(self, apps=None, *args, **kwargs):
        # List of locations with static files
        self.locations = []
        # Maps dir paths to an appropriate storage instance
        self.storages = SortedDict()
        if not isinstance(settings.STATICFILES_DIRS, (list, tuple)):
            raise ImproperlyConfigured(
                "Your STATICFILES_DIRS setting is not a tuple or list; "
                "perhaps you forgot a trailing comma?")
        for root in settings.STATICFILES_DIRS:
            if isinstance(root, (list, tuple)):
                prefix, root = root
            else:
                prefix = ''
            if settings.STATIC_ROOT and os.path.abspath(settings.STATIC_ROOT) == os.path.abspath(root):
                raise ImproperlyConfigured(
                    "The STATICFILES_DIRS setting should "
                    "not contain the STATIC_ROOT setting")
            if (prefix, root) not in self.locations:
                self.locations.append((prefix, root))
        for prefix, root in self.locations:
            filesystem_storage = FileSystemStorage(location=root)
            filesystem_storage.prefix = prefix
            self.storages[root] = filesystem_storage
        super(FileSystemFinder, self).__init__(*args, **kwargs)

    def find(self, path, all=False):
        """
        Looks for files in the extra locations
        as defined in ``STATICFILES_DIRS``.
        """
        matches = []
        brand = settings.BRAND
        mod = import_module('gladminds.{0}'.format(brand))
        custom_root = os.path.join(os.path.dirname(mod.__file__), 'static')
        for prefix, root in self.locations:
            matched_path = self.find_location(root, custom_root, path, prefix)
            if matched_path:
                if not all:
                    return matched_path
                matches.append(matched_path)
        return matches

    def find_location(self, root, custom_root, path, prefix=None):
        """
        Finds a requested static file in a location, returning the found
        absolute path (or ``None`` if no match).
        """
        if prefix:
            prefix = '%s%s' % (prefix, os.sep)
            if not path.startswith(prefix):
                return None
            path = path[len(prefix):]

        custom_path = safe_join(custom_root, path)
        if os.path.exists(custom_path):
            return custom_path

        path = safe_join(root, path)
        if os.path.exists(path):
            return path

    def list(self, ignore_patterns):
        """
        List all files in all locations.
        """
        for prefix, root in self.locations:
            storage = self.storages[root]
            for path in utils.get_files(storage, ignore_patterns):
                yield path, storage


class AppDirectoriesFinder(BaseFinder):
    """
    A static files finder that looks in the directory of each app as
    specified in the source_dir attribute of the given storage class.
    """
    storage_class = AppStaticStorage

    def __init__(self, apps=None, *args, **kwargs):
        # The list of apps that are handled
        self.apps = []
        # Mapping of app module paths to storage instances
        self.storages = SortedDict()
        if apps is None:
            apps = settings.INSTALLED_APPS
        for app in apps:
            app_storage = self.storage_class(app)
            if os.path.isdir(app_storage.location):
                self.storages[app] = app_storage
                if app not in self.apps:
                    self.apps.append(app)
        super(AppDirectoriesFinder, self).__init__(*args, **kwargs)

    def list(self, ignore_patterns):
        """
        List all files in all app storages.
        """
        for storage in six.itervalues(self.storages):
            if storage.exists(''):  # check if storage location exists
                for path in utils.get_files(storage, ignore_patterns):
                    yield path, storage

    def find(self, path, all=False):
        """
        Looks for files in the app directories.
        """
        matches = []
        for app in self.apps:
            match = self.find_in_app(app, path)
            if match:
                if not all:
                    return match
                matches.append(match)
        return matches

    def find_in_app(self, app, path):
        """
        Find a requested static file in an app's static locations.
        """
        storage = self.storages.get(app, None)
        if storage:
            if storage.prefix:
                prefix = '%s%s' % (storage.prefix, os.sep)
                if not path.startswith(prefix):
                    return None
                path = path[len(prefix):]
            # only try to find a file if the source dir actually exists
            if storage.exists(path):
                matched_path = storage.path(path)
                if matched_path:
                    return matched_path


class BaseStorageFinder(BaseFinder):
    """
    A base static files finder to be used to extended
    with an own storage class.
    """
    storage = None

    def __init__(self, storage=None, *args, **kwargs):
        if storage is not None:
            self.storage = storage
        if self.storage is None:
            raise ImproperlyConfigured("The staticfiles storage finder %r "
                                       "doesn't have a storage class "
                                       "assigned." % self.__class__)
        # Make sure we have an storage instance here.
        if not isinstance(self.storage, (Storage, LazyObject)):
            self.storage = self.storage()
        super(BaseStorageFinder, self).__init__(*args, **kwargs)

    def find(self, path, all=False):
        """
        Looks for files in the default file storage, if it's local.
        """
        try:
            self.storage.path('')
        except NotImplementedError:
            pass
        else:
            if self.storage.exists(path):
                match = self.storage.path(path)
                if all:
                    match = [match]
                return match
        return []

    def list(self, ignore_patterns):
        """
        List all files of the storage.
        """
        for path in utils.get_files(self.storage, ignore_patterns):
            yield path, self.storage


class DefaultStorageFinder(BaseStorageFinder):
    """
    A static files finder that uses the default storage backend.
    """
    storage = default_storage

    def __init__(self, *args, **kwargs):
        super(DefaultStorageFinder, self).__init__(*args, **kwargs)
        base_location = getattr(self.storage, 'base_location', empty)
        if not base_location:
            raise ImproperlyConfigured("The storage backend of the "
                                       "staticfiles finder %r doesn't have "
                                       "a valid location." % self.__class__)


def find(path, all=False):
    """
    Find a static file with the given path using all enabled finders.

    If ``all`` is ``False`` (default), return the first matching
    absolute path (or ``None`` if no match). Otherwise return a list.
    """
    matches = []
    for finder in get_finders():
        result = finder.find(path, all=all)
        if not all and result:
            return result
        if not isinstance(result, (list, tuple)):
            result = [result]
        matches.extend(result)
    if matches:
        return matches
    # No match.
    return [] if all else None


def get_finders():
    for finder_path in settings.STATICFILES_FINDERS:
        yield get_finder(finder_path)


def _get_finder(import_path):
    """
    Imports the staticfiles finder class described by import_path, where
    import_path is the full Python path to the class.
    """
    Finder = import_by_path(import_path)
    if not issubclass(Finder, BaseFinder):
        raise ImproperlyConfigured('Finder "%s" is not a subclass of "%s"' %
                                   (Finder, BaseFinder))
    return Finder()
get_finder = memoize(_get_finder, _finders, 1)

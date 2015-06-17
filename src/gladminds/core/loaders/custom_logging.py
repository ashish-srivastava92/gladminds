from logging import FileHandler, StreamHandler
import os
from django.conf import settings
import logging
try:
    import codecs
except ImportError:
    codecs = None

_BRAND = 'brand'


class CustomFileHandler(FileHandler):
    """
    A handler class which writes formatted logging records to disk files.
    """
    def __init__(self, filename, mode='a', encoding=None, delay=0):
        """
        Open the specified file and use it as the stream for logging.
        """
        self.stream_cache = {}
        self.filename = filename
        filename = '{0}/{1}'.format(settings.LOG_BASE_PATH, filename)
        super(CustomFileHandler, self).__init__(filename, mode=mode,
                                                encoding=encoding, delay=delay)

    def emit(self, record):
        """
        Emit a record.

        If the stream was not opened because 'delay' was specified in the
        constructor, open it before calling the superclass's emit.
        """
        brand = settings.BRAND
        if brand is None:
            brand = getattr(record, _BRAND)
        key = brand + self.baseFilename
        if self.stream_cache.get(key) is None:
            self.stream_cache[key] = self._open_file(brand)
        self.stream = self.stream_cache[key]
        if hasattr(record, _BRAND) is None:
            record.__dict__[_BRAND] = 'BACKGROUND-JOB'
        StreamHandler.emit(self, record)

    def _open_file(self, brand):
        """
        Open the current base file with the (original) mode and encoding.
        Return the resulting stream.
        """
        filepath = self.baseFilename
        if brand is not None:
            path = '{0}/{1}/{2}'.format(settings.LOG_BASE_PATH,
                                               brand, self.filename)
            if not os.path.exists(path):
                try:
                    os.makedirs('/'.join(path.split('/')[:-1]))
                except:
                    pass
                open(path, 'w').close()

            filepath = os.path.abspath(path)
        if self.encoding is None:
            stream = open(filepath, self.mode)
        else:
            stream = codecs.open(filepath, self.mode, self.encoding)
        return stream


class CustomFilter(logging.Filter):
    def filter(self, record):
        if not hasattr(record.__dict__, _BRAND):
            record.__dict__[_BRAND] = settings.BRAND or None
        return True

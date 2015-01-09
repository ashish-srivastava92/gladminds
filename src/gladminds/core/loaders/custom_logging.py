from logging import FileHandler, StreamHandler
import os
from django.conf import settings
try:
    import codecs
except ImportError:
    codecs = None


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
        key = settings.BRAND + self.baseFilename
        if self.stream_cache.get(key) is None:
            self.stream_cache[key] = self._open()
        self.stream = self.stream_cache[key]
        StreamHandler.emit(self, record)

    def _open(self):
        """
        Open the current base file with the (original) mode and encoding.
        Return the resulting stream.
        """
        filepath = self.baseFilename
        if settings.BRAND is not None:
            path = '{0}/{1}/{2}'.format(settings.LOG_BASE_PATH,
                                               settings.BRAND, self.filename)
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

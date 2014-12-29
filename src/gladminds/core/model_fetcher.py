from importlib import import_module
from django.conf import settings


class ModelFetcher(object):
    """
    The global config wrapper that handles the backend.
    """
    def __init__(self):
        super(ModelFetcher, self).__init__()

    def __getattr__(self, key):
        return getattr(import_module('gladminds.{0}.models'.format(settings.BRAND)), key)

models = ModelFetcher()
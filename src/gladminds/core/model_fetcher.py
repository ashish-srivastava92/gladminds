from importlib import import_module
from django.conf import settings


class ModelFetcher(object):
    """
    The global config wrapper that handles the backend.
    """
    def __init__(self, model_name=None):
        self.model_name = model_name

    def __getattr__(self, key):
        if key in ['objects']:
            return getattr(import_module('gladminds.{0}.models'.format(settings.BRAND)), self.model_name).objects

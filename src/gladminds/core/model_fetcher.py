from importlib import import_module
from django.conf import settings


class ModelFetcher(object):
    """
    The global config wrapper that handles the backend.
    """
    def __init__(self, brand=None):
        super(ModelFetcher, self).__init__()
        self.brand = brand

    def __getattr__(self, key):
        if self.brand is None:
            brand = settings.BRAND
        try:
            return getattr(import_module('gladminds.{0}.models'.format(brand)), key)
        except Exception as e:
            return getattr(import_module('gladminds.core.models'), key)

models = ModelFetcher()
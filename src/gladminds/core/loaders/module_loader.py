from importlib import import_module
from django.conf import settings


def get_models():
    try:
        return import_module('gladminds.{0}.models'.format(settings.BRAND))
    except:
        #this should return a junk model
        return None


def get_model(model, brand=None):
    if not brand:
        brand = settings.BRAND
    try:
        return getattr(import_module('gladminds.{0}.models'.format(brand)), model)
    except:
        return None
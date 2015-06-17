from django.core.cache import cache
from django.conf import settings

class Cache():
    @staticmethod
    def get(key, brand=None):
        if brand is None:
            brand = settings.BRAND
        return cache.get('{0}-{1}-{2}'.format(settings.ENV, brand, key))
    
    @staticmethod
    def set(key, result, timeout=15, brand=None):
        if brand is None:
            brand = settings.BRAND
        return cache.set('{0}-{1}-{2}'.format(settings.ENV, brand, key), result, timeout*60)
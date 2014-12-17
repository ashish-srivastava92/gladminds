'''
this file contains logic for handling services enabled by brands .
'''

from django.conf import settings
import logging


from gladminds.default.models import BrandService
from gladminds.core.exceptions import ServiceNotActiveException

logger = logging.getLogger('gladminds')


class Services():
    '''
    List of all services.....
    '''
    FREE_SERVICE_COUPON = 'free_service_coupon'
    SERVICE_DESK = 'service_desk'
    LOYALTY = 'loyalty'
    AFTERBUY = 'afterbuy'


class ServiceHandler(object):

    def check_service_enabled(self, service_name, brand=None):
        if not brand:
            brand = settings.BRAND
        brand_service_data = BrandService.objects.filter(service__name=service_name, brand__name=brand,
                                                               active=True)
        if len(brand_service_data)>0:
            return True

        return False


def check_service_active(service_name):
    '''
    Checks that service is enabled depending on the url passed
    :param service_name:
    :type string:
    '''
    def check_service_wrapper(func_to_decorate):
        def wrapper(*args, **kwargs):
            if ServiceHandler.check_service_enabled(service_name):
                result = func_to_decorate(*args, **kwargs)
                logger.info("Brand is allowed to use this service")
                return result
            else:
                raise ServiceNotActiveException
        wrapper.__doc__ = func_to_decorate.__doc__
        wrapper.__name__ = func_to_decorate.__name__
        return wrapper
    return check_service_wrapper

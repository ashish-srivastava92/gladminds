'''
this file contains logic for handling services enabled by brands .
'''

from gladminds.default.models import BrandService 
from django.conf import settings


class Services():
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
    
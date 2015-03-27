from django.conf import settings
import os
def add_slashes(data):
    if data.startswith('/'):
        data = data[1:]
    if not data.endswith('/'):
        data = data + '/'

    return data


class Constants():
        BRAND = "testbrand"
        INDUSTRY = "testindustry"
        PRODUCT_TYPE = "testproducttype"


class AfterbuyUrls():
        REGISTRATION = 'consumers/registration/'
        LOGIN = 'consumers/login/'
        BRAND = 'brands/'
        INDUSTRY = 'industries/'
        
class BajajUrls():
        COUPONS = 'coupons/'
        LOGIN = 'gm-users/login/'
        MESSAGES = 'messages/'
        
COUPON_SCHEMA = open(os.path.join(settings.BASE_DIR, 'tests/smoke/core/testdata/coupon_data.json')).read()


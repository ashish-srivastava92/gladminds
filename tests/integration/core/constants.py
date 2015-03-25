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
        
#COUPON_SCHEMA = open(os.path.join(settings.BASE_DIR, 'tests/smoke/bajaj/testdata/coupon_data.json')).read()
DISPATCH_XML_DATA = open(os.path.join(settings.BASE_DIR, 'tests/integration/bajaj/test_data/product_dispatch_feed.xml')).read()
PURCHASE_XML_DATA = open(os.path.join(settings.BASE_DIR, 'tests/integration/bajaj/test_data/product_purchase_feed.xml')).read()       
SERVICE_ADVISOR_DATA = open(os.path.join(settings.BASE_DIR, 'tests/integration/bajaj/test_data/service_advisor_feed.xml')).read()
        
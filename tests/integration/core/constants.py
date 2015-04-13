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
        LOGOUT = 'gm-users/logout/'
        DEALER_LOGIN = 'aftersell/dealer/login/'
        
COUPON_SCHEMA = open(os.path.join(settings.BASE_DIR, 'tests/smoke/core/testdata/coupon_data.json')).read()
DISPATCH_XML_DATA = open(os.path.join(settings.BASE_DIR, 'tests/integration/bajaj/test_data/product_dispatch_feed.xml')).read()
PURCHASE_XML_DATA = open(os.path.join(settings.BASE_DIR, 'tests/integration/bajaj/test_data/product_purchase_feed.xml')).read()       
SERVICE_ADVISOR_DATA = open(os.path.join(settings.BASE_DIR, 'tests/integration/bajaj/test_data/service_advisor_feed.xml')).read()
OLD_FSC_DATA = open(os.path.join(settings.BASE_DIR, 'tests/integration/bajaj/test_data/old_fsc_feed.xml')).read()
CREDIT_NOTE_DATA=open(os.path.join(settings.BASE_DIR, 'tests/integration/bajaj/test_data/credit_note_feed.xml')).read()  
CUSTOMER_DATA = (('customer-phone','7777777777'), ('customer-name','TestU2927'), ('purchase-date','02/04/2015'),( 'customer-vin','12345678901232792'),('customer-id','TM-29122701'))
SA_DATA=(('sa-id',''),('phone-number','6767676767'),('name','SA29'),('status','Y'))
EXISTING_SA_DATA=(('sa-id','GMDEALER001SA31'),('phone-number','1111111111'),('name','TestUser31'),('status','Y'))
UPDATE_SA_DATA=(('sa-id','GMDEALER001SA31'),('phone-number','1111111111'),('name','TestUser31'),('status','N'))
ASC_DATA=(('name','ASC29'),('address','#66/2A,AFS,Jalahalli(west)'),('password','123'),('phone-number','9999999999'),('email','SA1@hashedin'),('pincode','560015')) 
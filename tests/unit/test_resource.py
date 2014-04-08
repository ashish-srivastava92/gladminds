import json, os
from gladminds.models import common
from django.test.client import Client
from django.conf import settings
from django.contrib.auth.models import User
from integration.base_integration import GladmindsResourceTestCase

client = Client()

class GladmindsResourcesTest(GladmindsResourceTestCase):
    def setUp(self):
        super(GladmindsResourcesTest, self).setUp()
        
        file_path = os.path.join(settings.BASE_DIR, 'etc/data/data.json')
        self.data = json.load(open(file_path))['data']
        dealer = self.data['export']['dealer']
        file_path = os.path.join(settings.BASE_DIR, 'etc/data/template.json')
        message_templates = json.loads(open(file_path).read())
        brand_obj = self.get_brand_obj(brand_id='brand001', brand_name='bajaj')
        product_type_obj = self.get_product_type_obj(brand_id=brand_obj, product_name='DISCO120', product_type='BIKE')
        dealer_obj = self.get_delear_obj(dealer_id='DEALER001')
        customer_obj = self.get_customer_obj(phone_number='9999999')
        product_obj = self.get_product_obj(vin="VINXXX001", producttype_data=product_type_obj, dealer_data = dealer_obj\
                                           , customer_phone_number = customer_obj, sap_customer_id='SAP001')
        service_advisor = self.get_service_advisor_obj(dealer_data = dealer_obj, service_advisor_id = 'SA001Test'\
                                                 ,name='UMOTO', phone_number='4444861111', status='Y')
        service_advisor = self.get_service_advisor_obj(dealer_data = dealer_obj, service_advisor_id = 'SA002Test'\
                                                 ,name='UMOTOR', phone_number='9999999999', status='Y')
        advisor_dealer_rel_obj = self.get_dealer_service_advisor_obj(dealer_data=dealer_obj, service_advisor_id=service_advisor, status='Y')
        coupon_obj = self.get_coupon_obj(unique_service_coupon='COUPON005', product_data=product_obj, valid_days=30\
                                         , valid_kms=500, service_type = 1)
        
    def test_dispatch_gladminds(self):
        result = client.post('/v1/messages', data = {'text':'CHECK SAP001 500 1', 'phoneNumber' : '4444861111'})
        self.assertHttpOK(result)
        self.assertTrue('true' in result.content)
        result = client.post('/v1/messages', data = {'text':'CLOSE SAP001 COUPON005', 'phoneNumber' : '9999999999'})
        self.assertTrue('False' in result.content)
        self.assertHttpOK(result)
        result = client.post('/v1/messages', data = {'text':'CLOSE TESTVECHILEID00002 COUPON005', 'phoneNumber' : '4444861111'})
        self.assertTrue('true' in result.content)
        self.assertHttpOK(result)
        result = client.post('/v1/messages', data = {'text':'CHECK SAP001 500', 'phoneNumber' : '4444861111'})
        self.assertHttpBadRequest(result)
        result = client.post('/v1/messages', data = {'text':'CLOSE TESTVECHILEID00002', 'phoneNumber' : '4444861111'})
        self.assertHttpBadRequest(result)
        
        
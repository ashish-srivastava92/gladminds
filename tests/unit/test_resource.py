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
        file_path = os.path.join(settings.BASE_DIR, 'etc/data/template.json')
        brand_obj = self.get_brand_obj(brand_id='brand001', brand_name='bajaj')
        product_type_obj = self.get_product_type_obj(brand_id=brand_obj, product_name='DISCO120', product_type='BIKE')
        dealer_obj = self.get_delear_obj(dealer_id='DEALER001')
        customer_obj = self.get_customer_obj(phone_number='9999999')
        product_obj = self.get_product_obj(vin="VINXXX001", producttype_data=product_type_obj, dealer_data = dealer_obj\
                                           , customer_phone_number = customer_obj, sap_customer_id='SAP001')
        service_advisor = self.get_service_advisor_obj(dealer_data = dealer_obj, service_advisor_id = 'SA001Test'\
                                                 ,name='UMOTO', phone_number='+914444861111', status='Y')
        self.get_dealer_service_advisor_obj(dealer_data=dealer_obj, service_advisor_id=service_advisor, status='Y')
        service_advisor1 = self.get_service_advisor_obj(dealer_data = dealer_obj, service_advisor_id = 'SA002Test'\
                                                 ,name='UMOTOR', phone_number='+919999999999', status='Y')
        self.get_dealer_service_advisor_obj(dealer_data=dealer_obj, service_advisor_id=service_advisor1, status='Y')
        self.get_coupon_obj(unique_service_coupon='COUPON005', product_data=product_obj, valid_days=30\
                                         , valid_kms=500, service_type = 1)
        customer_obj1 = self.get_customer_obj(phone_number='8888888')
        product_obj1 = self.get_product_obj(vin="VINXXX002", producttype_data=product_type_obj, dealer_data = dealer_obj\
                                           , customer_phone_number = customer_obj1, sap_customer_id='SAP002')
        self.get_coupon_obj(unique_service_coupon='COUPON004', product_data=product_obj1, valid_days=30\
                                         , valid_kms=500, service_type = 1)
        self.get_coupon_obj(unique_service_coupon='COUPON006', product_data=product_obj, valid_days=30\
                                         , valid_kms=3000, service_type = 2)
        self.get_coupon_obj(unique_service_coupon='COUPON007', product_data=product_obj, valid_days=30\
                                         , valid_kms=6000, service_type = 3)
        
    def test_dispatch_gladminds(self):
        result = client.post('/v1/messages', data = {'text':'A SAP001 500 1', 'phoneNumber' : '4444861111'})
        self.assertHttpOK(result)
        self.assertTrue('true' in result.content)
        result = client.post('/v1/messages', data = {'text':'A SAP001 500', 'phoneNumber' : '4444861111'})
        self.assertHttpBadRequest(result)
        result = client.post('/v1/messages', data = {'text':'C TESTVECHILEID00002', 'phoneNumber' : '4444861111'})
        self.assertHttpBadRequest(result)
        
    def test_format_message(self):
        result = client.post('/v1/messages', data = {'text':'   A    SAP001   500   1    ', 'phoneNumber' : '4444861111'})
        self.assertHttpOK(result)
        self.assertTrue('true' in result.content)
        
    def test_close_coupon(self):
        '''
            Coupon has been initiated by dealer - UMOTO
            Only UMOTO is allowed to close the coupon
        '''
        result = client.post('/v1/messages', data = {'text':'A SAP001 500 1', 'phoneNumber' : '4444861111'})
        self.assertHttpOK(result)
        self.assertTrue('true' in result.content)
#       Below Dealer will not be able to close the coupon
        result = client.post('/v1/messages', data = {'text':'C SAP001 COUPON005', 'phoneNumber' : '9999999999'})
        self.assertTrue('false' in result.content)
        self.assertHttpOK(result)
#       Below is the initiator and the coupon will be closed
        result = client.post('/v1/messages', data = {'text':'C SAP001 COUPON005', 'phoneNumber' : '4444861111'})
        self.assertTrue('true' in result.content)
        self.assertHttpOK(result)
        
    def test_is_valid_data(self):
        result = client.post('/v1/messages', data = {'text':'A SAP001 500 1', 'phoneNumber' : '4444861111'})
        self.assertHttpOK(result)
        self.assertTrue('true' in result.content)
        result = client.post('/v1/messages', data = {'text':'A SAP002 500 1', 'phoneNumber' : '4444861111'})
        self.assertHttpOK(result)
        self.assertTrue('true' in result.content)
        result = client.post('/v1/messages', data = {'text':'C SAP002 COUPON005', 'phoneNumber' : '4444861111'})
        self.assertTrue('false' in result.content)
        self.assertHttpOK(result)
        result = client.post('/v1/messages', data = {'text':'C SAP001 COUPON004', 'phoneNumber' : '4444861111'})
        self.assertTrue('false' in result.content)
        self.assertHttpOK(result)
        
    def test_expire_or_close_less_kms_coupon(self):
        result = client.post('/v1/messages', data = {'text':'A SAP001 500 1', 'phoneNumber' : '4444861111'})
        self.assertHttpOK(result)
        self.assertTrue('true' in result.content)
        #Coupon validation is tested for 3rd service coupon "COUPON007" with coupon for service 2 "COUPON006" unused.
        result = client.post('/v1/messages', data = {'text':'A SAP001 5500 3', 'phoneNumber' : '4444861111'})
        self.assertHttpOK(result)
        result = client.post('/v1/messages', data = {'customerId': 'SAP001', 'action' : 'validate', 'odoRead' : 5500, 'serviceType' : 3, 'advisorMobile' : '4444861111'})
        self.assertHttpOK(result)
        self.assertTrue('true' in result.content)
        #The coupon for service 2 should have been expired.
        coupon_obj = self.filter_coupon_obj(coupon_id='COUPON006')
        self.assertEqual(coupon_obj.status, 3)
        #The 3rd service coupon should be in progress.
        coupon_obj = self.filter_coupon_obj(coupon_id='COUPON007')
        self.assertEqual(coupon_obj.status, 4)
        
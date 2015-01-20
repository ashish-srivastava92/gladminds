import time
from integration.bajaj.base_integration import BrandResourceTestCase
from integration.bajaj.base import BaseTestCase
from integration.bajaj.test_brand_logic import Brand
from integration.bajaj.test_system_logic import System

from django.test import TestCase

from gladminds.bajaj import models
from django.test.client import Client
import logging
import json
logger = logging.getLogger('gladminds')

client = Client()


class CustomerRegistrationTest(BrandResourceTestCase, BaseTestCase):
 
    def setUp(self):
        TestCase.setUp(self)
        BaseTestCase.setUp(self)
        self.brand = Brand(self)
        self.system = System(self)
        MSG_CUST_REG = "GCP_REG test.user@test.com TestUser"
        PHONE_NUMBER = "+TS{0}".format(int(time.time()))
        self.CUST_REG = {'text': MSG_CUST_REG, 'phoneNumber': PHONE_NUMBER}
 
        # iNVALID MESSAGE
        MSG_INVALID_CUST_REG = "GCP_REG test.user@test.com"
        self.INVALID_CUST_REG = {
            'text': MSG_INVALID_CUST_REG, 'phoneNumber': PHONE_NUMBER}
 
        # INVALID KEYWORD
        MSG_INVALID_CUST_REG_KEY = "REG test.user@test.com TestUser"
        self.INVALID_CUST_REG_KEY = {
            'text': MSG_INVALID_CUST_REG_KEY, 'phoneNumber': PHONE_NUMBER}
 
        # Already Register
        MSG_ALREADY_CUST_REG = "GCP_REG test.gladminds@test.com Test Gldaminds"
        self.ALREADY_CUST_REG = {
            'text': MSG_ALREADY_CUST_REG, 'phoneNumber': '+TS0000000001'}
 
    def test_customer_registration(self):
        brand = self.brand
        system = self.system
        response = brand.send_sms(url=self.MESSAGE_URL, message=self.CUST_REG)
        system.verify_result(input=response.status_code, output=200)
 
    def test_invalid_message(self):
        brand = self.brand
        system = self.system
        response = brand.send_sms(url=self.MESSAGE_URL, message=self.INVALID_CUST_REG)
        system.verify_result(input=response.status_code, output=400)
        response = brand.send_sms(url=self.MESSAGE_URL, message=self.INVALID_CUST_REG_KEY)
        system.verify_result(input=response.status_code, output=400)
 
    def test_already_registered_customer(self):
        brand = self.brand
        system = self.system
        response = brand.send_sms(url=self.MESSAGE_URL, message=self.ALREADY_CUST_REG)
        system.verify_result(input=response.status_code, output=200)


class CustomerServiceTest(BaseTestCase):
 
    def setUp(self):
        TestCase.setUp(self)
        BaseTestCase.setUp(self)
        self.brand = Brand(self)
        self.system = System(self)
        VALID_MSG_SERVICE = "SERVICE F0B18AE"
        VALID_PHONE_NUMBER = "+TS9800000011"
        self.vlid_service_message = {
            'text': VALID_MSG_SERVICE, 'phoneNumber': VALID_PHONE_NUMBER}
 
        # Invalid check customer id
        INVALID_MSG_SERVICE = "SERVICE 000000"
        self.inavlid_service_message = {
            'text': INVALID_MSG_SERVICE, 'phoneNumber': VALID_PHONE_NUMBER}
 
        # Invalid Phone Number
        INVALID_PHONE_NUMBER = "+TA0000000011"
        self.service_message_with_invalid_phone_number = {
            'text': VALID_MSG_SERVICE, 'phoneNumber': INVALID_PHONE_NUMBER}
 
    def test_valid_service(self):
        brand = self.brand
        system = self.system
        response = brand.send_sms(url=self.MESSAGE_URL, message=self.vlid_service_message)
        system.verify_result(input=response.status_code, output=200)
 
    def test_invalid_service(self):
        brand = self.brand
        system = self.system
        response = brand.send_sms(url=self.MESSAGE_URL, message=self.inavlid_service_message)
        system.verify_result(input=response.status_code, output=200)
        response = brand.send_sms(url=self.MESSAGE_URL, message=self.service_message_with_invalid_phone_number)
        system.verify_result(input=response.status_code, output=200)


class CouponCheckAndClosure(BrandResourceTestCase, BaseTestCase):

    def setUp(self):
        '''
            Test Case Checking coupon validation can be done only from
            registered dealer's number
        '''
        TestCase.setUp(self)
        BaseTestCase.setUp(self)
        self.brand = Brand(self)
        brand = self.brand
        self.system = System(self)
        self.create_user(username='gladminds', email='gladminds@gladminds.co', password='gladminds')
        brand.send_service_advisor_feed()
        brand.send_dispatch_feed()
        brand.send_purchase_feed()
        self.product_obj = brand.get_product_obj(product_id='XXXXXXXXXX')

    def test_simple_inprogress_from_unused(self):
        brand = self.brand
        system = self.system
        create_sms_dict = {'kms': 450, 'service_type': 1, 'sap_customer_id': 'GMCUSTOMER01'}
        brand.check_coupon(create_sms_dict, "9999999999")
        coupon_status = brand.check_coupon_status(unique_service_coupon='USC001')
        system.verify_result(input=coupon_status.status, output=4)

#     Need to find out how to write this test case because it creates cyclic dependency.
#     def test_validate_dealer(self):
#         self.assertEqual(models.ServiceAdvisor.objects.count(), 1, "Service Advisor Obj is not created as required")
#         obj = GladmindsResources()
#         self.assertEqual(obj.validate_dealer("9999999999").phone_number, u"9999999999", "validate dealer")
#         sa_obj = models.ServiceAdvisor.objects.filter(service_advisor_id='DEALER001SA001')
#         sa_dealer_rel = models.ServiceAdvisorDealerRelationship.objects.filter(service_advisor_id = sa_obj[0])[0]
#         sa_dealer_rel.status = 'N'
#         sa_dealer_rel.save()

    def test_coupon_expiry(self):
        brand = self.brand
        system = self.system
        brand.get_coupon_obj(unique_service_coupon='USC0002', product=self.product_obj, valid_days=30, valid_kms=2000, service_type=2)
        brand.get_coupon_obj(unique_service_coupon='USC0003', product=self.product_obj, valid_days=30, valid_kms=5000, service_type=3)
        create_sms_dict = {'kms': 2050, 'service_type': 3, 'sap_customer_id': 'GMCUSTOMER01'}
        brand.check_coupon(create_sms_dict, '9999999999')
        system.verify_result(input=models.CouponData.objects.filter(unique_service_coupon='USC001')[0].status, output=5)
        system.verify_result(input=models.CouponData.objects.filter(unique_service_coupon='USC0002')[0].status, output=5)
        system.verify_result(input=models.CouponData.objects.filter(unique_service_coupon='USC0003')[0].status, output=4)
  
    def test_invalid_ucn_or_sap_id(self):
        brand = self.brand
        brand.get_coupon_obj(unique_service_coupon='USC0002', product=self.product_obj, valid_days=30, valid_kms=2000, service_type=2)
        brand.get_coupon_obj(unique_service_coupon='USC0003', product=self.product_obj, valid_days=30, valid_kms=5000, service_type=3)
        data = 'C {0} {1}'.format('SAP004', 'USC002')
        sms_dict = {'text': data, 'phoneNumber': '9999999999'}
        response = brand.send_sms(url=self.MESSAGE_URL, message=sms_dict)
        result = json.loads(response.content)
        self.assertFalse(result['status'])

    def test_coupon_logic_1(self):
        '''
            check SAP001 450 2
            If we have check coupon with this message
            and 1 service is unused.
            Then then 1 is in-progress and 2 is in unused state
        '''
        brand = self.brand
        system = self.system
        brand.get_coupon_obj(unique_service_coupon='USC0003', product=self.product_obj, valid_days=30, valid_kms=1000, service_type=2)
        '''Service Advisor Obj is not created as required'''
        system.verify_result(input=models.ServiceAdvisor.objects.count(), output=3)
        create_sms_dict = {'kms': 450, 'service_type': 2, 'sap_customer_id': 'GMCUSTOMER01'}
        brand.check_coupon(create_sms_dict, '9999999999')
  
        '''In-progress Coupon'''
        coupon_status = brand.check_coupon_status(unique_service_coupon='USC002')
        system.verify_result(input=coupon_status.status, output=4)
     
        '''Unused Coupon'''
        coupon_status = brand.check_coupon_status(unique_service_coupon='USC001')
        system.verify_result(input=coupon_status.status, output=1)
 
    def test_coupon_logic_2(self):
        '''
            If we have check coupon with this message
            check SAP001 600 2.
            Then then 1 is expired and 2 is in progress state
        '''
        brand = self.brand
        system = self.system
        brand.get_coupon_obj(unique_service_coupon='USC0002', product=self.product_obj, valid_days=30, valid_kms=1000, service_type=2)
 
        '''Service Advisor Obj is not created as required'''
        system.verify_result(input=models.ServiceAdvisor.objects.count(), output=3)
 
        create_sms_dict = {'kms': 600, 'service_type': 2, 'sap_customer_id': 'GMCUSTOMER01'}
        brand.check_coupon(create_sms_dict, '9999999999')
 
        '''In-progress Coupon'''
        coupon_status = brand.check_coupon_status(unique_service_coupon='USC0002')
        system.verify_result(input=coupon_status.status, output=4)
 
        '''Unused Coupon'''
        coupon_status = brand.check_coupon_status(unique_service_coupon='USC001')
        system.verify_result(input=coupon_status.status, output=5)
 
    def test_coupon_logic_3(self):
        '''
            Initial state
            coupon 1 is in unused and valid in b/w (400 - 500)
            coupon 2 is in unused and valid in b/w (900 - 1000)
            If we have check coupon with this message
            check SAP001 1100 2
            Mark 1 service as exceed limit if it not used yet
            or nothing happen to coupon 1 if it is in-progress
            And make 2 service as exceed limit
        '''
        brand = self.brand
        system = self.system
        brand.get_coupon_obj(unique_service_coupon='USC0002', product=self.product_obj, valid_days=30, valid_kms=1000, service_type=2)
  
        '''Service Advisor Obj is not created as required'''
        system.verify_result(input=models.ServiceAdvisor.objects.count(), output=3)
  
        create_sms_dict = {'kms': 1100, 'service_type': 2, 'sap_customer_id': 'GMCUSTOMER01'}
        brand.check_coupon(create_sms_dict, '9999999999')
  
        '''in_progess_coupon status should be 4'''
        coupon_status = brand.check_coupon_status(unique_service_coupon='USC001')
        system.verify_result(input=coupon_status.status, output=5)
  
        '''Coupon should be in unused State'''
        coupon_status = brand.check_coupon_status(unique_service_coupon='USC0002')
        system.verify_result(input=coupon_status.status, output=5)
  
    def test_coupon_logic_4(self):
        '''
            Initial state
            coupon 1 is in in-progress and valid in b/w (400 - 500)
            coupon 2 is in unused and valid in b/w (900 - 1000)
            If we have check coupon with this message
            check SAP001 1100 2
            Mark 1 service as exceed limit if it not used yet
            or nothing happen to coupon 1 if it is in-progress
            And make 2 service as exceed limit
        '''
        brand = self.brand
        system = self.system
  
        brand.get_coupon_obj(unique_service_coupon='USC0002', product=self.product_obj, valid_days=30, valid_kms=1000, service_type=2)
  
        '''Service Advisor Obj is not created as required'''
        system.verify_result(input=models.ServiceAdvisor.objects.count(), output=3)
  
        sms_dict = {'kms': 450, 'service_type': 1, 'sap_customer_id': 'GMCUSTOMER01'}
        brand.check_coupon(sms_dict, '9999999999')
  
        sms_dict = {'kms': 1100, 'service_type': 2, 'sap_customer_id': 'GMCUSTOMER01'}
        brand.check_coupon(sms_dict, '9999999999')
  
        '''in_progess_coupon status should be 4'''
        coupon_status = brand.check_coupon_status(unique_service_coupon='USC001')
        system.verify_result(input=coupon_status.status, output=5)
  
        '''Coupon should be in unused State'''
        coupon_status = brand.check_coupon_status(unique_service_coupon='USC0002')
        system.verify_result(input=coupon_status.status, output=5)
  
    def test_coupon_logic_5(self):
        '''
            Initial state
            coupon 1 is in unused and valid in b/w (400 - 500)
            coupon 2 is in unused and valid in b/w (900 - 1000)
            coupon 3 is in unused and valid in b/w (1400 - 1500)
            If we have check coupon with this message
            check SAP001 1100 1
            Mark 1 as exceed limit
            Mark 2 as exceed limit
            Mark 3 as in progress
 
            check SAP001 450 1
            Mark 1 as in progress
            Mark 2 as unused
            Mark 3 as unused
        '''
        
        brand = self.brand
        system = self.system
        brand.get_coupon_obj(unique_service_coupon='USC0003', product=self.product_obj, valid_days=90, valid_kms=1500, service_type=3)
 
        sms_dict = {'kms': 1100, 'service_type': 2, 'sap_customer_id': 'GMCUSTOMER01'}
        
        brand.check_coupon(sms_dict, '9999999999')
               
        coupon_status = brand.check_coupon_status(unique_service_coupon='USC001')
        system.verify_result(input=coupon_status.status, output=5)
        coupon_status = brand.check_coupon_status(unique_service_coupon='USC002')
        system.verify_result(input=coupon_status.status, output=5)
        coupon_status = brand.check_coupon_status(unique_service_coupon='USC0003')
        system.verify_result(input=coupon_status.status, output=1)
 
        sms_dict = {'kms': 450, 'service_type': 1, 'sap_customer_id': 'GMCUSTOMER01'}
        brand.check_coupon(sms_dict, '9999999999')
        
        
        coupon_status = brand.check_coupon_status(unique_service_coupon='USC001')
        system.verify_result(input=coupon_status.status, output=4)
        coupon_status = brand.check_coupon_status(unique_service_coupon='USC002')
        system.verify_result(input=coupon_status.status, output=5)
        coupon_status = brand.check_coupon_status(unique_service_coupon='USC0003')
        system.verify_result(input=coupon_status.status, output=1)
  
        '''
            Initial state
            coupon 1 is in progress
            coupon 2 is in unused and valid in b/w (900 - 1000)
            coupon 3 is in unused and valid in b/w (1400 - 1500)
            If we have check coupon with this message
            check SAP001 1550 1
            Mark 1 as exceed limit
            Mark 2 as exceed limit
            Mark 3 as exceed limit
        '''
        sms_dict = {'kms': 1550, 'service_type': 3, 'sap_customer_id': 'GMCUSTOMER01'}
        brand.check_coupon(sms_dict, '9999999999')
  
        coupon_status = brand.check_coupon_status(unique_service_coupon='USC001')
        system.verify_result(input=coupon_status.status, output=5)
        coupon_status = brand.check_coupon_status(unique_service_coupon='USC002')
        system.verify_result(input=coupon_status.status, output=5)
        coupon_status = brand.check_coupon_status(unique_service_coupon='USC0003')
        system.verify_result(input=coupon_status.status, output=5)


class BrandData(BrandResourceTestCase, BaseTestCase):
 
    def setUp(self):
        TestCase.setUp(self)
        BaseTestCase.setUp(self)
        self.brand = Brand(self)
        self.system = System(self)
        self.PHONE_NUMBER = "+TS0000000000"
        self.VALID_BRAND_ID = {
            'text': "BRAND BRAND001", 'phoneNumber': self.PHONE_NUMBER}
        self.INVALID_BRAND_ID = {
            'text': "BRAND BRAN", 'phoneNumber': self.PHONE_NUMBER}
 
    '''
    TestCase for getting all products associated with the brand for a customer
    '''
 
    def test_get_all_products_of_a_brand(self):
        brand = self.brand
        system = self.system
        response = brand.send_sms(url=self.MESSAGE_URL, message=self.VALID_BRAND_ID)
        system.verify_result(input=response.status_code, output=200)
 
    def test_get_all_brand(self):
        brand = self.brand
        system = self.system
        response = brand.send_sms(url=self.MESSAGE_URL, message=self.INVALID_BRAND_ID)
        system.verify_result(input=response.status_code, output=200)
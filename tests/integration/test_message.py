import time
from django.core import management
from base_integration import GladmindsResourceTestCase
from gladminds.models import common
from gladminds.aftersell.models import common as aftersell_common, logs 
from django.contrib.auth.models import User
from django.test.client import Client
import logging
import json
from tastypie.exceptions import ImmediateHttpResponse
logger = logging.getLogger('gladminds')

client=Client()

class CustomerRegistrationTest(GladmindsResourceTestCase):
  
    def setUp(self):
        super(CustomerRegistrationTest, self).setUp()
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
        resp = client.post(self.MESSAGE_URL, data=self.CUST_REG)
        self.assertHttpOK(resp)
  
    def test_invalid_message(self):
        resp = client.post(self.MESSAGE_URL, data=self.INVALID_CUST_REG)
        self.assertHttpBadRequest(resp)
  
        resp = client.post(
            self.MESSAGE_URL, data=self.INVALID_CUST_REG_KEY)
        self.assertHttpBadRequest(resp)
  
    def test_already_registered_customer(self):
        resp = client.post(
            self.MESSAGE_URL, data=self.ALREADY_CUST_REG)
        self.assertHttpOK(resp)
  
  
class CustomerServiceTest(GladmindsResourceTestCase):
  
    def setUp(self):
        super(CustomerServiceTest, self).setUp()
        VALID_MSG_SERVICE = "SERVICE F0B18AE"
        VALID_PHONE_NUMBER = "+TS9800000011"
        self.MSG_SVC = {
            'text': VALID_MSG_SERVICE, 'phoneNumber': VALID_PHONE_NUMBER}
  
        # Invalid check customer id
        INVALID_MSG_SERVICE = "SERVICE 000000"
        self.IN_MSG_SVC = {
            'text': INVALID_MSG_SERVICE, 'phoneNumber': VALID_PHONE_NUMBER}
  
        # Invalid Phone Number
        INVALID_PHONE_NUMBER = "+TA0000000011"
        self.IN_PH_MSG_SVC = {
            'text': VALID_MSG_SERVICE, 'phoneNumber': INVALID_PHONE_NUMBER}
  
    def test_valid_service(self):
        resp = client.post(self.MESSAGE_URL, data=self.MSG_SVC)
        self.assertHttpOK(resp)
  
    def test_invalid_service(self):
        resp = client.post(self.MESSAGE_URL, data=self.IN_MSG_SVC)
        self.assertHttpOK(resp)
  
        resp = client.post(
            self.MESSAGE_URL, data=self.IN_PH_MSG_SVC)
        self.assertHttpOK(resp)
  
  
class CouponCheckAndClosure(GladmindsResourceTestCase):
  
    def setUp(self):
        '''
            Test Case Checking coupon validation can be done only from 
            registered dealer's number
        '''
        super(CouponCheckAndClosure, self).setUp()
        user = User.objects.create_user('gladminds', 'gladminds@gladminds.co', 'gladminds')
        user.save()
        self.brand_obj = self.get_brand_obj(brand_id='brand001', brand_name='bajaj')
        self.product_type_obj = self.get_product_type_obj(brand_id=self.brand_obj, product_name='DISCO120', product_type='BIKE')
        self.dealer_obj = self.get_delear_obj(dealer_id='DEALER001')
        self.customer_obj = self.get_customer_obj(phone_number='9999999999')
        self.product_obj = self.get_product_obj(vin="VINXXX001", product_type=self.product_type_obj, dealer_id = self.dealer_obj, customer_phone_number = self.customer_obj, sap_customer_id='SAP001')
        self.get_coupon_obj(unique_service_coupon='USC001', vin=self.product_obj, valid_days=30, valid_kms=500, service_type=1)
  
        sa_obj = self.get_service_advisor_obj(service_advisor_id='DEALER001SA001', name="SA001", phone_number='+919999999999')
        self.get_dealer_service_advisor_obj(dealer_id=self.dealer_obj, service_advisor_id=sa_obj, status='Y')
  
  
    def validate_coupon(self, data, phone_number):
        data = 'A {1} {0} {2}'.format(data['kms'], data['sap_customer_id'], data['service_type'])
        result = client.post('/v1/messages', data={'text': data, 'phoneNumber' : phone_number})
        self.assertHttpOK(result)
  
    def test_simple_inprogress_from_unused(self):
        phone_number = "9999999999"
        self.assertEqual(aftersell_common.ServiceAdvisor.objects.count(), 1, "Service Advisor Obj is not created as required")
          
        sms_dict = {'kms': 450, 'service_type': 1, 'sap_customer_id': 'SAP001'}
        self.validate_coupon(sms_dict, phone_number)
          
        in_progess_coupon = common.CouponData.objects.get(unique_service_coupon='USC001')
        print "fdsads", common.CouponData.objects.all()[0].status
        self.assertEqual(in_progess_coupon.status, 4, "in_progess_coupon status should be 4")
  
#     Need to find out how to write this test case because it creates cyclic dependency.
#     def test_validate_dealer(self):
#         self.assertEqual(common.ServiceAdvisor.objects.count(), 1, "Service Advisor Obj is not created as required")
#         obj = GladmindsResources()
#         self.assertEqual(obj.validate_dealer("9999999999").phone_number, u"9999999999", "validate dealer")
#         sa_obj = common.ServiceAdvisor.objects.filter(service_advisor_id='DEALER001SA001')
#         sa_dealer_rel = common.ServiceAdvisorDealerRelationship.objects.filter(service_advisor_id = sa_obj[0])[0]
#         sa_dealer_rel.status = 'N'
#         sa_dealer_rel.save()
  
    def test_coupon_expiry(self):
        self.get_coupon_obj(unique_service_coupon='USC002', vin=self.product_obj, valid_days=30, valid_kms=2000, service_type=2)
        self.get_coupon_obj(unique_service_coupon='USC003', vin=self.product_obj, valid_days=30, valid_kms=5000, service_type=3)
          
        sms_dict = {'kms': 2050, 'service_type': 3, 'sap_customer_id': 'SAP001'}
          
        self.validate_coupon(sms_dict, '9999999999')
          
        self.assertEquals(5, common.CouponData.objects.filter(unique_service_coupon='USC001')[0].status)
        self.assertEquals(5, common.CouponData.objects.filter(unique_service_coupon='USC002')[0].status)
        self.assertEquals(4, common.CouponData.objects.filter(unique_service_coupon='USC003')[0].status)
  
  
    def test_invalid_ucn_or_sap_id(self):
        self.get_coupon_obj(unique_service_coupon='USC002', vin=self.product_obj, valid_days=30, valid_kms=2000, service_type=2)
        self.get_coupon_obj(unique_service_coupon='USC003', vin=self.product_obj, valid_days=30, valid_kms=5000, service_type=3)
          
          
        data = 'C {0} {1}'.format('SAP004', 'USC002')
        result = client.post('/v1/messages', data={'text': data, 'phoneNumber' : '9999999999'})
        result = json.loads(result.content)
        self.assertFalse(result['status'])
          
    def test_forward_logic_1(self):
        '''
            check SAP001 450 2
            If we have check coupon with this message
            and 1 service is unused.
            Then then 1 is in-progress and 2 is in unused state
        '''
        self.get_coupon_obj(unique_service_coupon='USC002', vin=self.product_obj, valid_days=30, valid_kms=1000, service_type=2)
  
        phone_number = "9999999999"
        self.assertEqual(aftersell_common.ServiceAdvisor.objects.count(), 1, "Service Advisor Obj is not created as required")
          
        sms_dict = {'kms': 450, 'service_type': 2, 'sap_customer_id': 'SAP001'}
        self.validate_coupon(sms_dict, phone_number)
  
        in_progess_coupon = common.CouponData.objects.get(unique_service_coupon='USC001')
        self.assertEqual(in_progess_coupon.status, 4, "in_progess_coupon status should be 4")
  
        in_progess_coupon = common.CouponData.objects.get(unique_service_coupon='USC002')
        self.assertEqual(in_progess_coupon.status, 1, "Coupon should be in unused State")
  
    def test_forward_logic_2(self):
        '''
            If we have check coupon with this message
            check SAP001 450 2
            and 1 service is in-progress.
            Then then 1 is in-progress and 2 is in unused state
        '''
        self.get_coupon_obj(unique_service_coupon='USC002', vin=self.product_obj, valid_days=30, valid_kms=1000, service_type=2)
  
        phone_number = "9999999999"
        self.assertEqual(aftersell_common.ServiceAdvisor.objects.count(), 1, "Service Advisor Obj is not created as required")
          
        sms_dict = {'kms': 450, 'service_type': 2, 'sap_customer_id': 'SAP001'}
        self.validate_coupon(sms_dict, phone_number)
  
        in_progess_coupon = common.CouponData.objects.get(unique_service_coupon='USC001')
        self.assertEqual(in_progess_coupon.status, 4, "in_progess_coupon status should be 4")
  
        in_progess_coupon = common.CouponData.objects.get(unique_service_coupon='USC002')
        self.assertEqual(in_progess_coupon.status, 1, "Coupon should be in unused State")
  
    def test_forward_logic_3(self):
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
  
        self.get_coupon_obj(unique_service_coupon='USC002', vin=self.product_obj, valid_days=30, valid_kms=1000, service_type=2)
  
        phone_number = "9999999999"
        self.assertEqual(aftersell_common.ServiceAdvisor.objects.count(), 1, "Service Advisor Obj is not created as required")
          
        sms_dict = {'kms': 1100, 'service_type': 2, 'sap_customer_id': 'SAP001'}
        self.validate_coupon(sms_dict, phone_number)
  
        in_progess_coupon = common.CouponData.objects.get(unique_service_coupon='USC001')
        self.assertEqual(in_progess_coupon.status, 5, "in_progess_coupon status should be 4")
  
        in_progess_coupon = common.CouponData.objects.get(unique_service_coupon='USC002')
        self.assertEqual(in_progess_coupon.status, 5, "Coupon should be in unused State")
  
    def test_forward_logic_4(self):
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
  
        self.get_coupon_obj(unique_service_coupon='USC002', vin=self.product_obj, valid_days=30, valid_kms=1000, service_type=2)
  
        phone_number = "9999999999"
        self.assertEqual(aftersell_common.ServiceAdvisor.objects.count(), 1, "Service Advisor Obj is not created as required")
          
  
        sms_dict = {'kms': 450, 'service_type': 1, 'sap_customer_id': 'SAP001'}
        self.validate_coupon(sms_dict, phone_number)
  
        sms_dict = {'kms': 1100, 'service_type': 2, 'sap_customer_id': 'SAP001'}
        self.validate_coupon(sms_dict, phone_number)
  
        in_progess_coupon = common.CouponData.objects.get(unique_service_coupon='USC001')
        self.assertEqual(in_progess_coupon.status, 5, "in_progess_coupon status should be 4")
  
        in_progess_coupon = common.CouponData.objects.get(unique_service_coupon='USC002')
        self.assertEqual(in_progess_coupon.status, 5, "Coupon should be in unused State")
  
    def test_forward_logic_5(self):
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
        phone_number = "9999999999"
        self.get_coupon_obj(unique_service_coupon='USC002', vin=self.product_obj, valid_days=60, valid_kms=1000, service_type=2)
        self.get_coupon_obj(unique_service_coupon='USC003', vin=self.product_obj, valid_days=90, valid_kms=1500, service_type=3)
  
        sms_dict = {'kms': 1100, 'service_type': 2, 'sap_customer_id': 'SAP001'}
          
        self.validate_coupon(sms_dict, phone_number)
  
        self.assertCouponStatus('USC001', 5)
        self.assertCouponStatus('USC002', 5)
        self.assertCouponStatus('USC003', 4)
  
        sms_dict = {'kms': 450, 'service_type': 1, 'sap_customer_id': 'SAP001'}
        self.validate_coupon(sms_dict, phone_number)
  
        self.assertCouponStatus('USC001', 4)
        self.assertCouponStatus('USC002', 1)
        self.assertCouponStatus('USC003', 1)
  
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
        sms_dict = {'kms': 1550, 'service_type': 3, 'sap_customer_id': 'SAP001'}
        self.validate_coupon(sms_dict, phone_number)
  
        self.assertCouponStatus('USC001', 5)
        self.assertCouponStatus('USC002', 5)
        self.assertCouponStatus('USC003', 5)
  
    def assertCouponStatus(self, coupon_id, status):
        coupon_obj = common.CouponData.objects\
                        .get(unique_service_coupon=coupon_id)
        self.assertEqual(coupon_obj.status, status, \
          "Coupon Status should be %s. It is %s" % (status, coupon_obj.status))
  
  
class BrandData(GladmindsResourceTestCase):
  
    def setUp(self):
        super(BrandData, self).setUp()
        self.PHONE_NUMBER = "+TS0000000000"
        self.VALID_BRAND_ID = {
            'text': "BRAND BRAND001", 'phoneNumber': self.PHONE_NUMBER}
        self.INVALID_BRAND_ID = {
            'text': "BRAND BRAN", 'phoneNumber': self.PHONE_NUMBER}
  
    '''
    TestCase for getting all products associated with the brand for a customer
    '''
  
    def test_get_all_products_of_a_brand(self):
        resp = client.post(
            self.MESSAGE_URL, data=self.VALID_BRAND_ID)
        self.assertHttpOK(resp)
  
    def test_get_all_brand(self):
        resp = client.post(
            self.MESSAGE_URL, data=self.INVALID_BRAND_ID)
        self.assertHttpOK(resp)



class CustomerIdReccovery(GladmindsResourceTestCase):

    def setUp(self):
        super(CustomerIdReccovery, self).setUp()
        user = User.objects.create_user('gladminds', 'gladminds@gladminds.co', 'gladminds')
        user.save()
        self.brand_obj = self.get_brand_obj(brand_id='brand001', brand_name='bajaj')
        self.product_type_obj = self.get_product_type_obj(brand_id=self.brand_obj, product_name='DISCO120', product_type='BIKE')
        self.dealer_obj = self.get_delear_obj(dealer_id='DEALER001')
        self.customer_obj = self.get_customer_obj(phone_number='9999999999')
        self.product_obj = self.get_product_obj(vin="VINXXX001", product_type=self.product_type_obj, dealer_id = self.dealer_obj, customer_phone_number = self.customer_obj, sap_customer_id='SAP001')

        self.PHONE_NUMBER = "9999999999"
        self.VALID_VIN_ID = {
            'text': "r vin VINXXX001", 'phoneNumber': self.PHONE_NUMBER}
        self.INVALID_VIN_ID = {
            'text': "r vin VINXXX002", 'phoneNumber': self.PHONE_NUMBER}

    '''
    TestCase to recover id and vin from vin and id respectively
    '''
    
    def test_get_sap_id_by_vin(self):
        resp = client.post(
            self.MESSAGE_URL, data=self.VALID_VIN_ID)
        audit_log_objects =  logs.AuditLog.objects.all()
        self.assertEqual('Your id is SAP001.', audit_log_objects[2].message)
        self.assertHttpOK(resp)
        
        resp = client.post(
            self.MESSAGE_URL, data=self.INVALID_VIN_ID)
        audit_log_objects =  logs.AuditLog.objects.all()
        self.assertEqual('Incorrect vin or no matching details.', audit_log_objects[4].message)
        self.assertHttpOK(resp)
        

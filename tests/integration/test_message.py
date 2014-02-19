import time
from django.core import management
from base_integration import GladmindsResourceTestCase

class CustomerRegistrationTest(GladmindsResourceTestCase):
    def setUp(self):
        super(CustomerRegistrationTest, self).setUp()
        MSG_CUST_REG = "GCP_REG test.user@test.com Test User"
        PHONE_NUMBER = "+TS{0}".format(int(time.time()))
        self.CUST_REG = {'text': MSG_CUST_REG, 'phoneNumber': PHONE_NUMBER}
         
        #iNVALID MESSAGE
        MSG_INVALID_CUST_REG = "GCP_REG test.user@test.com"
        self.INVALID_CUST_REG = {'text': MSG_INVALID_CUST_REG, 'phoneNumber': PHONE_NUMBER}
     
        #INVALID KEYWORD
        MSG_INVALID_CUST_REG_KEY = "REG test.user@test.com Test User"
        self.INVALID_CUST_REG_KEY = {'text': MSG_INVALID_CUST_REG_KEY, 'phoneNumber': PHONE_NUMBER}
         
        #Already Register
        MSG_ALREADY_CUST_REG = "GCP_REG test.gladminds@test.com Test Gldaminds"
        self.ALREADY_CUST_REG = {'text': MSG_ALREADY_CUST_REG, 'phoneNumber': '+TS0000000001'}
         
 
    def test_customer_registration(self):
       resp = self.api_client.post(uri=self.MESSAGE_URL, data = self.CUST_REG)
       self.assertHttpOK(resp)
         
    def test_invalid_message(self):
        resp = self.api_client.post(uri=self.MESSAGE_URL, data = self.INVALID_CUST_REG)
        self.assertHttpBadRequest(resp)
          
        resp = self.api_client.post(uri=self.MESSAGE_URL, data = self.INVALID_CUST_REG_KEY)
        self.assertHttpBadRequest(resp)
         
    def test_customer_registration(self):
       resp = self.api_client.post(uri=self.MESSAGE_URL, data = self.CUST_REG)
       self.assertHttpOK(resp)
        
    def test_already_registered_customer(self):
        resp = self.api_client.post(uri=self.MESSAGE_URL, data = self.ALREADY_CUST_REG)
        self.assertHttpOK(resp)
             
class CustomerServiceTest(GladmindsResourceTestCase):
      
     def setUp(self):
         super(CustomerServiceTest, self).setUp()
         VALID_MSG_SERVICE = "SERVICE F0B18AE"
         VALID_PHONE_NUMBER = "+TS9800000011"
         self.MSG_SVC = {'text': VALID_MSG_SERVICE, 'phoneNumber': VALID_PHONE_NUMBER}
          
         #Invalid check customer id
         INVALID_MSG_SERVICE = "SERVICE 000000"
         self.IN_MSG_SVC = {'text': INVALID_MSG_SERVICE, 'phoneNumber': VALID_PHONE_NUMBER}
          
         #Invalid Phone Number
         INVALID_PHONE_NUMBER = "+TA0000000011"
         self.IN_PH_MSG_SVC = {'text': VALID_MSG_SERVICE, 'phoneNumber': INVALID_PHONE_NUMBER}
     
     def test_valid_service(self):
        resp = self.api_client.post(uri=self.MESSAGE_URL, data = self.MSG_SVC)
        self.assertHttpOK(resp)
     
     def test_invalid_service(self):
        resp = self.api_client.post(uri=self.MESSAGE_URL, data = self.IN_MSG_SVC)
        self.assertHttpOK(resp)
         
        resp = self.api_client.post(uri=self.MESSAGE_URL, data = self.IN_PH_MSG_SVC)
        self.assertHttpOK(resp)
         
     
class CouponCheckAndClosure(GladmindsResourceTestCase):
    def setUp(self):
        super(CouponCheckAndClosure, self).setUp()
        self.MSG_CHECK_COUPON = "CHECK TESTVECHILEID00002 50 2"
        self.PHONE_NUMBER = "+SA0000000000"
        self.CHECK_COUPON = {'text': self.MSG_CHECK_COUPON, 'phoneNumber': self.PHONE_NUMBER}
        self.INVALID_PHONE_NUMBER="+0000000000"
        self.CHECK_INVALID_COUPON={'text': self.MSG_CHECK_COUPON, 
                                   'phoneNumber': self.INVALID_PHONE_NUMBER}
        self.VALID_COUPON="CHECK TESTVECHILEID00002 50 3"
        self.CHECK_VALID_COUPON = {'text': self.VALID_COUPON, 'phoneNumber': self.PHONE_NUMBER}
        self.CLOSE_COUPON={'text':'CLOSE TESTVECHILEID00002 COUPON005','phoneNumber': self.PHONE_NUMBER}
     
    '''
    Test Case Checking coupon validation can be done only from 
    registered dealer's number
    '''
    def test_check_coupon_sa(self):
       resp = self.api_client.post(uri=self.MESSAGE_URL, data=self.CHECK_COUPON)
       self.assertHttpOK(resp)
       resp = self.api_client.post(uri=self.MESSAGE_URL, data=self.CHECK_INVALID_COUPON)
       self.assertHttpUnauthorized(resp)
        
    def test_valid_coupon(self):
        resp = self.api_client.post(uri=self.MESSAGE_URL, data=self.CHECK_VALID_COUPON)
        self.assertHttpOK(resp)
        
    def test_close_coupon(self):
        resp = self.api_client.post(uri=self.MESSAGE_URL, data=self.CLOSE_COUPON)
        self.assertHttpOK(resp)
        
class BrandData(GladmindsResourceTestCase):
    def setUp(self):
        super(BrandData, self).setUp() 
        self.PHONE_NUMBER = "+TS0000000000"   
        self.VALID_BRAND_ID = {'text': "BRAND BRAND001", 'phoneNumber': self.PHONE_NUMBER}
        self.INVALID_BRAND_ID={'text': "BRAND BRAN", 'phoneNumber': self.PHONE_NUMBER}
        
    '''
    TestCase for getting all products associated with the brand for a customer
    '''        
    def test_get_all_products_of_a_brand(self):
       resp = self.api_client.post(uri=self.MESSAGE_URL, data=self.VALID_BRAND_ID)
       self.assertHttpOK(resp)
       
    def test_get_all_brand(self):
       resp = self.api_client.post(uri=self.MESSAGE_URL, data=self.INVALID_BRAND_ID)
       self.assertHttpOK(resp)
        

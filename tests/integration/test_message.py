import time
from django.core import management
from tastypie.test import ResourceTestCase

class GladmindsResourceTestCase(ResourceTestCase):
    
    def setUp(self):
        super(GladmindsResourceTestCase, self).setUp()
        management.call_command('loaddata', 'etc/testdata/template.json', verbosity=0)
        management.call_command('loaddata', 'etc/testdata/customer.json', verbosity=0)
        management.call_command('loaddata', 'etc/testdata/brand.json', verbosity=0)
        management.call_command('loaddata', 'etc/testdata/producttype.json', verbosity=0)
        management.call_command('loaddata', 'etc/testdata/dealer.json', verbosity=0)
        management.call_command('loaddata', 'etc/testdata/serviceadvisor.json', verbosity=0)
        management.call_command('loaddata', 'etc/testdata/product.json', verbosity=0)
        management.call_command('loaddata', 'etc/testdata/coupon.json', verbosity=0)
        self.MESSAGE_URL = "/v1/messages"
    
    def assertSuccessfulHttpResponse(self, resp, msg=None):
        """
        Ensures the response is returning status between 200 and 299,
         both inclusive 
        """
        return self.assertTrue(resp.status_code >= 200 
                               and resp.status_code <= 299, msg) 
        

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
        

    def test_customer_registration(self):
       resp = self.api_client.post(uri=self.MESSAGE_URL, data = self.CUST_REG)
       self.assertHttpOK(resp)
        
    def test_invalid_message(self):
        resp = self.api_client.post(uri=self.MESSAGE_URL, data = self.INVALID_CUST_REG)
        self.assertHttpBadRequest(resp)
         
        resp = self.api_client.post(uri=self.MESSAGE_URL, data = self.MSG_INVALID_CUST_REG_KEY)
        self.assertHttpBadRequest(resp)
        #Already Register
        MSG_ALREADY_CUST_REG = "GCP_REG test.gladminds@test.com Test Gldaminds"
        self.ALREADY_CUST_REG = {'text': MSG_INVALID_CUST_REG_KEY, 'phoneNumber': '+TS0000000001'}
        
    def test_customer_registration(self):
       resp = self.api_client.post(uri=self.MESSAGE_URL, data = self.CUST_REG)
       self.assertHttpOK(resp)
       
    def test_invalid_message(self):
        resp = self.api_client.post(uri=self.MESSAGE_URL, data = self.INVALID_CUST_REG)
        self.assertHttpBadRequest(resp)
        
        resp = self.api_client.post(uri=self.MESSAGE_URL, data = self.MSG_INVALID_CUST_REG_KEY)
        self.assertHttpBadRequest(resp)
    
    def test_already_registered_customer(self):
        resp = self.api_client.post(uri=self.MESSAGE_URL, data = self.ALREADY_CUST_REG)
        self.assertHttpOK(resp)
            
class CustomerServiceTest(GladmindsResourceTestCase):
     
     def setUp(self):
         super(CustomerServiceTest, self).setUp()
         MSG_CUST_REG = "SERVICE test.user@test.com Test User"
         PHONE_NUMBER = "+TS{0}".format(int(time.time()))
         self.CUST_REG = {'text': MSG_CUST_REG, 'phoneNumber': PHONE_NUMBER}
    
class CouponCheckAndClosure(GladmindsResourceTestCase):
    def setUp(self):
        super(CouponCheckAndClosure, self).setUp()
        self.MSG_CHECK_COUPON = "CHECK VIN1 50 1"
        self.PHONE_NUMBER = "+910000000000"
        self.CHECK_COUPON = {'text': self.MSG_CHECK_COUPON, 'phoneNumber': self.PHONE_NUMBER}
    
    def test_coupon_validation(self):
       print ":::::::;resp:::::::::::"
       resp = self.api_client.post(uri=self.MESSAGE_URL, data=self.CHECK_COUPON)
       print ":::::::;resp:::::::::::",resp
#        self.assertHttpOK(resp)

    
       
       
       

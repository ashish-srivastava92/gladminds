import time
from django.core import management
from tastypie.test import ResourceTestCase

class GladmindsResourceTestCase(ResourceTestCase):
    
    def setUp(self):
        super(GladmindsResourceTestCase, self).setUp()
        management.call_command('loaddata', 'etc/data/template.json', verbosity=0)
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
        self.MSG_CUST_REG = "GCP_REG test.user@test.com Test User"
        self.PHONE_NUMBER = "+TS{0}".format(int(time.time()))
        self.CUST_REG = {'text': self.MSG_CUST_REG, 'phoneNumber': self.PHONE_NUMBER}
    
        
   def test_customer_registration(self):
       resp = self.api_client.post(uri=self.MESSAGE_URL, data = self.CUST_REG)
       self.assertHttpOK(resp)
       
       

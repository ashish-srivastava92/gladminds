import time
from django.core import management
from tastypie.test import ResourceTestCase

class MessageTest(ResourceTestCase):
   
   def setUp(self):
        super(MessageTest, self).setUp()
        management.call_command('loaddata', 'etc/data/template.json', verbosity=0)
        self.URL = "/v1/messages"
        self.MSG_CUST_REG = "GCP_REG test.user@test.com Test User"
        self.PHONE_NUMBER = "+TS{0}".format(int(time.time()))
        self.CUST_REG = {'text': self.MSG_CUST_REG, 'phoneNumber': self.PHONE_NUMBER}
        
   def test_customer_registration(self):
       resp = self.api_client.post(uri=self.URL, data = self.CUST_REG)
       self.assertHttpOK(resp)

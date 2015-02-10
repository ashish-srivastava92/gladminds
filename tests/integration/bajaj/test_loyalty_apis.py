#from django.test import TestCase
import json
from django.test.client import Client
from tastypie.test import ResourceTestCase
from test_constants import NSM, ASM
client=Client(SERVER_NAME='bajaj')

class LoyaltyApiTests(ResourceTestCase):
    multi_db=True
    def setUp(self):
        super(LoyaltyApiTests, self).setUp()
 
    def post(self,uri,data):
        resp = client.post(uri, data=json.dumps(data), content_type='application/json')
        return resp
    
    def test_create_nsm(self):
        uri = '/loyalty/v1/nsms/'
        resp = self.post(uri,data=NSM)
        self.assertEquals(resp.status_code,201)
        return resp
    
    def test_get_nsm(self):
        resp = self.test_create_nsm()
        self.assertEquals(resp.status_code,201)
        resp = client.get('/loyalty/v1/nsms/1/',content_type='application/json')
        self.assertEquals(resp.status_code,200)
        self.assertEqual(self.deserialize(resp)['phone_number'], "1234567890")
        return resp
    
    def test_update_nsm(self):
        resp = self.test_get_nsm() 
        self.assertEquals(resp.status_code,200)
        a={"phone_number":"1234512345"}
        resp = client.put('/loyalty/v1/nsms/1/', data=json.dumps(a), content_type='application/json')
        self.assertEquals(resp.status_code, 200)
        resp = client.get('/loyalty/v1/nsms/1/',content_type='application/json')
        self.assertEqual(self.deserialize(resp)['phone_number'], "1234512345")
        
    def test_create_asm(self):
        uri = '/loyalty/v1/asms/'
        resp = self.post(uri,data=ASM)
        self.assertEquals(resp.status_code,201)
        return resp
    
    def test_get_asm(self):
        resp = self.test_create_asm()
        self.assertEquals(resp.status_code,201)
        resp = client.get('/loyalty/v1/asms/1/',content_type='application/json')
        self.assertEquals(resp.status_code,200)
        self.assertEqual(self.deserialize(resp)['phone_number'], "9176339712")
        return resp
    
    def test_update_asm(self):
        resp = self.test_get_asm() 
        self.assertEquals(resp.status_code,200)
        a={"phone_number":"9176339715"}
        resp = client.put('/loyalty/v1/asms/1/', data=json.dumps(a), content_type='application/json')
        self.assertEquals(resp.status_code, 200)
        resp = client.get('/loyalty/v1/asms/1/',content_type='application/json')
        self.assertEqual(self.deserialize(resp)['phone_number'], "9176339715")
        
        
    
        
    
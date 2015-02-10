#from django.test import TestCase
import json
from django.test.client import Client
from tastypie.test import ResourceTestCase, TestApiClient
from test_constants import NSM
client=Client(SERVER_NAME='bajaj')

class TestNationalSalesManager(ResourceTestCase):
    multi_db=True
    def setUp(self):
        super(TestNationalSalesManager, self).setUp()
#         self.client =Client(SERVER_NAME='bajaj')
 
    def post(self,uri,data):
        resp = client.post(uri, data=json.dumps(data), content_type='application/json')
        return resp
    
    def test_create_nsm(self):
        uri = '/loyalty/v1/nsmnames/'
        resp = self.post(uri,data=NSM)
        self.assertEquals(resp.status_code,201)
        return resp
    
    def test_get_nsm(self):
        #uri = '/loyalty/v1/nsmnames/'
        #resp = self.post(uri,data=NSM)
        resp = self.test_create_nsm()
        self.assertEquals(resp.status_code,201)
        resp = client.get('/loyalty/v1/nsmnames/1/',content_type='application/json')
        self.assertEquals(resp.status_code,200)
        self.assertEqual(self.deserialize(resp)['phone_number'], "1234567890")
        return resp
    
    def test_update_nsm(self):
        resp = self.test_get_nsm() 
        self.assertEquals(resp.status_code,200)
        a={"phone_number":"1234512345"}
        resp = client.put('/loyalty/v1/nsmnames/1/', data=json.dumps(a), content_type='application/json')
        self.assertEquals(resp.status_code, 200)
        resp = client.get('/loyalty/v1/nsmnames/1/',content_type='application/json')
        self.assertEqual(self.deserialize(resp)['phone_number'], "1234512345")
        
        
    
        
    
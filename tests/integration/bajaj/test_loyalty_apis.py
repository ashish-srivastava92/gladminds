#from django.test import TestCase
import json
from django.test.client import Client
from tastypie.test import ResourceTestCase
from test_constants import NSM
from test_constants import DISTRIBUTOR
client=Client(SERVER_NAME='bajaj')

class LoyaltyApiTests(ResourceTestCase):
    multi_db=True
    def setUp(self):
        super(LoyaltyApiTests, self).setUp()
 
    def post(self,uri,data,content_type='application/json'):
        resp = client.post(uri, data=json.dumps(data), content_type=content_type)
        return resp
    
    def get(self,uri,content_type='application/json'):
        resp = client.get(uri,content_type=content_type)
        return resp
    
    def put(self,uri,data,content_type='application/json'):
        resp = client.put(uri,data=json.dumps(data), content_type=content_type)
        return resp
    
    def test_create_nsm(self):
        uri = '/loyalty/v1/nsms/'
        resp = self.post(uri,data=NSM)
        self.assertEquals(resp.status_code,201)
        return resp
    
    def test_get_nsm(self):
        resp = self.test_create_nsm()
        self.assertEquals(resp.status_code,201)
        uri = '/loyalty/v1/nsms/1/'
        resp = self.get(uri)
        self.assertEquals(resp.status_code,200)
        self.assertEqual(self.deserialize(resp)['phone_number'], "1234567890")
        return resp
    
    def test_update_nsm(self):
        resp = self.test_get_nsm() 
        self.assertEquals(resp.status_code,200)
        a={"phone_number":"1234512345"}
        uri = '/loyalty/v1/nsms/1/'
        resp = self.put(uri,a)
        self.assertEquals(resp.status_code, 200)
        uri = '/loyalty/v1/nsms/1/'
        resp = self.get(uri)
        self.assertEqual(self.deserialize(resp)['phone_number'], "1234512345")
    
    def test_create_distributor(self):
        uri = '/loyalty/v1/distributors/'
        resp = self.post(uri,data = DISTRIBUTOR)
        self.assertEquals(resp.status_code,201)
        return resp
    
    def test_get_distributor(self):
        resp = self.test_create_distributor()
        self.assertEquals(resp.status_code,201)
        uri = '/loyalty/v1/distributors/1/'
        resp = self.get(uri)
        self.assertEquals(resp.status_code,200)
        self.assertEqual(self.deserialize(resp)['phone_number'], "8951234509")
        self.assertEqual(self.deserialize(resp)['distributor_id'], "15689")
        self.assertEqual(self.deserialize(resp)['name'], "Mrugen")
        self.assertEqual(self.deserialize(resp)['email'], "mrugen@gladminds.co")
        self.assertEqual(self.deserialize(resp)['city'], "bhuj")
        return resp
    
    def test_update_distributor(self):
        resp = self.test_get_distributor()
        self.assertEquals(resp.status_code,200)
        data={"phone_number":"8951234409"}
        uri = '/loyalty/v1/distributors/1/'
        resp = self.put(uri,data)
        self.assertEquals(resp.status_code, 200)
        uri = '/loyalty/v1/distributors/1/'
        resp = self.get(uri)
        self.assertEqual(self.deserialize(resp)['phone_number'], "8951234409")
        
        
        
    
        
    
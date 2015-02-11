#from django.test import TestCase
import json
from django.test.client import Client
from tastypie.test import ResourceTestCase
from test_constants import NSM, ASM,DISTRIBUTOR,RETAILER,SPARE_MASTER, SPARE_POINT
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
        self.assertEqual(self.deserialize(resp)['phone_number'], "9999999999")
        return resp
    
    def test_update_asm(self):
        resp = self.test_get_asm() 
        self.assertEquals(resp.status_code,200)
        a={"phone_number":"9999999998"}
        resp = client.put('/loyalty/v1/asms/1/', data=json.dumps(a), content_type='application/json')
        self.assertEquals(resp.status_code, 200)
        resp = client.get('/loyalty/v1/asms/1/',content_type='application/json')
        self.assertEqual(self.deserialize(resp)['phone_number'], "9999999998")
        
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
        self.assertEqual(self.deserialize(resp)['phone_number'], "1111111111")
        self.assertEqual(self.deserialize(resp)["asm"]['asm_id'],"ASM005")
        self.assertEqual(self.deserialize(resp)["user"]["user"]['username'],"15586")
        
        return resp
    
    def test_update_distributor(self):
        resp = self.test_get_distributor()
        self.assertEquals(resp.status_code,200)
        data={"phone_number":"2222222222"}
        uri = '/loyalty/v1/distributors/1/'
        resp = self.put(uri,data)
        self.assertEquals(resp.status_code, 200)
        uri = '/loyalty/v1/distributors/1/'
        resp = self.get(uri)
        self.assertEqual(self.deserialize(resp)['phone_number'], "2222222222")
    
    def test_create_retailer(self):
        uri = '/loyalty/v1/retailers/'
        resp = self.post(uri,data = RETAILER)
        self.assertEquals(resp.status_code,201)
        return resp
    
    def test_get_retailer(self):
        resp = self.test_create_retailer()
        self.assertEquals(resp.status_code,201)
        uri = '/loyalty/v1/retailers/1/'
        resp = self.get(uri)
        self.assertEquals(resp.status_code,200)
        self.assertEqual(self.deserialize(resp)['retailer_name'], "Ayush")
        self.assertEqual(self.deserialize(resp)['retailer_town'], "devghar")
        return resp
    
    def test_update_retailer(self):
        resp = self.test_get_retailer()
        self.assertEquals(resp.status_code,200)
        data={"retailer_town":"alalpur"}
        uri = '/loyalty/v1/retailers/1/'
        resp = self.put(uri,data)
        self.assertEquals(resp.status_code, 200)
        uri = '/loyalty/v1/retailers/1/'
        resp = self.get(uri)
        self.assertEqual(self.deserialize(resp)['retailer_town'], "alalpur")
    
    def test_create_spare_master(self):
        uri = '/loyalty/v1/spare-master/'
        resp = self.post(uri,data = SPARE_MASTER)
        self.assertEquals(resp.status_code,201)
        return resp
    
    def test_get_spare_master(self):
        resp = self.test_create_spare_master()
        self.assertEquals(resp.status_code,201)
        uri = '/loyalty/v1/spare-master/1/'
        resp = self.get(uri)
        self.assertEquals(resp.status_code,200)
        self.assertEqual(self.deserialize(resp)['part_number'], "11111111")
        self.assertEqual(self.deserialize(resp)["product_type"]['image_url'], "http://test")
        return resp
    
    def test_update_spare_master(self):
        resp = self.test_get_spare_master()
        self.assertEquals(resp.status_code,200)
        data={"part_model":"3S"}
        uri = '/loyalty/v1/spare-master/1/'
        resp = self.put(uri,data)
        self.assertEquals(resp.status_code, 200)
        uri = '/loyalty/v1/spare-master/1/'
        resp = self.get(uri)
        self.assertEqual(self.deserialize(resp)['part_model'], "3S")
    
    def test_create_spare_part_point(self):
        uri = '/loyalty/v1/spare-point/'
        resp = self.post(uri,data = SPARE_POINT)
        self.assertEquals(resp.status_code,201)
        return resp
    
    def test_get_spare_part_point(self):
        resp = self.test_create_spare_part_point()
        self.assertEquals(resp.status_code,201)
        uri = '/loyalty/v1/spare-point/1/'
        resp = self.get(uri)
        self.assertEquals(resp.status_code,200)
        self.assertEqual(self.deserialize(resp)['MRP'], 30)
        self.assertEqual(self.deserialize(resp)["part_number"]['part_number'], "11111111")
        return resp
    
    def test_update_spare_part_point(self):
        resp = self.test_get_spare_part_point()
        self.assertEquals(resp.status_code,200)
        data={"MRP": 31}
        uri = '/loyalty/v1/spare-point/1/'
        resp = self.put(uri,data)
        self.assertEquals(resp.status_code, 200)
        uri = '/loyalty/v1/spare-point/1/'
        resp = self.get(uri)
        self.assertEqual(self.deserialize(resp)['MRP'], 31)
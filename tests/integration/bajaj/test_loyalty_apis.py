#from django.test import TestCase
import json
from django.test.client import Client
from tastypie.test import ResourceTestCase
# from test_constants import NSM, ASM,DISTRIBUTOR,RETAILER,SPARE_MASTER
from test_constants import *
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
        
    def test_create_partner(self):
        uri = '/loyalty/v1/partners/'
        resp = self.post(uri,data=PARTNER)
        self.assertEquals(resp.status_code,201)
        return resp
    
    def test_get_partner(self):
        resp = self.test_create_partner()
        self.assertEquals(resp.status_code,201)
        resp = client.get('/loyalty/v1/partners/1/',content_type='application/json')
        self.assertEquals(resp.status_code,200)
        self.assertEqual(self.deserialize(resp)['name'], "Anchit")
        return resp
    
    def test_update_partner(self):
        resp = self.test_get_partner() 
        self.assertEquals(resp.status_code,200)
        a={"name":"Abhinav"}
        resp = client.put('/loyalty/v1/partners/1/', data=json.dumps(a), content_type='application/json')
        self.assertEquals(resp.status_code, 200)
        resp = client.get('/loyalty/v1/partners/1/',content_type='application/json')
        self.assertEqual(self.deserialize(resp)['name'], "Abhinav")
        
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

    def test_create_product(self):
        uri = '/loyalty/v1/product-catalog/'
        create_mock_data = PRODUCT
        resp = self.post(uri,data=create_mock_data)
        self.assertEquals(resp.status_code,201)
        return resp

    def test_get_product(self):
        resp = self.test_create_product()
        self.assertEquals(resp.status_code,201)
        uri = '/loyalty/v1/product-catalog/1/'
        resp = self.get(uri)
        self.assertEquals(resp.status_code,200)
        self.assertEqual(self.deserialize(resp)['image_url'], None)
        return resp

    def test_update_product(self):
        resp = self.test_get_product()
        self.assertEquals(resp.status_code,200)
        data={"image_url":"qwer/alalpur"}
        uri = '/loyalty/v1/product-catalog/1/'
        resp = self.put(uri,data)
        self.assertEquals(resp.status_code, 200)
        uri = '/loyalty/v1/product-catalog/1/'
        resp = self.get(uri)
        self.assertEqual(self.deserialize(resp)['image_url'], "/media/qwer/alalpur")

    def test_create_redemptiomrequest(self):
        uri = '/loyalty/v1/redemption-request/'
        create_mock_data = REDEMPTION_REQUEST
        resp = self.post(uri,data=create_mock_data)
        self.assertEquals(resp.status_code,201)
        return resp

    def test_get_redemptiomrequest(self):
        resp = self.test_create_redemptiomrequest()
        self.assertEquals(resp.status_code,201)
        uri = '/loyalty/v1/redemption-request/1/'
        resp = self.get(uri)
        self.assertEquals(resp.status_code,200)
        self.assertEqual(self.deserialize(resp)['image_url'], None)
        return resp

    def test_update_redemptiomrequest(self):
        resp = self.test_get_redemptiomrequest()
        self.assertEquals(resp.status_code,200)
        data={"resolution_flag":False}
        uri = '/loyalty/v1/redemption-request/1/'
        resp = self.put(uri,data)
        self.assertEquals(resp.status_code, 200)
        uri = '/loyalty/v1/redemption-request/1/'
        resp = self.get(uri)
        self.assertEqual(self.deserialize(resp)['is_approved'], False)
    
    ''' within sla and overdue test case '''
 
    def test_get_redemptiomrequest_by_overdue(self):
		resp = self.test_create_redemptiomrequest()
		self.assertEquals(resp.status_code,201)
		uri = '/loyalty/v1/redemption-request/1/?resolution_flag=True'
		resp = self.get(uri)
		self.assertEquals(resp.status_code,200)
		self.test_update_redemptiomrequest()
		uri = '/loyalty/v1/redemption-request/1/?resolution_flag=False'
		resp = self.get(uri)
		self.assertEquals(resp.status_code,200)
		
    def test_get_redemptiomrequest_by_state(self):
    	resp = self.test_create_redemptiomrequest()
    	self.assertEquals(resp.status_code,201)
        uri = '/loyalty/v1/redemption-request/1/?member__state=karnataka'
        resp = self.get(uri)
        self.assertEquals(resp.status_code,200)

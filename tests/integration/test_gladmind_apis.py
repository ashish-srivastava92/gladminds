import requests
from django.contrib.auth.models import User
    
from django.test.client import Client
from tastypie.test import ResourceTestCase, TestApiClient
from django.test.testcases import TestCase
import json
from provider.oauth2.models import AccessToken
from provider.oauth2.models import Client as auth_client
client = TestApiClient()
djangoClient=Client()


class GladMindsApiTests(ResourceTestCase):
    
    def setUp(self):
        super(GladMindsApiTests, self).setUp()
        self.access_token = 'testaccesstoken'
        user = User.objects.create_user(username='gladminds', email='gm@gm.com',password='gladminds')
        secret_cli = auth_client(user=user, name='client', client_type=1, url='')
        secret_cli.save()
        access = AccessToken(user=user, token=self.access_token, client=secret_cli)
        access.save()
        self.gm_user = {
                  "customer_name": "test_user",
                  "isActive": True,
                  "phone_number": "1234567890",
                  "user": {
                           "phone_number": "999999999",
                           "user": {
                                    "email": "",
                                    "first_name": "",
                                    "last_name": "",
                                    "username": "ppa",
                                    "password" :"123"
                                    }
                           }
                  }
        
            
        self.gm_products = {
                            "customer_product_number": None,
                            "engine": None,
                            "insurance_loc": None,
                            "insurance_yrs": None,      
                            "invoice_loc": None,        
                            "isActive": True,
                            "order": 0,
                            "product_type": {
                                             "brand": {
                                                          "brand_id": "Bajaaaaj",
                                                          "brand_image_loc": " ",
                                                          "brand_name": "Bajaj",
                                                          "isActive": True
                                                          },
                                             "isActive": True,
                                             "order": 0,
                                             "product_image_loc": None,
                                             "product_name": "3700DHPP",
                                             "product_type": "3700DHPP",                  
                                             "warranty_email": None,                      
                                             "warranty_phone": None                       
                                             },                                              
                            "purchased_from": None,
                            "sap_customer_id": None,    
                            "seller_email": None,       
                            "seller_phone": None,       
                            "veh_reg_no": None,         
                            "vin": 22,                  
                            "warranty_loc": None,       
                            "warranty_yrs": None
                            }
        self.coupons = {
                        "order": 0,
                        "service_type": 2,
                        "status": 1,
                        "unique_service_coupon": "1",
                        "valid_days": 260,
                        "valid_kms": 8000,
                        "vin": {
                                "created_on": "2014-04-25T15:56:34",
                                "invoice_date": "2013-04-06T00:00:00",
                                "isActive": True,               
                                "last_modified": "2014-04-25T15:56:34",
                                "order": 0,                     
                                "product_type": {
                                                 "brand": {
                                                           "brand_id": "Bajaj",
                                                           "brand_image_loc": " ",
                                                           "brand_name": "Bajaj",
                                                           "isActive": True                                           
                                                           },
                                                 "isActive": True,
                                                 "order": 0,
                                                 "product_image_loc": "",
                                                 "product_name": "3700DHFS",
                                                 "product_type": "3700DHFS",
                                                 "product_type_id": 101959
                                                 },
                                "vin": "22"
                                }
                        }                       

    def add_a_gmuser(self):
        uri = '/v1/gmusers/'
        resp = self.api_client.post(uri, format='json', data=self.gm_user)
        return resp
    
    def add_a_product(self):
        uri = '/v1/products/'
        resp = self.api_client.post(uri, format='json', data=self.gm_products)
        return resp
    
    def add_a_coupon(self):
        uri = '/v1/coupons/'
        resp = self.api_client.post(uri, format='json', data=self.coupons)
        return resp

    def test_create_a_gmuser(self):
        resp = self.add_a_gmuser()
        self.assertEquals(resp.status_code,201)

    def test_get_a_particular_gmuser(self):
        resp = self.add_a_gmuser()
        self.assertEquals(resp.status_code,201)
        resp = self.api_client.get('/v1/gmusers/1/', format='json')
        self.assertEquals(resp.status_code,200)
        self.assertEqual(self.deserialize(resp)['phone_number'], "1234567890")
        self.assertEqual(len(self.deserialize(resp)), 19)
    
    def test_update_gmuser(self):
        resp = self.add_a_gmuser()
        self.assertEquals(resp.status_code,201)
        resp = self.api_client.get('/v1/gmusers/1/', format='json')
        self.assertEqual(self.deserialize(resp)['phone_number'], "1234567890")
        resp = self.api_client.put('/v1/gmusers/1/', format='json', data={"phone_number":"1234512345"})
        self.assertEquals(resp.status_code, 200)
        resp = self.api_client.get('/v1/gmusers/1/', format='json')
        self.assertEqual(self.deserialize(resp)['phone_number'], "1234512345")
    
    def test_delete_gmuser(self):
        resp = self.add_a_gmuser()
        self.assertEquals(resp.status_code,201)
        resp = self.api_client.get('/v1/gmusers/', format='json')
        self.assertEquals(resp.status_code,200)
        self.assertEqual(len(self.deserialize(resp)['objects']), 1)
        resp = self.api_client.delete('/v1/gmusers/1/', format='json')
        self.assertEquals(resp.status_code,204)
    
    def test_create_a_product(self):
        resp = self.add_a_product()
        self.assertEquals(resp.status_code,201)

    def test_get_a_particular_product(self):
        resp = self.add_a_product()
        self.assertEquals(resp.status_code,201)
        resp = self.api_client.get('/v1/products/1/', format='json')
        self.assertEquals(resp.status_code,200)
        self.assertEqual(self.deserialize(resp)['vin'], "22")
        self.assertEqual(len(self.deserialize(resp)), 23)
        
    def test_update_a_product(self):
        resp = self.add_a_product()
        self.assertEquals(resp.status_code,201)
        resp = self.api_client.get('/v1/products/1/', format='json')
        self.assertEqual(self.deserialize(resp)['vin'], "22")
        resp = self.api_client.put('/v1/products/1/', format='json', data={"vin":"11"})
        resp = self.api_client.get('/v1/products/1/', format='json')
        self.assertEquals(resp.status_code, 200)
        self.assertEqual(self.deserialize(resp)['vin'], "11")
    
    def test_delete_product(self):
        resp = self.add_a_product()
        self.assertEquals(resp.status_code,201)
        resp = self.api_client.get('/v1/products/', format='json')
        self.assertEquals(resp.status_code,200)
        self.assertEqual(len(self.deserialize(resp)['objects']), 1)
        resp = self.api_client.delete('/v1/products/1/', format='json')
        self.assertEquals(resp.status_code,204)
        
    def test_create_a_coupon(self):
        resp = self.add_a_coupon()
        self.assertEquals(resp.status_code,201)

    def test_get_a_particular_coupon(self):
        resp = self.add_a_coupon()
        self.assertEquals(resp.status_code,201)
        resp = self.api_client.get('/v1/coupons/1/', format='json')
        self.assertEquals(resp.status_code,200)
        self.assertEqual(self.deserialize(resp)['unique_service_coupon'], '1')
        self.assertEqual(len(self.deserialize(resp)), 18)
        
    def test_update_a_coupon(self):
        resp = self.add_a_coupon()
        self.assertEquals(resp.status_code,201)
        resp = self.api_client.get('/v1/coupons/1/', format='json')
        self.assertEqual(self.deserialize(resp)['unique_service_coupon'], '1')
        resp = self.api_client.put('/v1/coupons/1/', format='json', data={"unique_service_coupon":'2'})
        self.assertEquals(resp.status_code, 200)
        resp = self.api_client.get('/v1/coupons/1/', format='json')
        self.assertEquals(resp.status_code, 200)
        self.assertEqual(self.deserialize(resp)['unique_service_coupon'], '2')
    
    def test_delete_coupon(self):
        resp = self.add_a_coupon()
        self.assertEquals(resp.status_code,201)
        resp = self.api_client.get('/v1/coupons/', format='json')
        self.assertEquals(resp.status_code,200)
        self.assertEqual(len(self.deserialize(resp)['objects']), 1)
        resp = self.api_client.delete('/v1/coupons/1/', format='json')
        self.assertEquals(resp.status_code,204)
    

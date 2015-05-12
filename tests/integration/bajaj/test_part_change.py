import json
from django.test.client import Client
from tastypie.test import ResourceTestCase
# from test_constants import 
from gladminds.core.auth_helper import Roles
from gladminds.core.model_fetcher import models
from django.contrib.auth.models import User, Group
from test_constants import BRAND_PRODUCT_RANGE, BRAND_VERTICAL, BOM_HEADER,\
    BOM_PLATE_PART
from integration.bajaj.base import BaseTestCase

client=Client(SERVER_NAME='bajaj')

class PartChangeTests(BaseTestCase):
    multi_db=True
    def setUp(self):
        super(PartChangeTests, self).setUp()

    def post(self, uri, data, access_token=None, content_type='application/json'):
        if access_token:
            uri = uri+'?access_token='+access_token
        resp = client.post(uri, data=json.dumps(data), content_type=content_type)
        return resp

    def get(self, uri, access_token, content_type='application/json'):
        resp = client.get(uri+'&&access_token='+access_token, content_type=content_type)
        return resp
    
    def user_login(self):
        self.create_user(username='user', email='asc@xyz.com', password='123', 
                        phone_number="+911234567890", brand='bajaj')
        data={"username": "user", "password": "123" }
        resp=self.post(uri='/v1/gm-users/login/', data=data)
        return json.loads(resp.content)['access_token']
    
    def test_get_brand_vertical(self):
        access_token = self.user_login()
        uri = '/v1/brand-vertical/'
        resp = self.post(uri, BRAND_VERTICAL, access_token)
        self.assertEquals(resp.status_code, 201)
        uri = '/v1/brand-vertical/?name=vertical2'
        resp = self.get(uri, access_token, content_type='application/json')
        self.assertEquals(resp.status_code, 200)
        
    def test_get_brand_product_range(self):
        access_token = self.user_login()
        uri = '/v1/brand-product-range/'
        resp = self.post(uri, data=BRAND_PRODUCT_RANGE, access_token=access_token)
        self.assertEquals(resp.status_code,201)
        uri = '/v1/brand-product-range/?vertical=vertical2'
        resp = self.get(uri=uri, access_token=access_token)
        self.assertEquals(resp.status_code , 200)
        self.assertEquals(json.loads(resp.content)['objects'][0]['sku_code'], "112")
        uri = '/v1/brand-product-range/?vertical=vertical22'
        resp = self.get(uri=uri, access_token=access_token)
        self.assertEquals(len(json.loads(resp.content)['objects']), 0)
        self.assertEquals(resp.status_code , 200)
    
    def test_get_bom_header(self):
        access_token = self.user_login()
        uri = '/v1/bom-header/'
        resp = self.post(uri, data=BOM_HEADER, access_token=access_token)
        self.assertEquals(resp.status_code, 201)
        uri = '/v1/bom-header/?sku_code=112'
        resp = self.get(uri, access_token)
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(json.loads(resp.content)['objects'][0]['sku_code'], "112")
        self.assertEquals(json.loads(resp.content)['objects'][0]['bom_number'], "1232")
    
    def test_bom_plate_part(self):
        access_token = self.user_login()
        uri = '/v1/bom-plate-part/'
        resp = self.post(uri, data=BOM_PLATE_PART, access_token=access_token)
        self.assertEquals(resp.status_code, 201)
        uri = '/v1/bom-plate-part/?bom__sku_code=112'
        resp = self.get(uri, access_token=access_token)
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(json.loads(resp.content)['objects'][0]['plate']['plate_id'], "212")
        
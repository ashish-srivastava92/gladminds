#from django.test import TestCase
import json
import os
from django.test.client import Client
from django.conf import settings
# from tastypie.test import ResourceTestCase
from test_constants import NATIONAL_SPARES_MANAGER, AREA_SPARES_MANAGER,DISTRIBUTOR,RETAILER,SPARE_MASTER, SPARE_POINT,SPARE_PART_UPC,\
    REDEMPTION_REQUEST,PARTNER,PRODUCT,ACCUMULATION, SPARE_PART_UPC_1,SLA,\
    MEMBER, WELCOMEKIT, COMMENT_THREAD, MEMBER1, TRANSFERPOINTS, TERRITORY,\
    STATE, CITY
from gladminds.core.auth_helper import Roles
from gladminds.core.model_fetcher import models
from gladminds.management.commands import load_gm_migration_data
from integration.core.base_integration import CoreResourceTestCase

client=Client(SERVER_NAME='bajajcv')

class LoyaltyApiTests(CoreResourceTestCase):
    multi_db=True
    def setUp(self):
        super(LoyaltyApiTests, self).setUp()
        self.create_user(username='bajaj', email='bajaj@gmail.com', password='bajaj', 
                        group_name=Roles.SUPERADMINS, brand='bajajcv')
        self.create_user(username='user', email='asc@xyz.com', password='123', 
                        group_name=Roles.LOYALTYSUPERADMINS, phone_number="+911234567890", brand='bajajcv')
        data={"username": "user", "password": "123"}
        self.access_token = self.user_login(data)

    def post(self, uri, data, access_token=None, content_type='application/json'):
        if access_token:
            uri = uri+'?access_token='+self.access_token
        resp = client.post(uri, data=json.dumps(data), content_type=content_type)
        return resp

    def get(self, uri, access_token, content_type='application/json'):
        resp = client.get(uri+'?access_token='+self.access_token, content_type=content_type)
        return resp

    def put(self, uri, access_token, data, content_type='application/json'):
        resp = client.put(uri+'?access_token='+self.access_token, data=json.dumps(data), content_type=content_type)
        return resp

    def create_new_user(self, username, group_name, email):
        user_profile = self.create_user(username=username, email= email, password='123', group_name=group_name, phone_number="+911234567890")
        return user_profile

    def create_nsm(self):
        uri = '/v1/national-spares-managers/'
        resp = self.post(uri,data=NATIONAL_SPARES_MANAGER, access_token=self.access_token)
        return resp
 
    def get_nsm(self):
        uri = '/v1/national-spares-managers/1/'
        resp = self.get(uri, access_token=self.access_token)
        return resp
    
    def update_nsm(self, data):
        uri = '/v1/national-spares-managers/1/'
        resp = self.put(uri, self.access_token, data)
        return resp
    
    def create_asm(self):
        uri = '/v1/area-spares-managers/'
        resp = self.post(uri, data=AREA_SPARES_MANAGER, access_token=self.access_token)
        return resp
    
    def get_asm(self):
        resp = client.get('/v1/area-spares-managers/1/' , access_token=self.access_token, content_type='application/json')
        return resp
    
    def update_asm(self, data):
        resp = self.put('/v1/area-spares-managers/1/', access_token=self.access_token, data=data)
        return resp
    
    def create_member(self, data):
        uri = '/v1/members/'
        resp = self.post(uri,data=data, access_token=self.access_token)
        return resp

    def test_create_nsm(self):
        resp=self.create_nsm()
        self.assertEquals(resp.status_code,201)
 
    def test_get_nsm(self):
        self.create_nsm()
        resp=self.get_nsm()
        self.assertEquals(resp.status_code,200)
        self.assertEqual(self.deserialize(resp)['phone_number'], "1234567890")
 
    def test_update_nsm(self):
        self.create_nsm()
        new_detail={"phone_number":"1234512345"}
        resp=self.update_nsm(new_detail)
        self.assertEquals(resp.status_code, 200)
        resp=self.get_nsm()
        self.assertEqual(self.deserialize(resp)['phone_number'], new_detail['phone_number'])

    def test_create_asm(self):
        resp=self.create_asm()
        self.assertEquals(resp.status_code,201)

    def test_get_asm(self):
        self.create_asm()
        resp=self.get_asm()
        self.assertEquals(resp.status_code,200)
        self.assertEqual(self.deserialize(resp)['phone_number'], "9999999999")

    def test_update_asm(self):
        self.create_asm()
        detail={"phone_number":"9999999998"}
        resp=self.update_asm(detail)
        self.assertEquals(resp.status_code, 200)
        resp=self.get_asm()
        self.assertEquals(resp.status_code, 200)
        self.assertEqual(self.deserialize(resp)['phone_number'], detail['phone_number'])

    def test_create_partner(self, group_name=Roles.AREASPARESMANAGERS):
        uri = '/v1/partners/'
        resp = self.post(uri,data=PARTNER, access_token=self.access_token)
        self.assertEquals(resp.status_code,201)
 
    def test_get_partner(self):
        self.test_create_partner()
        resp = self.get(uri='/v1/partners/1/',access_token=self.access_token)
        self.assertEquals(resp.status_code,200)
        self.assertEqual(self.deserialize(resp)['name'], "Anchit")
 
    def test_update_partner(self):
        self.test_get_partner()
        data={"name":"Abhinav"}
        resp = self.put(uri='/v1/partners/1/', access_token=self.access_token ,data=data)
        self.assertEquals(resp.status_code, 200)
        resp = self.get(uri='/v1/partners/1/', access_token=self.access_token)
        self.assertEqual(self.deserialize(resp)['name'], "Abhinav")

    def test_create_member(self):
        resp=self.create_member(data=MEMBER)
        self.assertEquals(resp.status_code,201)
 
    def test_get_member(self):
        resp=self.create_member(data=MEMBER)
        uri = '/v1/members/1/'
        resp = self.get(uri, access_token=self.access_token)
        self.assertEquals(resp.status_code,200)
        self.assertEqual(self.deserialize(resp)['phone_number'],"+919842461800")
 
    def test_update_member(self):
        resp=self.create_member(data=MEMBER)
        data={"phone_number":"+919842461801"}
        uri = '/v1/members/1/'
        resp = self.put(uri, data=data, access_token=self.access_token)
        self.assertEquals(resp.status_code, 200)
        uri = '/v1/members/1/'
        resp = self.get(uri, self.access_token)
        self.assertEqual(self.deserialize(resp)['phone_number'],"+919842461801")

    def test_create_distributor(self):
        uri = '/v1/distributors/'
        resp = self.post(uri,data=DISTRIBUTOR, access_token=self.access_token)
        self.assertEquals(resp.status_code,201)
 
    def test_get_distributor(self):
        resp = self.test_create_distributor()
        uri = '/v1/distributors/1/'
        resp = self.get(uri, access_token=self.access_token)
        self.assertEquals(resp.status_code,200)
        self.assertEqual(self.deserialize(resp)['phone_number'], "1111111111")
        self.assertEqual(self.deserialize(resp)["asm"]['asm_id'],"ASM005")
        self.assertEqual(self.deserialize(resp)["user"]["user"]['username'],"user")
 
    def test_update_distributor(self):
        resp = self.test_create_distributor()
        data={"phone_number":"2222222222"}
        uri = '/v1/distributors/1/'
        resp = self.put(uri, data=data, access_token=self.access_token)
        self.assertEquals(resp.status_code, 200)
        uri = '/v1/distributors/1/'
        resp = self.get(uri, self.access_token)
        self.assertEqual(self.deserialize(resp)['phone_number'], "2222222222")
 
    def test_create_product(self):
        uri = '/v1/product-catalogs/'
        resp = self.post(uri,data=PRODUCT, access_token=self.access_token)
        self.assertEquals(resp.status_code,201)
 
    def test_get_product(self):
        resp = self.test_create_product()
        uri = '/v1/product-catalogs/1/'
        resp = self.get(uri, access_token=self.access_token)
        self.assertEquals(resp.status_code,200)
        self.assertEqual(self.deserialize(resp)['image_url'], None)
 
    def test_update_product(self):
        resp = self.test_create_product()
        data={"image_url":"qwer/alalpur"}
        uri = '/v1/product-catalogs/1/'
        resp = self.put(uri,data=data, access_token=self.access_token)
        self.assertEquals(resp.status_code, 200)
        uri = '/v1/product-catalogs/1/'
        resp = self.get(uri, access_token=self.access_token)
        self.assertEqual(self.deserialize(resp)['image_url'], "/media/qwer/alalpur")
 
    def test_create_sla(self):
        uri = '/v1/loyalty-slas/'
        resp = self.post(uri,data=SLA, access_token=self.access_token)
        self.assertEquals(resp.status_code,201)
 
    def test_get_sla(self):
        resp = self.test_create_sla()
        uri = '/v1/loyalty-slas/1/'
        resp = self.get(uri, access_token=self.access_token)
        self.assertEquals(resp.status_code,200)
        self.assertEqual(self.deserialize(resp)['action'], "Redemption")
        self.assertEqual(self.deserialize(resp)['resolution_time'], 6)
        self.assertEqual(self.deserialize(resp)['resolution_unit'], "hrs")
 
    def test_update_sla(self):
        resp = self.test_create_sla()
        data={"member_resolution_time": 10}
        uri = '/v1/loyalty-slas/1/'
        resp = self.put(uri,data=data, access_token=self.access_token)
        self.assertEquals(resp.status_code, 200)
        uri = '/v1/loyalty-slas/1/'
        resp = self.get(uri, access_token=self.access_token)
        self.assertEqual(self.deserialize(resp)['member_resolution_time'], 10) 

    def test_create_retailer(self):
        uri = '/v1/retailers/'
        resp = self.post(uri,data = RETAILER, access_token=self.access_token)
        self.assertEquals(resp.status_code,201)
 
    def test_get_retailer(self):
        self.test_create_retailer()
        uri = '/v1/retailers/1/'
        resp = self.get(uri, access_token=self.access_token)
        self.assertEquals(resp.status_code,200)
        self.assertEqual(self.deserialize(resp)['retailer_name'], "Ayush")
        self.assertEqual(self.deserialize(resp)['retailer_town'], "devghar")
        return resp
 
    def test_update_retailer(self):
        self.test_get_retailer()
        data={"retailer_town":"alalpur"}
        uri = '/v1/retailers/1/'
        resp = self.put(uri, self.access_token, data)
        self.assertEquals(resp.status_code, 200)
        uri = '/v1/retailers/1/'
        resp = self.get(uri, access_token=self.access_token)
        self.assertEqual(self.deserialize(resp)['retailer_town'], "alalpur")
 
    def test_create_spare_master(self):
        uri = '/v1/spare-masters/'
        resp = self.post(uri,data = SPARE_MASTER, access_token=self.access_token)
        self.assertEquals(resp.status_code,201)
 
    def test_get_spare_master(self):
        self.test_create_spare_master()
        uri = '/v1/spare-masters/1/'
        resp = self.get(uri, access_token=self.access_token)
        self.assertEquals(resp.status_code,200)
        self.assertEqual(self.deserialize(resp)['part_number'], "11111111")
        self.assertEqual(self.deserialize(resp)["product_type"]['image_url'], "http://test")
        return resp
 
    def test_update_spare_master(self):
        self.test_get_spare_master()
        data={"part_model":"3S"}
        uri = '/v1/spare-masters/1/'
        resp = self.put(uri,self.access_token, data)
        self.assertEquals(resp.status_code, 200)
        uri = '/v1/spare-masters/1/'
        resp = self.get(uri, access_token=self.access_token)
        self.assertEqual(self.deserialize(resp)['part_model'], "3S")
 
    def test_create_spare_part_upc(self):
        self.test_create_spare_master()
        uri = '/v1/spare-upcs/'
        resp = self.post(uri,data = SPARE_PART_UPC, access_token=self.access_token)
        self.assertEquals(resp.status_code,201)
 
    def test_get_spare_part_upc(self):
        self.test_create_spare_part_upc()
        uri = '/v1/spare-upcs/1/'
        resp = self.get(uri, access_token=self.access_token)
        self.assertEquals(resp.status_code,200)
        self.assertEqual(self.deserialize(resp)['unique_part_code'], "UPCC50")
        return resp
 
    def test_update_spare_part_upc(self):
        resp = self.test_get_spare_part_upc()
        self.assertEquals(resp.status_code,200)
        data={"unique_part_code":"UPCC51"}
        uri = '/v1/spare-upcs/1/'
        resp = self.put(uri,self.access_token, data)
        self.assertEquals(resp.status_code, 200)
        uri = '/v1/spare-upcs/1/'
        resp = self.get(uri, access_token=self.access_token)
        self.assertEqual(self.deserialize(resp)['unique_part_code'], "UPCC51")
 
 
    def test_create_spare_part_point(self):
        self.test_create_spare_master()
        uri = '/v1/spare-points/'
        resp = self.post(uri,data = SPARE_POINT, access_token=self.access_token)
        self.assertEquals(resp.status_code,201)
 
    def test_get_spare_part_point(self):
        self.test_create_spare_part_point()
        uri = '/v1/spare-points/1/'
        resp = self.get(uri, access_token=self.access_token)
        self.assertEquals(resp.status_code,200)
        self.assertEqual(self.deserialize(resp)['MRP'], 30)
        self.assertEqual(self.deserialize(resp)["part_number"]['part_number'], "11111111")
        return resp
 
    def test_update_spare_part_point(self):
        self.test_get_spare_part_point()
        data={"MRP": 31}
        uri = '/v1/spare-points/1/'
        resp = self.put(uri,self.access_token, data)
        self.assertEquals(resp.status_code, 200)
        uri = '/v1/spare-points/1/'
        resp = self.get(uri, access_token=self.access_token)
        self.assertEqual(self.deserialize(resp)['MRP'], 31)
 
    def test_create_territory(self,data = TERRITORY):
        uri = '/v1/territories/'
        resp = self.post(uri,data=data, access_token=self.access_token)
        self.assertEquals(resp.status_code,201)

    def test_get_territory(self):
        self.test_create_territory()
        uri = '/v1/territories/1/'
        resp = self.get(uri, access_token=self.access_token)
        self.assertEquals(resp.status_code,200)
        self.assertEqual(self.deserialize(resp)['territory'],'NORTH')

    def test_create_state(self, data=STATE):
        self.test_create_territory()
        uri = '/v1/states/'
        resp = self.post(uri,data=data, access_token=self.access_token)
        self.assertEquals(resp.status_code,201)
        return resp

    def test_get_state(self):
        self.test_create_state()
        uri = '/v1/states/1/'
        resp = self.get(uri, access_token=self.access_token)
        self.assertEquals(resp.status_code,200)
        self.assertEqual(self.deserialize(resp)['state_name'],'Karnataka')

    def test_create_city(self, data=CITY):
        self.test_create_state()
        uri = '/v1/cities/'
        resp = self.post(uri,data=data, access_token=self.access_token)
        self.assertEquals(resp.status_code,201)
        return resp

    def test_get_city(self):
        self.test_create_city()
        uri = '/v1/cities/1/'
        resp = self.get(uri, access_token=self.access_token)
        self.assertEquals(resp.status_code,200)
        self.assertEqual(self.deserialize(resp)['city'],'Bangalore')
        
    def test_transfer_points(self):
        self.test_create_spare_master()
  
        uri = '/v1/spare-points/'
        resp = self.post(uri,data = SPARE_POINT, access_token=self.access_token)
        self.assertEquals(resp.status_code,201)
  
        uri = '/v1/spare-upcs/'
        resp = self.post(uri,data = SPARE_PART_UPC, access_token=self.access_token)
        self.assertEquals(resp.status_code,201)
  
        self.create_member(data=MEMBER)
        self.create_member(data=MEMBER1)
        uri = '/v1/accumulation-discrepancies/transfer-points/'
        resp = client.post(uri, data =TRANSFERPOINTS, access_token=self.access_token)
        self.assertEquals(resp.status_code,200)
  
        uri = '/v1/members/1/'
        resp = self.get(uri, access_token=self.access_token)
        self.assertEqual(self.deserialize(resp)['total_points'],982)
  
        uri = '/v1/members/2/'
        resp = self.get(uri, access_token=self.access_token)
        self.assertEqual(self.deserialize(resp)['total_points'],118)
   
    def post_feed(self, file_path):
        xml_data = open(file_path, 'r').read()
        response = client.post('/api/v1/feed/?wsdl', data=xml_data, content_type='text/xml')
        self.assertEqual(200, response.status_code)

    def send_spare_part_master_feed(self):
        file_path = os.path.join(settings.BASE_DIR, 'tests/integration/bajaj/test_data/part_master_feed.xml')
        self.post_feed(file_path)
        
    def send_spare_part_upc_feed(self):
        file_path = os.path.join(settings.BASE_DIR, 'tests/integration/bajaj/test_data/part_upc_feed.xml')
        self.post_feed(file_path)
        
    def send_spare_part_point_feed(self):
        file_path = os.path.join(settings.BASE_DIR, 'tests/integration/bajaj/test_data/part_point_feed.xml')
        self.post_feed(file_path)
        
    def test_send_accumulation_request(self):
        self.create_member(data=MEMBER)
        self.test_create_sla()
        self.send_spare_part_master_feed()
        self.send_spare_part_upc_feed()
        self.send_spare_part_point_feed()
        uri = '/v1/messages'
        rrmsg = {'text': "AC UPC11", 'phoneNumber': "+919842461800"}
        resp = client.post(uri, rrmsg)
        self.assertEquals(resp.status_code,200)
    
    def test_send_redemption_request(self):
        self.test_create_product()
        self.test_send_accumulation_request()
        uri = '/v1/messages'
        rrmsg = {'text': "RD ME00003 123", 'phoneNumber': "+919842461800"}
        resp = client.post(uri, rrmsg)
        self.assertEquals(resp.status_code,200)


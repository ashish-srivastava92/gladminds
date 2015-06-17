#from django.test import TestCase
import json
from django.test.client import Client
from tastypie.test import ResourceTestCase
from test_constants import NATIONAL_SPARES_MANAGER, AREA_SPARES_MANAGER,DISTRIBUTOR,RETAILER,SPARE_MASTER, SPARE_POINT,SPARE_PART_UPC,\
    REDEMPTION_REQUEST,PARTNER,PRODUCT,ACCUMULATION, SPARE_PART_UPC_1,SLA,\
    MEMBER, WELCOMEKIT, COMMENT_THREAD, MEMBER1, TRANSFERPOINTS, TERRITORY,\
    STATE, CITY
from gladminds.core.auth_helper import Roles
from gladminds.core.model_fetcher import models
from gladminds.management.commands import load_gm_migration_data

client=Client(SERVER_NAME='bajajcv')

class LoyaltyApiTests(ResourceTestCase):
    multi_db=True
    def setUp(self):
        super(LoyaltyApiTests, self).setUp()
        load_obj = load_gm_migration_data.Command()
        load_obj.add_sms_template()

    def post(self, uri, data, access_token=None, content_type='application/json'):
        if access_token:
            uri = uri+'?access_token='+access_token
        resp = client.post(uri, data=json.dumps(data), content_type=content_type)
        return resp

    def get(self, uri, access_token, content_type='application/json'):
        resp = client.get(uri+'?access_token='+access_token, content_type=content_type)
        return resp

    def put(self, uri, access_token, data, content_type='application/json'):
        resp = client.put(uri+'?access_token='+access_token, data=json.dumps(data), content_type=content_type)
        return resp

    def create_new_user(self, username, group_name, email):
        user_profile = self.create_user(username=username, email= email, password='123', group_name=group_name, phone_number="+911234567890")
        return user_profile

    def login(self):
        client.login(username='user', password='123')
        
    ''' function returns access_token after login'''
    def user_login(self, group_name):
        self.create_user(username='user', email='asc@xyz.com', password='123', 
                        group_name=group_name, phone_number="+911234567890", brand='bajajcv')
        data={"username": "user", "password": "123" }
        resp=self.post(uri='/v1/gm-users/login/', data=data)
        return json.loads(resp.content)['access_token']
 
    def test_create_asm(self, data=AREA_SPARES_MANAGER):
        access_token = self.user_login(group_name=Roles.NATIONALSPARESMANAGERS)
        uri = '/v1/area-spares-managers/'
        resp = self.post(uri, data=data, access_token=access_token)
        self.assertEquals(resp.status_code,201)
        return access_token

    def test_get_asm(self):
        access_token = self.test_create_asm()
        resp = client.get('/v1/area-spares-managers/1/' , access_token=access_token, content_type='application/json')
        self.assertEquals(resp.status_code,200)
        self.assertEqual(self.deserialize(resp)['phone_number'], "9999999999")
        return access_token

    def test_update_asm(self):
        access_token = self.test_get_asm()
        a={"phone_number":"9999999998"}
        resp = self.put('/v1/area-spares-managers/1/', access_token=access_token, data=json.dumps(a), content_type='application/json')
        self.assertEquals(resp.status_code, 200)
        resp = self.get('/v1/area-spares-managers/1/',content_type='application/json')
        self.assertEquals(resp.status_code, 200)
        self.assertEqual(self.deserialize(resp)['phone_number'], "9999999998")

    def test_create_nsm(self):
        access_token = self.user_login(group_name=Roles.LOYALTYSUPERADMINS)
        uri = '/v1/national-spares-managers/'
        resp = self.post(uri,data=NATIONAL_SPARES_MANAGER, access_token=access_token)
        self.assertEquals(resp.status_code,201)
        return access_token
 
    def test_get_nsm(self):
        access_token = self.test_create_nsm()
        uri = '/v1/national-spares-managers/1/'
        resp = self.get(uri, access_token=access_token)
        self.assertEquals(resp.status_code,200)
        self.assertEqual(self.deserialize(resp)['phone_number'], "1234567890")
        return access_token
 
    def test_update_nsm(self):
        access_token = self.test_get_asm()
        a={"phone_number":"1234512345"}
        uri = '/v1/national-spares-managers/1/'
        resp = self.put(uri, access_token, a)
        self.assertEquals(resp.status_code, 200)
        uri = '/v1/national-spares-managers/1/'
        resp = self.get(uri, access_token=access_token)
        self.assertEqual(self.deserialize(resp)['phone_number'], "1234512345")

    def test_create_partner(self, group_name=Roles.AREASPARESMANAGERS):
        access_token = self.user_login(group_name=group_name)
        uri = '/v1/partners/'
        resp = self.post(uri,data=PARTNER, access_token=access_token)
        self.assertEquals(resp.status_code,201)
        return resp, access_token
 
    def test_get_partner(self):
        resp = self.test_create_partner()
        access_token = resp[1]
        resp = self.get(uri='/v1/partners/1/',access_token=access_token)
        self.assertEquals(resp.status_code,200)
        self.assertEqual(self.deserialize(resp)['name'], "Anchit")
        return resp, access_token
 
    def test_update_partner(self):
        resp = self.test_get_partner()
        self.assertEquals(resp[0].status_code,200)
        a={"name":"Abhinav"}
        resp = self.put(uri='/v1/partners/1/', access_token=resp[1] ,data=json.dumps(a))
        self.assertEquals(resp.status_code, 200)
        resp = self.get(uri='/v1/partners/1/', access_token=resp[1])
        self.assertEqual(self.deserialize(resp)['name'], "Abhinav")

    def test_create_member(self, access_token, data=MEMBER):
        uri = '/v1/members/'
        resp = self.post(uri,data=data, access_token=access_token)
        self.assertEquals(resp.status_code,201)
        return resp
 
    def test_get_member(self):
        access_token=self.test_create_distributor()
        resp = self.test_create_member(access_token)
        self.assertEquals(resp.status_code,201)
        uri = '/v1/members/1/'
        resp = self.get(uri, access_token=access_token)
        self.assertEquals(resp.status_code,200)
        self.assertEqual(self.deserialize(resp)['phone_number'],"+9198424618001")
        return resp
 
    def test_update_member(self):
        access_token = self.user_login(group_name=Roles.AREASPARESMANAGERS)
        resp = self.test_create_member(access_token)
        self.assertEquals(resp.status_code,201)
        data={"phone_number":"+919842461801"}
        uri = '/v1/members/1/'
        resp = self.put(uri, data=data, access_token=access_token)
        self.assertEquals(resp.status_code, 200)
        uri = '/v1/members/1/'
        resp = self.get(uri, access_token)
        self.assertEqual(self.deserialize(resp)['phone_number'],"+919842461801")

    def test_create_distributor(self):
        access_token = self.user_login(group_name=Roles.AREASPARESMANAGERS)
        uri = '/v1/distributors/'
        resp = self.post(uri,data=DISTRIBUTOR, access_token=access_token)
        self.assertEquals(resp.status_code,201)
        return resp, access_token
 
    def test_get_distributor(self):
        resp = self.test_create_distributor()
        self.assertEquals(resp[0].status_code,201)
        access_token = resp[1]
        uri = '/v1/distributors/1/'
        resp = self.get(uri, access_token=access_token)
        self.assertEquals(resp.status_code,200)
        self.assertEqual(self.deserialize(resp)['phone_number'], "1111111111")
        self.assertEqual(self.deserialize(resp)["asm"]['asm_id'],"ASM005")
        self.assertEqual(self.deserialize(resp)["user"]["user"]['username'],"user")
        return resp
 
    def test_update_distributor(self):
        resp = self.test_get_distributor()
        self.assertEquals(resp.status_code,200)
        data={"phone_number":"2222222222"}
        uri = '/v1/distributors/1/'
        resp = self.put(uri,data)
        self.assertEquals(resp.status_code, 200)
        uri = '/v1/distributors/1/'
        resp = self.get(uri)
        self.assertEqual(self.deserialize(resp)['phone_number'], "2222222222")
 
    def test_create_product(self, access_token):
        uri = '/v1/product-catalogs/'
        resp = self.post(uri,data=PRODUCT, access_token=access_token)
        self.assertEquals(resp.status_code,201)
        return resp
 
    def test_get_product(self):
        access_token = self.user_login(group_name=Roles.AREASPARESMANAGERS)       
        resp = self.test_create_product(access_token=access_token)
        self.assertEquals(resp.status_code,201)
        uri = '/v1/product-catalogs/1/'
        resp = self.get(uri, access_token=access_token)
        self.assertEquals(resp.status_code,200)
        self.assertEqual(self.deserialize(resp)['image_url'], None)
        return resp, access_token
 
    def test_update_product(self):
        resp = self.test_get_product()
        self.assertEquals(resp[0].status_code,200)
        access_token = resp[1]
        data={"image_url":"qwer/alalpur"}
        uri = '/v1/product-catalogs/1/'
        resp = self.put(uri,data=data, access_token=access_token)
        self.assertEquals(resp.status_code, 200)
        uri = '/v1/product-catalogs/1/'
        resp = self.get(uri, access_token=access_token)
        self.assertEqual(self.deserialize(resp)['image_url'], "/media/qwer/alalpur")
 
    def test_create_sla(self, access_token=None):
        if not access_token:
            access_token = self.user_login(group_name=Roles.AREASPARESMANAGERS)
        uri = '/v1/loyalty-slas/'
        resp = self.post(uri,data=SLA, access_token=access_token)
        self.assertEquals(resp.status_code,201)
        return resp
 
    def test_get_sla(self):
        access_token = self.user_login(group_name=Roles.AREASPARESMANAGERS)
        resp = self.test_create_sla(access_token)
        self.assertEquals(resp.status_code,201)
        uri = '/v1/loyalty-slas/1/'
        resp = self.get(uri, access_token=access_token)
        self.assertEquals(resp.status_code,200)
        self.assertEqual(self.deserialize(resp)['action'], "Redemption")
        self.assertEqual(self.deserialize(resp)['resolution_time'], 6)
        self.assertEqual(self.deserialize(resp)['resolution_unit'], "hrs")
        return resp, access_token
 
    def test_update_sla(self):
        resp = self.test_get_sla()
        self.assertEquals(resp[0].status_code,200)
        access_token = resp[1]
        data={"member_resolution_time": 10}
        uri = '/v1/loyalty-slas/1/'
        resp = self.put(uri,data=data, access_token=access_token)
        self.assertEquals(resp.status_code, 200)
        uri = '/v1/loyalty-slas/1/'
        resp = self.get(uri, access_token=access_token)
        self.assertEqual(self.deserialize(resp)['member_resolution_time'], 10)

    def test_create_redemptiomrequest(self):
        
        access_token = self.user_login(group_name=Roles.AREASPARESMANAGERS)
        
        
        resp = self.test_create_member(access_token)
        self.assertEquals(resp.status_code,201)
        
        self.test_create_sla(access_token)
        resp = self.test_create_product(access_token)
        self.assertEquals(resp.status_code,201)
        
        uri = '/v1/messages'
        rrmsg = {'text': "RD ME00003 123", 'phoneNumber': "+919842461800"}
        resp = client.post(uri, rrmsg)
        return resp, access_token
 
    def test_get_redemptiomrequest(self):
        resp = self.test_create_redemptiomrequest()
        self.assertEquals(resp[0].status_code,200)
        access_token=resp[1]
        uri = '/v1/redemption-requests/1/'
        resp = self.get(uri, access_token=access_token)
        self.assertEquals(resp.status_code,200)
        self.assertEqual(self.deserialize(resp)['delivery_address'], '34, SRI MEENAKSHI AMMAN AUTO WORKS, SELLUR')
        return resp
 
    def test_update_redemptiomrequest(self):
        resp = self.test_create_redemptiomrequest()
        self.assertEquals(resp[0].status_code,200)
        access_token = resp[1]
        data={"resolution_flag":False}
        uri = '/v1/redemption-requests/1/'
        resp = self.put(uri,data=data, access_token=access_token)
        self.assertEquals(resp.status_code, 200)
        uri = '/v1/redemption-requests/1/'
        resp = self.get(uri, access_token=access_token)
        self.assertEqual(self.deserialize(resp)['is_approved'], False)

    ''' within sla and overdue test case '''
 
    def test_get_redemptiomrequest_by_overdue(self):
        resp = self.test_create_redemptiomrequest()
        self.assertEquals(resp[0].status_code,200)
        access_token = resp[1]
        
        uri = '/v1/redemption-requests/'
        resp = client.get(uri+'?access_token='+access_token+'&resolution_flag=True', content_type='application/json')
        self.assertEquals(resp.status_code,200)
        
        data={"resolution_flag":False}
        uri = '/v1/redemption-requests/1/'
        resp = self.put(uri,data=data, access_token=access_token)
        
        uri = '/v1/redemption-requests/'
        resp = client.get(uri+'?access_token='+access_token+'&resolution_flag=False', content_type='application/json')
        self.assertEquals(resp.status_code,200)
        
        resp = self.get(uri, access_token=access_token)
        
        self.assertEquals(resp.status_code,200)
 
    def test_get_redemptiomrequest_by_state(self):
        resp = self.test_create_redemptiomrequest()
        self.assertEquals(resp.status_code,201)
        uri = '/v1/redemption-requests/?member__state=karnataka'
        resp = self.get(uri)
        self.assertEquals(resp.status_code,200)
 
    def test_get_mechanic_list(self):
        resp = self.test_create_redemptiomrequest()
        self.assertEquals(resp.status_code,201)
        uri = '/v1/redemption-requests/members-details/open/'
        resp = self.get(uri)
        self.assertEquals(resp.status_code,200)

    def test_create_retailer(self):
        uri = '/v1/retailers/'
        resp = self.post(uri,data = RETAILER)
        self.assertEquals(resp.status_code,201)
        return resp
 
    def test_get_retailer(self):
        resp = self.test_create_retailer()
        self.assertEquals(resp.status_code,201)
        uri = '/v1/retailers/1/'
        resp = self.get(uri)
        self.assertEquals(resp.status_code,200)
        self.assertEqual(self.deserialize(resp)['retailer_name'], "Ayush")
        self.assertEqual(self.deserialize(resp)['retailer_town'], "devghar")
        return resp
 
    def test_update_retailer(self):
        resp = self.test_get_retailer()
        self.assertEquals(resp.status_code,200)
        data={"retailer_town":"alalpur"}
        uri = '/v1/retailers/1/'
        resp = self.put(uri,data)
        self.assertEquals(resp.status_code, 200)
        uri = '/v1/retailers/1/'
        resp = self.get(uri)
        self.assertEqual(self.deserialize(resp)['retailer_town'], "alalpur")
 
    def test_create_spare_master(self):
        uri = '/v1/spare-masters/'
        resp = self.post(uri,data = SPARE_MASTER)
        self.assertEquals(resp.status_code,201)
        return resp
 
    def test_get_spare_master(self):
        resp = self.test_create_spare_master()
        self.assertEquals(resp.status_code,201)
        uri = '/v1/spare-masters/1/'
        resp = self.get(uri)
        self.assertEquals(resp.status_code,200)
        self.assertEqual(self.deserialize(resp)['part_number'], "11111111")
        self.assertEqual(self.deserialize(resp)["product_type"]['image_url'], "http://test")
        return resp
 
    def test_update_spare_master(self):
        resp = self.test_get_spare_master()
        self.assertEquals(resp.status_code,200)
        data={"part_model":"3S"}
        uri = '/v1/spare-masters/1/'
        resp = self.put(uri,data)
        self.assertEquals(resp.status_code, 200)
        uri = '/v1/spare-masters/1/'
        resp = self.get(uri)
        self.assertEqual(self.deserialize(resp)['part_model'], "3S")
 
    def test_create_spare_part_upc(self):
        self.test_create_spare_master()
        uri = '/v1/spare-upcs/'
        resp = self.post(uri,data = SPARE_PART_UPC)
        self.assertEquals(resp.status_code,201)
        return resp
 
    def test_get_spare_part_upc(self):
        resp = self.test_create_spare_part_upc()
        self.assertEquals(resp.status_code,201)
        uri = '/v1/spare-upcs/1/'
        resp = self.get(uri)
        self.assertEquals(resp.status_code,200)
        self.assertEqual(self.deserialize(resp)['unique_part_code'], "UPCC50")
        return resp
 
    def test_update_spare_part_upc(self):
        resp = self.test_get_spare_part_upc()
        self.assertEquals(resp.status_code,200)
        data={"unique_part_code":"UPCC51"}
        uri = '/v1/spare-upcs/1/'
        resp = self.put(uri,data)
        self.assertEquals(resp.status_code, 200)
        uri = '/v1/spare-upcs/1/'
        resp = self.get(uri)
        self.assertEqual(self.deserialize(resp)['unique_part_code'], "UPCC51")
 
 
    def test_create_spare_part_point(self):
        self.test_create_spare_master()
        uri = '/v1/spare-points/'
        resp = self.post(uri,data = SPARE_POINT)
        self.assertEquals(resp.status_code,201)
        return resp
 
    def test_get_spare_part_point(self):
        resp = self.test_create_spare_part_point()
        self.assertEquals(resp.status_code,201)
        uri = '/v1/spare-points/1/'
        resp = self.get(uri)
        self.assertEquals(resp.status_code,200)
        self.assertEqual(self.deserialize(resp)['MRP'], 30)
        self.assertEqual(self.deserialize(resp)["part_number"]['part_number'], "11111111")
        return resp
 
    def test_update_spare_part_point(self):
        resp = self.test_get_spare_part_point()
        self.assertEquals(resp.status_code,200)
        data={"MRP": 31}
        uri = '/v1/spare-points/1/'
        resp = self.put(uri,data)
        self.assertEquals(resp.status_code, 200)
        uri = '/v1/spare-points/1/'
        resp = self.get(uri)
        self.assertEqual(self.deserialize(resp)['MRP'], 31)
    def test_create_accumulation(self):
        uri = '/v1/asms/'
        resp = self.post(uri,data=AREA_SPARES_MANAGER)
        self.assertEquals(resp.status_code,201)
        self.test_create_spare_master()
        uri = '/v1/spare-upcs/'
        resp = self.post(uri,data = SPARE_PART_UPC)
        resp = self.post(uri,data = SPARE_PART_UPC_1)
        self.assertEquals(resp.status_code,201)
        uri = '/v1/accumulations/'
        resp = self.post(uri,data = ACCUMULATION)
        self.assertEquals(resp.status_code,201)
        return resp
 
    def test_get_accumulation(self):
        resp = self.test_create_accumulation()
        self.assertEquals(resp.status_code,201)
        uri = '/v1/accumulations/1/'
        resp = self.get(uri)
        self.assertEquals(resp.status_code,200)
        self.assertEqual(self.deserialize(resp)['transaction_id'], 1)
        return resp
  
    def test_create_welcomekit(self):
        self.test_create_sla()
        self.test_create_member()
        self.test_create_partner()
        uri = '/v1/welcome-kits/'
        resp = self.post(uri,data = WELCOMEKIT)
        self.assertEquals(resp.status_code,201)
        return resp
 
    def test_get_welcomekit(self):
        resp = self.test_create_welcomekit()
        self.assertEquals(resp.status_code,201)
        uri = '/v1/welcome-kits/1/'
        resp = self.get(uri)
        self.assertEquals(resp.status_code,200)
        self.assertEqual(self.deserialize(resp)['status'],"Open")
        return resp
 
    def test_update_welcomekit(self):
        resp = self.test_create_welcomekit()
        self.assertEquals(resp.status_code,201)
        data={"delivery_address":"delhi"}
        uri = '/v1/welcome-kits/1/'
        resp = self.put(uri,data)
        self.assertEquals(resp.status_code, 200)
        uri = '/v1/welcome-kits/1/'
        resp = self.get(uri)
        self.assertEqual(self.deserialize(resp)['delivery_address'],"delhi")
 
    def test_create_commentthread(self):
        self.test_create_welcomekit()
        uri = '/v1/comment-threads/'
        resp = self.post(uri,data = COMMENT_THREAD)
        self.assertEquals(resp.status_code,201)
        return resp
 
    def test_get_commentthread(self):
        resp = self.test_create_commentthread()
        self.assertEquals(resp.status_code,201)
        uri = '/v1/comment-threads/1/'
        resp = self.get(uri)
        self.assertEquals(resp.status_code,200)
        self.assertEqual(self.deserialize(resp)['message'],"Gladminds")
        return resp
 
    def test_update_commentthread(self):
        resp = self.test_create_commentthread()
        self.assertEquals(resp.status_code,201)
        data={"message":"hi"}
        uri = '/v1/comment-threads/1/'
        resp = self.put(uri,data)
        self.assertEquals(resp.status_code, 200)
        uri = '/v1/comment-threads/1/'
        resp = self.get(uri)
        self.assertEqual(self.deserialize(resp)['message'],"hi")
 
    def test_transferpoints(self):
        self.test_create_spare_master()
 
        uri = '/v1/spare-points/'
        resp = self.post(uri,data = SPARE_POINT)
        self.assertEquals(resp.status_code,201)
 
        uri = '/v1/spare-upcs/'
        resp = self.post(uri,data = SPARE_PART_UPC)
        self.assertEquals(resp.status_code,201)
 
        self.test_create_member()
        self.test_create_member(data=MEMBER1)
        uri = '/v1/accumulation-discrepancies/transfer-points/'
        resp = client.post(uri, data =TRANSFERPOINTS)
        self.assertEquals(resp.status_code,200)
 
        uri = '/v1/members/1/'
        resp = self.get(uri)
        self.assertEqual(self.deserialize(resp)['total_points'],982)
 
        uri = '/v1/members/2/'
        resp = self.get(uri)
        self.assertEqual(self.deserialize(resp)['total_points'],118)
 
    def test_asm_redemptionrequest(self):
        data = REDEMPTION_REQUEST
        data['member']= MEMBER1
        self.test_create_redemptiomrequest()
        self.test_create_redemptiomrequest(data=data)
        self.test_create_asm()
        userprofile = self.create_new_user(username='user', group_name=Roles.AREASPARESMANAGERS, email='asc@xyz.com')
        userprofile.state ='karnataka'
        userprofile.save()
 
        up = models.AreaSparesManager.objects.get(email="spremnath@bajajauto.co.in")
        up.user =  userprofile
        up.save()
 
        self.login()
 
        uri = '/v1/redemption-requests/'
        self.get(uri)
 
    def test_rps_redemptionrequest(self):
        self.test_create_redemptiomrequest()
        data = REDEMPTION_REQUEST
        data['is_approved']= True
        self.test_create_redemptiomrequest(data=data)
        self.test_create_partner()
        userprofile = self.create_new_user(username='user', group_name=Roles.RPS, email='rp@xyz.com')
        userprofile.state ='karnataka'
        userprofile.save()
 
        partner = models.Partner.objects.get(name="Anchit")
        partner.user =  userprofile
        partner.save()
 
        self.login()
        uri = '/v1/redemption-requests/'
        resp = self.get(uri)
        self.assertEqual(self.deserialize(resp)['objects'][0]['packed_by'],'user')
 
 
    def test_lps_redemption(self):
 
        uri = '/v1/partners/'
        self.post(uri,data=PARTNER)
        userprofile = self.create_new_user(username='user', group_name=Roles.LPS, email='lp@xyz.com')
        partner = models.Partner.objects.get(name="Anchit")
        partner.user =  userprofile
        partner.save()
 
        self.test_create_redemptiomrequest()
        data = REDEMPTION_REQUEST
        data['status']= 'Shipped'
        self.test_create_redemptiomrequest(data=data)
        redemptionrequest = models.RedemptionRequest.objects.get(status='Shipped')
        redemptionrequest.partner = partner
        redemptionrequest.save()
 
        self.login()
        uri = '/v1/redemption-requests/'
        resp = self.get(uri)
        self.assertEqual(self.deserialize(resp)['objects'][0]['status'],'Shipped')
 
 
    def test_create_territory(self,data = TERRITORY):
        uri = '/v1/territories/'
        resp = self.post(uri,data=data)
        self.assertEquals(resp.status_code,201)
        return resp

    def test_get_territory(self):
        self.test_create_territory()
        uri = '/v1/territories/1/'
        resp = self.get(uri)
        self.assertEquals(resp.status_code,200)
        self.assertEqual(self.deserialize(resp)['territory'],'NORTH')

    def test_create_state(self, data=STATE):
        self.test_create_territory()
        uri = '/v1/states/'
        resp = self.post(uri,data=data)
        self.assertEquals(resp.status_code,201)
        return resp

    def test_get_state(self):
        self.test_create_state()
        uri = '/v1/states/1/'
        resp = self.get(uri)
        self.assertEquals(resp.status_code,200)
        self.assertEqual(self.deserialize(resp)['state_name'],'Karnataka')

    def test_create_city(self, data=CITY):
        self.test_create_state()
        uri = '/v1/cities/'
        resp = self.post(uri,data=data)
        self.assertEquals(resp.status_code,201)
        return resp

    def test_get_city(self):
        self.test_create_city()
        uri = '/v1/cities/1/'
        resp = self.get(uri)
        self.assertEquals(resp.status_code,200)
        self.assertEqual(self.deserialize(resp)['city'],'Bangalore')

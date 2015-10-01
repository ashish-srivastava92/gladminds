import json
import unittest

from django.test.client import Client
from django.test import TestCase
from django.core import mail
from django.conf import settings
from django.test.utils import override_settings

from integration.bajaj.base import BaseTestCase
from integration.bajaj.test_brand_logic import Brand
from integration.bajaj.test_system_logic import System
from test_constants import BRAND_PRODUCT_RANGE, BRAND_VERTICAL, BOM_HEADER, \
    BOM_PLATE_PART, ECO_RELEASE, ECO_IMPLEMENTATION, BOM_VISUALIZATION, \
    SBOM_REVIEW, COMMENTS_FOR_RELEASE_REJECT, CHANGE_STATUS_DATA 

from gladminds.core.auth_helper import Roles

client=Client(SERVER_NAME='bajaj')

class PartChangeTest(BaseTestCase):
    multi_db=True
    def setUp(self):
        TestCase.setUp(self)
        self.brand = Brand(self)
        self.system = System(self)
        BaseTestCase.setUp(self)
        self.create_user(username='bajaj', email='bajaj@gladminds.co', password='bajaj')
        self.create_user(username='epcuser', email='epctest@gladminds.co',
                         password='epcuser', group_name=Roles.VISUALIZATIONUSER)
        self.access_token = self.brand.admin_login()

    def post(self, uri, data, access_token=None, content_type='application/json'):
        if access_token:
            uri = uri+'?access_token='+access_token
        resp = client.post(uri, data=json.dumps(data), content_type=content_type)
        return resp

    def get(self, uri, access_token, data=None, content_type='application/json'):
        if access_token:
            uri = uri+'?access_token='+access_token
        resp = client.get(uri, data=data, content_type=content_type)
        return resp
    
    def user_login(self):
        self.create_user(username='user', email='asc@xyz.com', password='123', 
                        phone_number="+911234567890", brand='bajaj')
        data={"username": "user", "password": "123" }
        resp=self.post(uri='/v1/gm-users/login/', data=data)
        return json.loads(resp.content)['access_token']
    
    def save_bom_header(self, access_token, data):
        uri = '/v1/bom-headers/'
        resp = self.post(uri, data=data, access_token=access_token)
        return resp 
    
    def test_get_brand_vertical(self):
        access_token = self.user_login()
        uri = '/v1/brand-verticals/'
        resp = self.post(uri, BRAND_VERTICAL, access_token)
        self.assertEquals(resp.status_code, 201)
        uri = '/v1/brand-verticals/?name=vertical2'
        resp = self.get(uri, access_token, content_type='application/json')
        self.assertEquals(resp.status_code, 200)
        
    def test_get_brand_product_range(self):
        access_token = self.user_login()
        uri = '/v1/brand-product-range/'
        resp = self.post(uri, data=BRAND_PRODUCT_RANGE, access_token=access_token)
        self.assertEquals(resp.status_code,201)
        uri = '/v1/brand-product-range/'
        resp = self.get(uri=uri, access_token=access_token)
        self.assertEquals(resp.status_code , 200)
        self.assertEquals(json.loads(resp.content)['objects'][0]['sku_code'], "112")
    
    def test_get_bom_header(self):
        access_token = self.user_login()
        uri = '/v1/bom-headers/'
        resp = self.post(uri, data=BOM_HEADER, access_token=access_token)
        self.assertEquals(resp.status_code, 201)
        uri = '/v1/bom-headers/?sku_code=112'
        resp = self.get(uri, access_token)
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(json.loads(resp.content)['objects'][0]['sku_code'], "112")
        self.assertEquals(json.loads(resp.content)['objects'][0]['bom_number'], "1232")
    
    def test_bom_plate_part(self):
        access_token = self.user_login()
        uri = '/v1/bom-plate-parts/'
        resp = self.post(uri, data=BOM_PLATE_PART, access_token=access_token)
        self.assertEquals(resp.status_code, 201)
        uri = '/v1/bom-plate-parts/?bom__sku_code=112'
        resp = self.get(uri, access_token=access_token)
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(json.loads(resp.content)['objects'][0]['plate']['plate_id'], "44")
        
    def test_eco_release(self):
        access_token = self.user_login()
        uri = '/v1/eco-releases/'
        resp = self.post(uri, data=ECO_RELEASE, access_token=access_token)
        self.assertEquals(resp.status_code, 201)
               
        
    def test_eco_implementation(self):
        access_token = self.user_login()
        resp = self.save_bom_header(access_token, BOM_HEADER)
        self.assertEquals(resp.status_code, 201)
        uri = '/v1/eco-releases/'
        resp = self.post(uri, data=ECO_RELEASE, access_token=access_token)
        uri = '/v1/eco-implementations/'
        resp = self.post(uri, data=ECO_IMPLEMENTATION, access_token=access_token)
        self.assertEquals(resp.status_code, 201)
        uri = '/v1/eco-implementations/skucode/112/?access_token='+access_token
        resp = client.get(uri, content_type='application/json')
        self.assertEquals(resp.status_code, 200)
        eco_numbers = json.loads(resp.content)['data']
        self.assertEquals(len(eco_numbers), 1)
        self.assertEquals(eco_numbers[0],ECO_RELEASE["eco_number"])
        
    def test_preview_of_sbom(self):
        access_token = self.user_login()
        brand=self.brand
        brand.populate_upload_history_table(id=1,sku_code=112, bom_number="211760", plateId='44', eco_number='451')
        brand.populate_dependent_table('/v1/eco-implementations/',ECO_IMPLEMENTATION,access_token)
        brand.populate_dependent_table('/v1/bom-visualizations/',BOM_VISUALIZATION,access_token)
        uri = '/v1/bom-visualizations/preview-sbom/1/?access_token='+access_token
        resp = client.get(uri, content_type='application/json')
        self.assertEquals(resp.status_code, 200)
        plate_details = json.loads(resp.content)['plate_part_details']
        self.assertEquals(len(plate_details),1)
        self.assertEquals(plate_details[0]["part_number"],BOM_VISUALIZATION["bom"]["part"]["part_number"])
        
    def test_preview_latest_sbom(self):
        access_token = self.user_login()
        brand=self.brand
        brand.populate_upload_history_table(id=2,sku_code=112, bom_number="211760", plateId='44', eco_number='45')
        brand.populate_dependent_table('/v1/eco-implementations/',ECO_IMPLEMENTATION,access_token)
        brand.populate_dependent_table('/v1/bom-visualizations/',BOM_VISUALIZATION,access_token)
        uri = '/v1/bom-visualizations/preview-sbom/2/?access_token='+access_token       
        resp = client.get(uri, content_type='application/json')
        self.assertEquals(resp.status_code, 200)
        plate_details = json.loads(resp.content)['plate_part_details']
        self.assertEquals(len(plate_details),1)
        self.assertEquals(plate_details[0]["part_number"],BOM_VISUALIZATION["bom"]["part"]["part_number"])
        
    def test_approve_release(self):
        access_token = self.user_login()
        brand=self.brand
        brand.populate_upload_history_table(id=1,sku_code=112, bom_number="211760", plateId='44', eco_number='451')
        brand.populate_dependent_table('/v1/eco-implementations/',ECO_IMPLEMENTATION,access_token)
        brand.populate_dependent_table('/v1/bom-visualizations/',BOM_VISUALIZATION,access_token)
        uri = '/v1/bom-visualizations/change-status/1/'
        resp = self.post(uri, data=CHANGE_STATUS_DATA , access_token=access_token)
        self.assertEquals(resp.status_code, 200)
        release_status = json.loads(resp.content)['status']
        self.assertEquals(release_status,'Approved')
        
    def test_reject_release(self):
        access_token = self.user_login()
        brand=self.brand
        brand.populate_upload_history_table(id=1,sku_code=112, bom_number="211760", plateId='44', eco_number='451')
        brand.populate_dependent_table('/v1/eco-implementations/',ECO_IMPLEMENTATION,access_token)
        brand.populate_dependent_table('/v1/bom-visualizations/',BOM_VISUALIZATION,access_token)
        uri = '/v1/bom-visualizations/change-status/1/'
        resp = self.post(uri, data=COMMENTS_FOR_RELEASE_REJECT, access_token=access_token)
        self.assertEquals(resp.status_code, 200)
        release_status = json.loads(resp.content)['status']
        self.assertEquals(release_status,'Rejected')
        uri = '/v1/bom-visualizations/preview-sbom/1/?access_token='+access_token       
        resp = client.get(uri, content_type='application/json')
        comment = json.loads(resp.content)['comments']
        self.assertEquals(comment[0][0],COMMENTS_FOR_RELEASE_REJECT["comment"])
        
    
    def test_get_pending_sbom(self):
        access_token = self.user_login()
        brand=self.brand
        brand.populate_upload_history_table(id=1,sku_code=112, bom_number="211760", plateId='44', eco_number='451')
        uri = '/v1/visualisation-upload-history/?access_token='+access_token+'&status=Pending'
        resp = client.get(uri, content_type='application/json')
        self.assertEquals(resp.status_code, 200)
        pending_sbom = json.loads(resp.content)['objects'][0]
        self.assertEquals(pending_sbom["status"],'Pending')   
               
    def test_get_plates_image(self):
        access_token = self.user_login()
        uri = '/v1/bom-plate-parts/'
        resp = self.post(uri, data=BOM_PLATE_PART, access_token=access_token)
        self.assertEquals(resp.status_code, 201)
        uri = '/v1/bom-plate-parts/get-plates/?sku_code=112&&bom_number=211760'
        resp = self.get(uri, access_token=access_token)
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(json.loads(resp.content)[0]['plate_id'], "44")

    def test_get_sbom_details(self):
        access_token = self.user_login()
        uri = '/v1/bom-visualizations/'
        resp = self.post(uri, data=BOM_VISUALIZATION, access_token=access_token)
        self.assertEquals(resp.status_code, 201)
        uri = '/v1/bom-plate-parts/?plate__plate_id=44&&bom__bom_number=211760&&bom__sku_code=112'
        resp = self.get(uri, access_token=access_token)
        self.assertEquals(json.loads(resp.content)['objects'][0]['part']['part_number'], "15161069")
        self.assertEquals(resp.status_code, 200)

    def test_review_sbom(self):
        access_token = self.user_login()
        uri = '/v1/bom-visualizations/'
        resp = self.post(uri, data=BOM_VISUALIZATION, access_token=access_token)
        self.assertEquals(resp.status_code, 201)
        uri = '/v1/bom-visualizations/review-sbom/'
        resp = self.post(uri, data=SBOM_REVIEW, access_token=access_token)
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(json.loads(resp.content)['message'], "Success")
        
    @unittest.skip("skip the test mails to be fixed")
    @override_settings(EMAIL_BACKEND='django.core.mail.backends.dummy.EmailBackend')
    def test_sbom_search_by_vin(self):
        access_token = self.access_token
        brand=self.brand
        system=self.system
        brand.send_dispatch_feed()
        brand.send_sbom_data_feed()
#         self.assertEqual(len(mail.outbox), 1)
        response=brand.search_sbom_data(access_token, 'vin', '12345678901232792')
        system.verify_result(input=len(response), output=2)
    
    @unittest.skip("skip the test mails to be fixed")
    def test_sbom_search_by_desc(self):
        access_token = self.access_token
        brand=self.brand
        system=self.system
        brand.send_dispatch_feed()
        brand.send_sbom_data_feed()
#         self.assertEqual(len(mail.outbox), 1)
        response=brand.search_sbom_data(access_token, 'description', 'pulsar')
        sku = filter(lambda sku: sku['sku_code']=='00DH15ZZ', response)
        system.verify_result(input=len(sku), output=1)
        system.verify_result(input=sku[0]['description'], output='PULSAR 150')

    @unittest.skip("skip the test mails to be fixed")
    def test_sbom_search_by_sku(self):
        access_token = self.access_token
        brand=self.brand
        system=self.system
        brand.send_dispatch_feed()
        brand.send_sbom_data_feed()
#         self.assertEqual(len(mail.outbox), 1)
        response=brand.search_sbom_data(access_token, 'sku_code', '00DH15ZZ')
        system.verify_result(input=len(response), output=1)
        system.verify_result(input=response[0]['revision_number'], output=0)

    @unittest.skip("skip the test mails to be fixed")
    def test_sbom_search_by_revision(self):
        access_token = self.access_token
        brand=self.brand
        system=self.system
        brand.send_dispatch_feed()
        brand.send_sbom_data_feed()
#         self.assertEqual(len(mail.outbox), 1)
        response=brand.search_sbom_data(access_token, 'revision', '0')
        system.verify_result(input=len(response), output=3)

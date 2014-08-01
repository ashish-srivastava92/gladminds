''' Test Case for testing out the Afterbuy Api
'''

from integration.base_integration import GladmindsResourceTestCase
from provider.oauth2.models import Client as auth_client
from provider.oauth2.models import AccessToken

from django.contrib.auth.models import User
from django.test.client import Client
from gladminds.models import common

import json
from pydoc import cli

client = Client()


class TestAfterbuy(GladmindsResourceTestCase):

    def setUp(self):
        super(TestAfterbuy, self).setUp()
        self.access_token = 'testaccesstoken'
        user = User.objects.create_user(username='gladminds', email='gm@gm.com', password='gladminds')
        secret_cli = auth_client(user=user, name='client', client_type=1, url='')
        secret_cli.save()
        access = AccessToken(user=user, token=self.access_token, client=secret_cli)
        access.save()
        
    def test_create_new_user(self):
        '''
            Response of Api Status :
                {
                "status": 1, 
                "username": "testuser", 
                "sourceURL": "", 
                "thumbURL": "", 
                "message": "Success!", 
                "id": "GMS176DAE19163F", 
                "unique_id": "GMS176DAE19163F"
                }
        '''
        data = {
            'txtState': 'Uttar Pradesh',
            'txtCountry': 'india',
            'txtMobile': '99999999',
            'txtPassword': 'password',
            'txtEmail': 'email@dsdsdsds.com',
            'txtAddress': 'bangalore',
            'btn_reg_submit': 'submit',
            'txtConfirmPassword': 'password',
            'action': 'newRegister',
            'picImgURL': 'df',
            'profilePIC': '',
            'txtName': 'testuser'
        }
        response = client.post('/afterbuy/', data=data)
        self.assertEqual(response.status_code, 200)
        
    def test_check_login(self):
        self.test_create_new_user()
        data = { 
                    'action': 'checkLogin',
                    'txtPassword': 'password',
                    'txtUsername': 'testuser'
                }
        response = client.post(
            '/afterbuy/', data=data)
        self.assertEqual(response.status_code, 200)
        
    def test_product_details(self):
        response = client.get('/afterbuy/', data={'action': 'getProducts'})
        self.assertEqual(response.status_code, 200)

    def test_create_item(self):
        response = client.get('/afterbuy/', data={'action': 'addingItem'})
        self.assertEqual(response.status_code, 200)
        
    def test_generating_OTP(self):
        data = {"mobile":"99999999"}
        response = client.post("/afterbuy/otp/generate/", data=data)
        deserialize_resp = self.deserialize(response)
        self.assertEqual('OTP sent to mobile 99999999', deserialize_resp['message'])
        self.assertEqual(200, response.status_code)
        
    def test_notification_count_of_user(self):
        data = {"mobile":"99999999"}
        resp = client.post("/afterbuy/otp/generate/", data=data)
        response = client.get('/v1/afterbuy/notification/count/?mobile=99999999')
        resp_content = json.loads(response.content)
        self.assertEqual(resp_content['count'], 0)
        self.assertEqual(response.status_code, 200)

    def test_notification_list_of_user(self):
        data = {"mobile":"99999999"}
        resp = client.post("/afterbuy/otp/generate/", data=data)
        response = client.get('/v1/afterbuy/notification/list/?mobile=99999999')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, "No notification exists.")

           
    def test_get_product_insurance(self):
        self.test_create_new_user()
        testUser = User.objects.get(username='testuser')
        user = common.GladMindUsers.objects.get(user=testUser)
        testProductData = common.ProductData(vin="aaaaaaaa", customer_phone_number=user)
        testProductData.save()
        testProductInsuranceInfo = common.ProductInsuranceInfo(product=testProductData, issue_date='2014-07-28', expiry_date='2014-07-28', insurance_phone='1111111111')
        testProductInsuranceInfo.save()
        response = client.get('/v1/afterbuy/product/insurance/?vin=aaaaaaaa')
        self.assertEqual(response.status_code, 200)
        response = client.get('/v1/afterbuy/product/insurance/?vin=')
        self.assertEqual(response.status_code, 400)
    
    def test_get_product_warranty(self):
        self.test_create_new_user()
        testUser = User.objects.get(username='testuser')
        user = common.GladMindUsers.objects.get(user=testUser)        
        testBrand = common.BrandData(brand_id='1', brand_name="test_brand")
        testBrand.save()
        brands = common.BrandData.objects.get(brand_name="test_brand")        
        testProductType = common.ProductTypeData(brand_id=brands, product_name="Test", warranty_email="abc@def.com", warranty_phone="88888888")
        testProductType.save()        
        testProductType = common.ProductTypeData.objects.get(brand_id=brands)        
        testProductData = common.ProductData(vin="aaaaaaaa", customer_phone_number=user, product_type=testProductType)
        testProductData.save()        
        testProductWarranty = common.ProductWarrantyInfo(product=testProductData, issue_date='2014-07-28', expiry_date='2014-07-28')
        testProductWarranty.save()
        response = client.get('/v1/afterbuy/product/warranty/?vin=aaaaaaaa')
        self.assertEqual(response.status_code, 200)
        response = client.get('/v1/afterbuy/product/warranty/?vin=')
        self.assertEqual(response.status_code,400)

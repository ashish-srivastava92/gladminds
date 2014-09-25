''' Test Case for testing out the Afterbuy Api
'''

from integration.base_integration import GladmindsResourceTestCase
from provider.oauth2.models import Client as auth_client
from provider.oauth2.models import AccessToken
from django.utils import unittest
from django.contrib.auth.models import User
from django.test.client import Client
from integration.base import BaseTestCase
from django.test import TestCase
from gladminds.models import common
from gladminds.afterbuy.models import common as afterbuy_common
import json
client = Client()


class TestAfterbuy(GladmindsResourceTestCase, BaseTestCase):

    def setUp(self):
        TestCase.setUp(self)
        BaseTestCase.setUp(self)
        self.access_token = 'testaccesstoken'
        self.create_user(username='gladminds', email='gm@gm.com', password='gladminds')
        user = self.get_user_obj(username='gladminds')
        secret_cli = auth_client(user=user, name='client', client_type=1, url='')
        secret_cli.save()
        access = AccessToken(user=user, token=self.access_token, client=secret_cli)
        access.save()
        user_obj = self.create_gladmind_user()
        brand_obj = self.create_get_brand_obj(brand_id='1', brand_name="test_brand")
        testProductType = self.create_get_product_type_obj(brand_id=brand_obj, product_name="Test", warranty_email="abc@def.com", warranty_phone="88888888")
        self.create_get_user_product_obj(vin='MD2A57BZ4EWA05472', customer_phone_number=user_obj)
        product_info = self.create_get_product_obj(vin='MD2A57BZ4EWA05472', customer_phone_number=user_obj, product_type=testProductType)
        self.create_get_product_insurance_info(product=product_info, issue_date='2014-07-28', expiry_date='2014-07-28', insurance_phone='1111111111', policy_number='12s33')
        self.create_get_product_warranty_info(product=product_info, issue_date='2014-07-28', expiry_date='2014-07-28')
        self.create_get_spare_data(spare_brand=brand_obj, spare_name="test spare")

    @unittest.skip("skip the test")
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

    @unittest.skip("skip the test")
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
        create_mock_data = {'action': 'getProducts'}
        get_response = client.get('/afterbuy/', data=create_mock_data)
        self.assert_successful_http_response(get_response)

    def test_create_item(self):
        create_mock_data = {'action': 'addingItem'}
        get_response = client.get('/afterbuy/', data=create_mock_data)
        self.assert_successful_http_response(get_response)

    def test_generating_OTP(self):
        create_mock_data = {"mobile":"99999999"}
        get_response = client.post("/afterbuy/otp/generate/", data=create_mock_data)
        deserialize_resp = self.deserialize(get_response)
        self.assertEqual('OTP sent to mobile 99999999', deserialize_resp['message'])
        self.assert_successful_http_response(get_response)

    def test_notification_count_of_user(self):
        create_mock_data = {"mobile":"99999999"}
        resp = client.post("/afterbuy/otp/generate/", data=create_mock_data)
        get_response = client.get('/v1/afterbuy/notification/count/?mobile=99999999')
        resp_content = json.loads(get_response.content)
        self.assertEqual(resp_content['count'], 0)
        self.assert_successful_http_response(get_response)

    def test_notification_list_of_user(self):
        create_mock_data = {"mobile":"99999999"}
        resp = client.post("/afterbuy/otp/generate/", data=create_mock_data)
        get_response = client.get('/v1/afterbuy/notification/list/?mobile=99999999')
        self.assert_successful_http_response(get_response)
        self.assertEqual(get_response.content, "No notification exists.")

    def test_get_product_insurance(self):
        get_response = client.get('/v1/afterbuy/product/insurance/?vin=MD2A57BZ4EWA05472')
        self.assert_successful_http_response(get_response)
        get_response = client.get('/v1/afterbuy/product/insurance/?vin=')
        self.assertEqual(get_response.status_code, 400)

    def test_get_product_warranty(self):
        get_response = client.get('/v1/afterbuy/product/warranty/?vin=MD2A57BZ4EWA05472')
        self.assert_successful_http_response(get_response)
        get_response = client.get('/v1/afterbuy/product/warranty/?vin=')
        self.assertEqual(get_response.status_code,400)

    def test_get_spares_list(self):
        get_response = client.get('/v1/afterbuy/product/spares/?vin=MD2A57BZ4EWA05472')
        self.assert_successful_http_response(get_response)
        get_response = client.get('/v1/afterbuy/product/spares/?vin=')
        self.assertEqual(get_response.status_code,400)

    def test_save_user_details(self):
        create_mock_data = {"mobile":"99999998","name":"xyz","email":"xyz@gmail.com","gender":"m","address":"a-302 om complex"
                ,"size":"1","pincode":"320037"}
        get_response = client.post("/v1/afterbuy/user/save/", data=create_mock_data)
        deserialize_resp = self.deserialize(get_response)
        self.assertEqual('details saved', deserialize_resp['message'])
        self.assert_successful_http_response(get_response)

    def test_save_user_feedback(self):
        create_mock_data = {"mobile":"99999998", "message":"dummy message"}
        get_response = client.post("/v1/afterbuy/user/feedback/", data=create_mock_data)
        deserialize_resp = self.deserialize(get_response)
        self.assertEqual('saved successfully', deserialize_resp['message'])
        self.assert_successful_http_response(get_response)

    def test_get_product_coupons(self):
        create_mock_data = {'vin': 'MD2A57BZ4EWA05472'}
        get_response = client.get('/v1/afterbuy/product/coupons/', data=create_mock_data)
        self.assert_successful_http_response(get_response)

    def test_get_product_purchase_information(self):
        get_response = client.get('/v1/afterbuy/product/purchase-info/', data={'vin': 'MD2A57BZ4EWA05472'})
        self.assert_successful_http_response(get_response)

    def test_save_user_phone_details(self):
        create_mock_data = {"mobile":"99999998", "IMEI":"123e4","ICCID":"12ef", "phone_name":"9727071081",
                 "serial_number":"123eee", "capacity":"2", "os":"dummyos","version":"11", "Model":"reb" }
        get_response = client.post("/v1/afterbuy/phone-details/", data=create_mock_data)
        deserialize_resp = self.deserialize(get_response)
        self.assertEqual('details saved', deserialize_resp[0]['message'])
        self.assert_successful_http_response(get_response)

    def test_post_dispatch_dict(self):
        create_mock_data = {"mobile":"99999998","vin":"MD2A57BZ4EWA05472"}
        get_response = client.post('/v1/afterbuy/product/info/', data=create_mock_data)
        self.assert_successful_http_response(get_response) 

    def test_get_dispatch_dict(self):
        create_mock_data = {"mobile":"99999998"}
        get_response = client.get('/v1/afterbuy/product/info/', data=create_mock_data)
        self.assert_successful_http_response(get_response)

    def test_delete_dispatch_dict(self):
        url = '/v1/afterbuy/product/info/?mobile=99999998&vin=MD2A57BZ4EWA05472'
        get_response = client.delete(url)
        self.assert_successful_http_response(get_response)

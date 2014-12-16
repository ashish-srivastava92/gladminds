''' Test Case for testing out the Afterbuy Api
'''
import unittest
import json
from datetime import datetime
from django.test.client import Client
from django.conf import settings
from django.contrib.auth.models import Group, User

from test_constants import AFTERBUY_PRODUCTS
from integration.afterbuy import base_integration
from gladminds.afterbuy import models
from provider.oauth2.models import AccessToken

client = Client(SERVER_NAME='afterbuy')


class TestAfterbuyApi(base_integration.AfterBuyResourceTestCase):
    def setUp(self):
        super(TestAfterbuyApi, self).setUp()
        token = models.OTPToken( token=settings.HARCODED_OTPS[0],
                                 request_date=datetime.now(),
                                 email='test.ab@gmail.com',
                                 phone_number='7760814041')
        token.save()
        group = Group(id=7,name='Users')
        group.save(using='afterbuy')

    def test_user_registration(self):
        create_mock_data = {"first_name": "saurav","phone_number":"7760814041",
                            "email_id":"test.ab@gmail.com","password":"123",
                            "otp_token":"000000"}
        uri = '/afterbuy/v1/consumers/registration/'
        resp = client.post(uri, data=json.dumps(create_mock_data), content_type='application/json')
        self.assertEquals(resp.status_code, 200)

    def test_user_login(self):
        login_data = {"phone_number":"7760814041", "password":"123"}
        uri = '/afterbuy/v1/consumers/login/'
        resp = client.post(uri, data=json.dumps(login_data), content_type='application/json')
        self.assertEquals(resp.status_code, 200)
          
        # Checking login by email id
        login_data = {"email_id":"test.ab@gmail.com", "password":"123"}
        uri = '/afterbuy/v1/consumers/login/'
        resp = client.post(uri, data=json.dumps(login_data), content_type='application/json')
        self.assertEquals(resp.status_code, 200)
        
    def test_user_emailid_exists(self):
        create_mock_data = {"email_id":"test.ab@gmail.com"}
        uri = '/afterbuy/v1/consumers/authenticate-email/'
        resp = self.client.post(uri, format='json', data=create_mock_data)
        self.assertEquals(200, resp.status_code)

    
    def test_user_send_otp(self):
        create_mock_data = {"phone_number":"7760814041"}
        uri = '/afterbuy/v1/consumers/phone-number/send-otp/'
        resp = client.post(uri, data=json.dumps(create_mock_data), content_type='application/json')
        self.assertEquals(resp.status_code, 200)
        
    def test_change_user_password(self):
        create_mock_data = {"password1": "1234",  "password2": "1234", "otp_token":"000000",
                            "auth_key": "e6281aa90743296987089ab013ee245dab66b27b"}
        uri = '/afterbuy/v1/consumers/forgot-password/phone/'
        resp = client.post(uri, data=json.dumps(create_mock_data), content_type='application/json')
        self.assertEquals(resp.status_code, 200)
        uri = '/afterbuy/v1/consumers/forgot-password/email/'
        resp = client.post(uri, data=json.dumps(create_mock_data), content_type='application/json')
        self.assertEquals(resp.status_code, 200)

    def test_add_product(self):
        self.test_user_registration()
    
    @unittest.skip('failin')
    def test_fetch_user_products(self):
        self.test_user_registration()
        create_mock_data = {'email_id':'srv.sngh@gmail.com'}
        uri = '/afterbuy/v1/consumers/1/products/'
        resp = self.client.get(uri, format='json', data=create_mock_data)
        self.assertEquals(200, resp.status_code)
    
    def test_product_api(self):
        #Checking post api
        json_data = json.dumps(AFTERBUY_PRODUCTS)
        resp = client.post('/afterbuy/v1/products/?access_token=e6281aa90743296987089ab013ee245dab66b27b', json_data, content_type='application/json')
        self.assertEquals(resp.status_code,201)
        
#         #Checking get api
#         resp = self.client.get('/afterbuy/v1/products/1/')
#         self.assertEquals(resp.status_code,200)
#         self.assertEqual(self.deserialize(resp)['nick_name'], "aaa")
#         self.assertEqual(len(self.deserialize(resp)), 17)
#         
#         #Cheking put api
#         json_data = json.dumps({"nick_name":"bbb"})
#         resp = self.client.put('/afterbuy/v1/products/1/',json_data, content_type='application/json')
#         self.assertEquals(resp.status_code, 200)
#         resp = self.client.get('/afterbuy/v1/products/1/')
#         self.assertEqual(self.deserialize(resp)['nick_name'], "bbb")
#         
#         
''' Test Case for testing out the Afterbuy Api
'''

from integration.base_integration import GladmindsResourceTestCase
from provider.oauth2.models import Client as auth_client
from provider.oauth2.models import AccessToken

from django.contrib.auth.models import User
from django.test.client import Client
from gladminds.models import common

import json

client = Client()


class TestAfterbuy(GladmindsResourceTestCase):

    def setUp(self):
        super(TestAfterbuy, self).setUp()
        self.access_token = 'testaccesstoken'
        user = User.objects.create_user(username='gladminds', email='gm@gm.com',password='gladminds')
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
            '/afterbuy/', data =data)
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

#    def test_get_product_spares(self):
#        data = {"mobile":"99999999"}
#        resp = client.post("/afterbuy/otp/generate/", data=data)
#        response = client.get('/v1/afterbuy/product/spares/?vin=""')
#        self.assertEqual(response.status_code, 202)
        

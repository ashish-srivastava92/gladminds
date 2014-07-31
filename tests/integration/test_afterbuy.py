''' Test Case for testing out the Afterbuy Api
'''

from integration.base_integration import GladmindsResourceTestCase
from provider.oauth2.models import Client as auth_client
from provider.oauth2.models import AccessToken

from django.contrib.auth.models import User
from django.test.client import Client
from gladminds.models import common
from gladminds.afterbuy.models import common as afterbuy_common
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
    
    def test_save_user_details(self):
        data = {"mobile":"99999999","name":"xyz","email":"xyz@gmail.com","gender":"m","address":"ccccc","size":"1","pincode":"320037"}
        user_info = common.GladMindUsers(phone_number='+9199999999')
        user_info.save()
        response = client.post("/v1/afterbuy/user/save/", data=data)
        deserialize_resp = self.deserialize(response)
        self.assertEqual('details saved', deserialize_resp['message'])
        self.assertEqual(200, response.status_code) 
           
    def test_save_user_feedback(self):
        data = {"mobile":"99999999","feedback_type":"xyz","message":"dfdfdfdf"}
        user_info = common.GladMindUsers(phone_number='+9199999999')
        user_info.save()
        response = client.post("/v1/afterbuy/user/feedback/", data=data)
        deserialize_resp = self.deserialize(response)
        self.assertEqual('saved successfully', deserialize_resp['message'])
        self.assertEqual(200, response.status_code)  
        
    def test_get_product_coupons(self):
        product_info = common.ProductData(vin = 'MD2A57BZ4EWA05472')
        product_info.save()
        response = client.get('/v1/afterbuy/product/coupons/', data={'vin': 'MD2A57BZ4EWA05472'})
        self.assertEqual(response.status_code, 200)  
     
    def test_get_product_purchase_information(self):
        product_info = common.ProductData(vin = 'MD2A57BZ4EWA05472')
        product_info.save()
        response = client.get('/v1/afterbuy/product/purchase-info/', data={'vin': 'MD2A57BZ4EWA05472'})
        self.assertEqual(response.status_code, 200)  
               
                 
    def test_save_user_phone_details(self):
        data = {"mobile":"99999999", "IMEI":"sdsdsdsd","ICCID":"ffdfdfd", "phone_name":"sjxbsjx", "serial_number":"bdj2e2e2e2", "capacity":"2", "os":"sss","version":"11", "Model":"ww" }
        user_info = common.GladMindUsers(phone_number='+9199999999')
        user_info.save()
        response = client.post("/v1/afterbuy/phone-details/", data=data)
        deserialize_resp = self.deserialize(response)
        self.assertEqual('details saved', deserialize_resp[0]['message'])
        self.assertEqual(200, response.status_code)
        
        
    def test_post_dispatch_dict(self):
        data={"mobile":"99999999","vin":"MD2A57BZ4EWA05472"}
        user_info = common.GladMindUsers(phone_number='+9199999999')
        user_info.save()
        aa = common.GladMindUsers.objects.filter(phone_number='+9199999999')
        product_info = afterbuy_common.UserProducts(vin = 'MD2A57BZ4EWA05472',customer_phone_number=aa[0])
        product_info.save()
        response = client.post('/v1/afterbuy/product/info/', data=data)
        self.assertEqual(response.status_code, 200) 
        
    def test_get_dispatch_dict(self):
        data={"mobile":"99999999"}
        user_info = common.GladMindUsers(phone_number='+9199999999')
        user_info.save()
        response = client.get('/v1/afterbuy/product/info/', data=data)
        self.assertEqual(response.status_code, 200)                             
             
    def test_delete_dispatch_dict(self):
        user_info = common.GladMindUsers(phone_number='+9199999999')
        user_info.save()
        aa = common.GladMindUsers.objects.filter(phone_number='+9199999999')
        product_info = afterbuy_common.UserProducts(vin = '123465656556',customer_phone_number=aa[0])
        product_info.save()
        url = '/v1/afterbuy/product/info/?mobile=99999999&vin=123465656556' 
        response = client.delete(url)
        self.assertEqual(response.status_code, 200)                       
                      
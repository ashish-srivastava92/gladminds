''' Test Case for testing out the Afterbuy Api
'''
import unittest
import json
from datetime import datetime
from django.test.client import Client
from django.conf import settings
from django.contrib.auth.models import Group, User, Permission
from test_constants import *
from integration.afterbuy import base_integration
from gladminds.afterbuy import models
from gladminds.core.auth_helper import GmApps, Roles
from integration.bajaj.test_feeds import FeedsResourceTest
from integration.bajaj.test_brand_logic import Brand
from integration.bajaj.base import BaseTestCase
# from integration.bajaj.test_feeds import FeedsResourceTest

client = Client(SERVER_NAME='afterbuy')
client1 = Client(SERVER_NAME='bajaj')

class TestAfterbuyApi(base_integration.AfterBuyResourceTestCase, BaseTestCase):
    multi_db = True 
    def setUp(self):
        super(TestAfterbuyApi, self).setUp()
        token = models.OTPToken(token=settings.HARCODED_OTPS[0],
                                 request_date=datetime.now(),
                                 email='test.ab@gmail.com',
                                 phone_number='7760814041')
        token.save()
        if not Group.objects.using(GmApps.AFTERBUY).filter(name=Roles.USERS).exists():
            Group(name=Roles.USERS).save(using=GmApps.AFTERBUY)
            permissions = Permission.objects.using(GmApps.AFTERBUY)
            group = Group.objects.using(GmApps.AFTERBUY).get(name=Roles.USERS)
            for permission in permissions:
                group.permissions.add(permission)

        self.create_afterbuy_user()
        self.request_headers_afterbuy = {'HTTP_HOST' :'local.api.afterbuy.co:8000'}
        self.request_headers_bajaj = {'HTTP_HOST' :'local.bajaj.gladminds.co:8000'}
    
    def user_login(self):
        login_details = self.login()
        access_token = json.loads(login_details.content)['access_token']
        return access_token

    def test_user_registration(self):

        create_mock_data = {"phone_number":"1111111111",
                            }
        uri = '/afterbuy/v1/consumers/registration/phone'
        resp = client.post(uri, data=json.dumps(create_mock_data), content_type='application/json')
        self.assertEquals(json.loads(resp.content)['status'], 200)
        create_mock_data = {"phone_number":"1111111111",
                            }
        uri = '/afterbuy/v1/consumers/registration/phone'
        resp = client.post(uri, data=json.dumps(create_mock_data), content_type='application/json')
        self.assertEquals(json.loads(resp.content)['status_code'], 200)
    
    def test_validate_otp(self):
        self.test_user_registration()
        uri = '/afterbuy/v1/consumers/validate-otp/'
        mock_data = {"otp_token": "000000"}
        resp = self.post(uri, content_type='application/json', data=mock_data)
        self.assertEquals(json.loads(resp.content)['status'], 200)

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
        create_mock_data = {"password1": "aA1234@", "password2": "aA1234@", "otp_token":"000000",
                            "auth_key": "e6281aa90743296987089ab013ee245dab66b27b"}
        uri = '/afterbuy/v1/consumers/forgot-password/phone/'
        resp = client.post(uri, data=json.dumps(create_mock_data), content_type='application/json')
        self.assertEquals(resp.status_code, 200)
        uri = '/afterbuy/v1/consumers/forgot-password/email/'
        resp = client.post(uri, data=json.dumps(create_mock_data), content_type='application/json')
        self.assertEquals(resp.status_code, 200)

    def test_product_api(self):
        resp = self.post('/afterbuy/v1/products/', data=AFTERBUY_PRODUCT)
        self.assertEquals(json.loads(resp.content)['consumers']['phone_number'], [u'You cannot update phone number'])

        resp = self.post('/afterbuy/v1/products/', data=AFTERBUY_PRODUCTS)
        self.assertEquals(json.loads(resp.content)['brand_product_id'],'zxcvbnm')
        self.assertEquals(resp.status_code, 201)

    def test_get_brand_details(self):
        access_token = self.user_login()
        resp = client.post('/afterbuy/v1/products/?access_token=' + access_token, data=json.dumps(AFTERBUY_PRODUCTS),
                           content_type='application/json')
        self.assertEquals(resp.status_code, 201)
        resp = client.get('/afterbuy/v1/products/get-brands/?access_token=' + access_token)
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(json.loads(resp.content)['status_code'], 200)

    @unittest.skip("skip the test")
    def test_user_product_acceptance(self):
        access_token = self.user_login()
        uri = '/afterbuy/v1/products/?access_token=' + access_token
 
        resp = client.post(uri, data=json.dumps(AFTERBUY_PRODUCTS), content_type='application/json')
        self.assertEquals(resp.status_code, 201)
        mock_data = {'product_id':"zxcvbnm", 'is_accepted': 1}
        resp = client.post('/afterbuy/v1/products/accept-product/?access_token=' + access_token,
                           data=json.dumps(mock_data), content_type='application/json')
        self.assertEquals(json.loads(resp.content)['status'], 200)
        self.assertEquals(resp.status_code, 200)
    
    def test_insurances_api(self):
        resp = self.post('/afterbuy/v1/insurances/', data=AFTERBUY_INSURANCES)
        self.assertEquals(resp.status_code, 201)
        self.assertEquals(json.loads(resp.content)['agency_contact'], 'bajaj')

    def test_invoices_api(self):
        resp = self.post('/afterbuy/v1/invoices/', data=AFTERBUY_INVOICES)
        self.assertEquals(resp.status_code, 201)
        self.assertEquals(json.loads(resp.content)['invoice_number'], '123456')

    def test_licenses_api(self):
        resp = self.post('/afterbuy/v1/licenses/', data=AFTERBUY_LICENCES)
        self.assertEquals(resp.status_code, 201)
        self.assertEquals(json.loads(resp.content)['license_number'], '12345')

    def test_pollution_api(self):
        resp = self.post('/afterbuy/v1/pollution/', data=AFTERBUY_POLLUTION)
        self.assertEquals(resp.status_code, 201)
        self.assertEquals(json.loads(resp.content)['pucc_number'], '123')

    def test_product_support_api(self):
        resp = self.post('/afterbuy/v1/product-support/', data=AFTERBUY_PRODUCTSUPPORT)
        self.assertEquals(resp.status_code, 201)
        self.assertEquals(json.loads(resp.content)['contact'], '1234567890')

    def test_sell_information_api(self):
        resp = self.post('/afterbuy/v1/sell-information/', data=AFTERBUY_SELLINFORMATION)
        self.assertEquals(resp.status_code, 201)
        self.assertEquals(json.loads(resp.content)['id'], 1)

    def test_product_imagesn_api(self):
        resp = self.post('/afterbuy/v1/product-images/', data=AFTERBUY_USERPRODUCTIMAGES)
        self.assertEquals(resp.status_code, 201)
        self.assertEquals(json.loads(resp.content)['image_url'], 'aaa')

    def test_registrations_api(self):
        resp = self.post('/afterbuy/v1/registrations/', data=AFTERBUY_REGISTATION)
        self.assertEquals(resp.status_code, 201)

    def test_support_api(self):
        resp = self.post('/afterbuy/v1/support/', data=AFTERBUY_SUPPORT)
        self.assertEquals(resp.status_code, 201)

    def test_product_coupons(self):
        create_mock_data = {'product_id':'1'}
        resp = self.post('/afterbuy/v1/products/1/coupons', data=json.dumps(create_mock_data))
        self.assertEquals(resp.status_code, 301)

    def test_mail_products_details(self):
        create_mock_data = {'product_id':'1'}
        resp = self.post('/afterbuy/v1/products/1/recycles', data=json.dumps(create_mock_data))
        self.assertEquals(resp.status_code, 301)
    
    def test_post_product_specifications(self):
        resp = self.post('/afterbuy/v1/product-specifications/', data=PRODUCT_SPECIFICATIONS)
        self.assertEquals(resp.status_code, 201)
    
    def test_post_product_features(self):
        resp = self.post('/afterbuy/v1/product-features/', data=PRODUCT_FEATURES)
        self.assertEquals(resp.status_code, 201)
    
    def test_post_product_recommended_parts(self):
        resp = self.post('/afterbuy/v1/product-parts/', data=PRODUCT_RECOMMENDED_PARTS)
        self.assertEquals(resp.status_code, 201)

    def test_product_details(self):
        access_token = self.user_login()
        resp = client.post('/afterbuy/v1/product-specifications/?access_token=' + access_token,
                           data=json.dumps(PRODUCT_SPECIFICATIONS), content_type='application/json')
        self.assertEquals(resp.status_code, 201)
        resp = client.post('/afterbuy/v1/product-features/?access_token=' + access_token,
                           data=json.dumps(PRODUCT_FEATURES), content_type='application/json')
        self.assertEquals(resp.status_code, 201)
        resp = client.get('/afterbuy/v1/products/details/?product_id=motorcycle&&access_token=' + access_token)
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(json.loads(resp.content)['status_code'], 200)
        resp = client.get('/afterbuy/v1/products/details/?product_id=motor&&access_token=' + access_token)
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(json.loads(resp.content)['message'], "Incorrect Product ID")

    def test_add_brand_details(self):
        access_token = self.user_login()
        resp = client.post('/afterbuy/v1/brands/?access_token=' + access_token,
                           data=json.dumps(PRODUCT_BRAND), content_type='application/json')
        self.assertEquals(resp.status_code, 201)
        return access_token
        
    def test_add_products(self):
        access_token = self.test_add_brand_details()
        resp = client.post('/afterbuy/v1/products/add/?access_token=' + access_token,
                           data=json.dumps(ADD_PRODUCT), content_type='application/json')
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(json.loads(resp.content)['status'], 200)
        
    def test_connent_to_brand(self):
        self.brand = Brand(self)
        self.create_user(username='bajaj', email='bajaj@gladminds.co', password='bajaj')
        self.brand.send_dispatch_feed()
        self.brand.send_purchase_feed() 

    def test_brand_sync(self):
        self.test_connent_to_brand()
        access_token = self.test_add_brand_details()
        uri = '/afterbuy/v1/products/brand-sync/?phone_number=7777777777&&access_token='+ access_token
        resp = client.get(uri)
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(json.loads(resp.content)['status'], 200)
    
    def test_get_service_details(self):
        self.test_connent_to_brand()
        access_token = self.test_add_brand_details()
        uri = '/afterbuy/v1/products/get-service-details/?product_id=12345678901232792&&access_token='+ access_token        
        resp = client.get(uri)
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(json.loads(resp.content)['serviceHistory'][0]['ucn'], 'USC9217')
        
    def test_get_product_coupons(self):
        self.test_connent_to_brand()
        access_token = self.user_login()
        uri = '/afterbuy/v1/products/coupons/?product_id=12345678901232792&&access_token='+ access_token
        resp = client.get(uri)
        self.assertEquals(json.loads(resp.content)['coupon_data'][0]['unique_service_coupon'], 'USC9217')
        self.assertEquals(resp.status_code, 200)

    def test_post_usermobile_info(self):
        access_token = self.user_login()
        uri = '/afterbuy/v1/user-mobile-info/?access_token='+access_token
        resp = client.post(uri, data=json.dumps(USER_MOBILE_INFO), content_type='application/json')
        self.assertEquals(resp.status_code, 201)
        self.assertEquals(json.loads(resp.content)['IMEI'], '4567008')
        
    def test_post_service_center_data(self):
        access_token = self.user_login()
        uri = '/afterbuy/v1/service-center-locations/?access_token='+access_token
        resp = client.post(uri, data=json.dumps(SERVICE_CENTER_LOCATION), content_type='application/json')
        self.assertEquals(resp.status_code, 201)
        self.assertEquals(json.loads(resp.content)['brand'], 'bajaj')
        return access_token
    
    def test_book_service(self):
        access_token = self.test_post_service_center_data()
        uri = '/afterbuy/v1/service-history/book-service/?access_token='+access_token
        resp = client.post(uri, data=json.dumps(BOOK_SERVICE), content_type='application/json')
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(json.loads(resp.content)['status'], 1)

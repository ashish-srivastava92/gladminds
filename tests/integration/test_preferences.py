"""
It will have all test cases for preferences APIs
"""
import unittest
from django.test.utils import setup_test_environment
from django.contrib.auth.models import User
from tastypie.test import ResourceTestCase
from django.test.client import Client
from provider.oauth2.models import AccessToken
from provider.oauth2.models import Client as auth_client
from test_constants import USER_PREFERENCE, APP_PREFERENCE

client = Client()
setup_test_environment()

class TestUserPreferencesResourceApi(ResourceTestCase):

    def setup(self):
        super(TestUserPreferencesResourceApi, self).setUp()
        self.access_token = 'testaccesstoken'
        user = User.objects.create_user(username='gladminds', email='gm@gm.com',password='gladminds')
        secret_cli = auth_client(user=user, name='client', client_type=1, url='')
        secret_cli.save()
        access = AccessToken(user=user, token=self.access_token, client=secret_cli)
        access.save()

    @unittest.skip("skip the test")
    def add_user_preference(self):
        resp = self.api_client.post('/v1/user-preferences/', data=USER_PREFERENCE)
        return resp

    @unittest.skip("skip the test")
    def test_create_user_perference(self):
        resp = self.add_user_preference()
        self.assertEquals(resp.status_code,201)

    @unittest.skip("skip the test")    
    def test_get_a_particular_user_preference(self):
        resp = self.add_user_preference()
        self.assertEquals(resp.status_code,201)
        resp = self.api_client.get('/v1/user-preferences/name/?user_profile=1', format='json')
        self.assertEquals(resp.status_code,200)
        self.assertEqual(self.deserialize(resp)['value'], "test_user")
        self.assertEqual(len(self.deserialize(resp)), 5)
        
    @unittest.skip("skip the test")
    def test_update_user_preference(self):
        resp = self.add_user_preference()
        self.assertEquals(resp.status_code,201)
        resp = self.api_client.get('/v1/user-preferences/name/?user_profile=1', format='json')
        self.assertEqual(self.deserialize(resp)['value'], "test_user")
        resp = self.api_client.put('/v1/user-preferences/name/?user_profile=1', format='json', data={"value":"test"})
        self.assertEquals(resp.status_code, 204)
        resp = self.api_client.get('/v1/user-preferences/name/?user_profile=1', format='json')
        self.assertEqual(self.deserialize(resp)['value'], "test")
        
    @unittest.skip("skip the test")
    def test_delete_user_preference(self):
        resp = self.add_user_preference()
        self.assertEquals(resp.status_code,201)
        resp = self.api_client.get('/v1/user-preferences/name/?user_profile=1', format='json')
        self.assertEquals(resp.status_code,200)
        self.assertEqual(len(self.deserialize(resp)), 5)
        resp = self.api_client.delete('/v1/user-preferences/1/', format='json')
        self.assertEquals(resp.status_code,204)
     
class TestAppPreferencesResourceApi(ResourceTestCase):

    def setup(self):
        super(TestAppPreferencesResourceApi, self).setUp()
        self.access_token = 'testaccesstoken'
        user = User.objects.create_user(username='gladminds', email='gm@gm.com',password='gladminds')
        secret_cli = auth_client(user=user, name='client', client_type=1, url='')
        secret_cli.save()
        access = AccessToken(user=user, token=self.access_token, client=secret_cli)
        access.save()
    def add_app_preference(self):

        resp = self.api_client.post('/v1/app-preferences/', data=APP_PREFERENCE)
        return resp
    
    @unittest.skip("skip the test")
    def test_create_app_perference(self):
        resp = self.add_app_preference()
        self.assertEquals(resp.status_code,201)
        
    @unittest.skip("skip the test")
    def test_get_a_particular_app_preference(self):
        resp = self.add_app_preference()
        self.assertEquals(resp.status_code,201)
        resp = self.api_client.get('/v1/app-preferences/name/?brand=1', format='json')
        self.assertEquals(resp.status_code,200)
        self.assertEqual(self.deserialize(resp)['value'], "test_brand")
        self.assertEqual(len(self.deserialize(resp)), 5)
        
    @unittest.skip("skip the test")
    def test_update_app_preference(self):
        resp = self.add_app_preference()
        self.assertEquals(resp.status_code,201)
        resp = self.api_client.get('/v1/app-preferences/name/?brand=1', format='json')
        self.assertEqual(self.deserialize(resp)['value'], "test_brand")
        resp = self.api_client.put('/v1/app-preferences/name/?brand=1', format='json', data={"value":"test"})
        self.assertEquals(resp.status_code, 204)
        resp = self.api_client.get('/v1/app-preferences/name/?brand=1', format='json')
        self.assertEqual(self.deserialize(resp)['value'], "test")
        
    @unittest.skip("skip the test")
    def test_delete_app_preference(self):
        resp = self.add_app_preference()
        self.assertEquals(resp.status_code,201)
        resp = self.api_client.get('/v1/app-preferences/name/?brand=1', format='json')
        self.assertEquals(resp.status_code,200)
        self.assertEqual(len(self.deserialize(resp)), 5)
        resp = self.api_client.delete('/v1/app-preferences/1/', format='json')
        self.assertEquals(resp.status_code,204)
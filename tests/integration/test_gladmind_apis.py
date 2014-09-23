import requests
from django.contrib.auth.models import User
    
from django.test.client import Client
from tastypie.test import ResourceTestCase, TestApiClient
from django.test.testcases import TestCase
import json
from provider.oauth2.models import AccessToken
from provider.oauth2.models import Client as auth_client
client = TestApiClient()
djangoClient=Client()


class GladMindsApiTests(ResourceTestCase):
    
    def setUp(self):
        super(GladMindsApiTests, self).setUp()
        self.access_token = 'testaccesstoken'
        user = User.objects.create_user(username='gladminds', email='gm@gm.com',password='gladminds')
        secret_cli = auth_client(user=user, name='client', client_type=1, url='')
        secret_cli.save()
        access = AccessToken(user=user, token=self.access_token, client=secret_cli)
        access.save()
        self.gm_user = {
                  "customer_name": "test_user",
                  "isActive": True,
                  "phone_number": "1234567890",
                  "user": {
                           "phone_number": "999999999",
                           "user": {
                                    "email": "",
                                    "first_name": "",
                                    "last_name": "",
                                    "username": "ppa",
                                    "password" :"123"
                                    }
                           }
                  }

    def add_a_gmuser(self):
        uri = '/v1/gmusers/'
        resp = self.api_client.post(uri, format='json', data=self.gm_user)
        return resp

    def test_create_a_gmuser(self):
        resp = self.add_a_gmuser()
        self.assertEquals(resp.status_code,201)

    def test_get_a_particular_gmuser(self):
        resp = self.add_a_gmuser()
        self.assertEquals(resp.status_code,201)
        resp = self.api_client.get('/v1/gmusers/1/', format='json')
        self.assertEquals(resp.status_code,200)
        self.assertEqual(self.deserialize(resp)['phone_number'], "1234567890")
        self.assertEqual(len(self.deserialize(resp)), 19)
    
    def test_update_gmuser(self):
        resp = self.add_a_gmuser()
        self.assertEquals(resp.status_code,201)
        resp = self.api_client.get('/v1/gmusers/1/', format='json')
        self.assertEqual(self.deserialize(resp)['phone_number'], "1234567890")
        resp = self.api_client.put('/v1/gmusers/1/', format='json', data={"phone_number":"1234512345"})
        self.assertEquals(resp.status_code, 200)
        self.assertEqual(self.deserialize(resp)['phone_number'], "1234512345")
    
    def test_delete_gmuser(self):
        resp = self.add_a_gmuser()
        self.assertEquals(resp.status_code,201)
        resp = self.api_client.get('/v1/gmusers/', format='json')
        self.assertEquals(resp.status_code,200)
        self.assertEqual(len(self.deserialize(resp)['objects']), 1)
        resp = self.api_client.delete('/v1/gmusers/1/', format='json')
        self.assertEquals(resp.status_code,204)
    

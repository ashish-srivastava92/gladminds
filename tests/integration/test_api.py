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


class AfterBuyIntegrationTests(ResourceTestCase):

    def setUp(self):
        super(AfterBuyIntegrationTests, self).setUp()
        self.access_token = 'testaccesstoken'
        user = User.objects.create_user(username='gladminds', email='gm@gm.com',password='gladminds')
        secret_cli = auth_client(user=user, name='client', client_type=1, url='')
        secret_cli.save()
        access = AccessToken(user=user, token=self.access_token, client=secret_cli)
        access.save()
        
    def test_users(self):
        uri='/v1/users/?accessToken=%s'%(self.access_token)
        response=self.api_client.get(uri, format='json')
        self.assertValidJSONResponse(response)
         
    def test_products(self):
        uri='/v1/users/?accessToken=%s'%(self.access_token)
        response=self.api_client.get(uri, format='json')
        self.assertValidJSONResponse(response)
        
    def test_brands(self):
        uri='/v1/users/?accessToken=%s'%(self.access_token)
        response=self.api_client.get(uri, format='json')
        self.assertValidJSONResponse(response)
        
        
    
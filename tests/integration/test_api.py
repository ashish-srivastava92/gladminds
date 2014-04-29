import requests
from django.contrib.auth.models import User
    
from django.test.client import Client
from tastypie.test import ResourceTestCase, TestApiClient
from django.test.testcases import TestCase
import json
client = TestApiClient()
djangoClient=Client()


class AfterBuyIntegrationTests(ResourceTestCase):

    def setUp(self):
        super(AfterBuyIntegrationTests, self).setUp()
        self.access_token = 'testaccesstoken'
        
    def test_users(self):
        uri='/v1/users/?accessToken=%s'%(self.access_token)
        response=self.api_client.get(uri, format='json')
        self.assertValidJSONResponse(response)
         
    def test_products(self):
        uri='/v1/products/'
        response=self.api_client.get(uri, format='json')
        self.assertValidJSONResponse(response)
        
    def test_brands(self):
        uri='/v1/brands/'
        response=self.api_client.get(uri, format='json')
        self.assertValidJSONResponse(response)
        
        
    
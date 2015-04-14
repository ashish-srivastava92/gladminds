import json
import requests
from django.test.testcases import TestCase
import os
from integration.core.constants import BajajUrls
import urllib
from django.test.client import Client
from requests import session

client = Client(SERVER_NAME=os.environ['SERVER_NAME'])


class BrandResourceTestCase(TestCase):
    

    def setUp(self):
        self.base_version = 'http://{0}/'.format(os.environ['SERVER_NAME'])
        self.base_version_xml = 'http://{0}/api/v1/feed/'.format(os.environ['SERVER_NAME'])
    
    def assertSuccess(self, first, msg=None):
        if int(first) < 200 or int(first) > 299:
            raise self.failureException(msg)
        
    def login(self,url, dct=None):
        if dct is None:
            dct = {"username": os.environ['USERNAME'], "password": os.environ['PASSWORD']}
        resp = requests.post(self.base_version+url+BajajUrls.LOGIN, data=json.dumps(dct),
                             headers={'content_type': 'application/json'})
        self.assertSuccess(resp.status_code)
        return json.loads(resp.content)['access_token']
    
    def logout(self,url,dct=None):
        if dct is None:
            dct = {"username": os.environ['USERNAME'], "password": os.environ['PASSWORD']}
        resp = requests.post(self.base_version+url+BajajUrls.LOGOUT, data=json.dumps(dct),
                             headers={'content_type': 'application/json'})
        self.assertSuccess(resp.status_code)
        return json.loads(resp.content)
            

    def post(self, uri, content_type='application/json', data=None,
             headers={'content_type': 'application/json'},isjson="True", params={}):
        params.update({'access_token': self.login(url="v1/")})
        if isjson=="False":
            resp = requests.post(self.base_version+uri, data=data, headers=headers)
        else:
            resp = requests.post(self.base_version+uri, data=json.dumps(data), headers=headers)
        self.assertSuccess(resp.status_code)
        return json.loads(resp.content)

    def get(self, uri, content_type='application/json',
            headers={'content_type':'application/json'}, params={}):
        params.update({'access_token': self.login(url="v1/")})
        resp = requests.get(self.base_version+uri, headers=headers, params=params)
        self.assertSuccess(resp.status_code)   
        return json.loads(resp.content)

    def delete(self, uri, content_type='application/json',
               headers={'content_type':'application/json'}, params={}):
        headers.update({'access_token': self.login(url="v1/")})
        resp = requests.delete(self.base_version+uri, headers=headers, params=params)
        self.assertSuccess(resp.status_code)
        
    def check_schema(self,data,stored_data):
        diff = set(data.keys()) - set(stored_data.keys())
        if diff:
            raise self.failureException("Schema not matching")
        for key,value in data.items():
            if isinstance(value,dict):
                self.check_schema(value,stored_data[key])
                
    def assertCheckSchema(self,data,COUPON_SCHEMA):
        unquoted = urllib.unquote(COUPON_SCHEMA)
        stored_data = json.loads(unquoted)
        self.check_schema(data,stored_data)

    def post_xml(self, content_type='application/xml', data=None,
             headers={
                      'content_type': 'text/xml; charset=UTF-8',
                      }, params={}):
        params.update({'access_token': self.login(url="v1/")})
        data = data.encode('utf-8')
        resp = requests.post(self.base_version_xml, data=data, headers=headers)
        self.assertSuccess(resp.status_code)
        
    def check_result(self, result,value,parameter=None,inner_parameter=None):
        if inner_parameter!=None:
            self.assertEqual(result[parameter][inner_parameter],value)
        else:
            self.assertEqual(result[parameter],value)
    
    def post_as_dealer(self, uri, username, password, content_type='application/json', data=None,
             headers={'content_type': 'application/json'},isjson="True", params={}):
        with session() as c:
            resp = c.post(self.base_version+BajajUrls.DEALER_LOGIN, data=(('username',username), ('password',password)))
            if isjson=="False":
                resp = c.post(self.base_version+uri, data=data)                
            else:
                resp = c.post(self.base_version+uri, data=json.dumps(data), headers=headers)
        self.assertSuccess(resp.status_code)
        
        
    def check_coupon(self,phone_number,data):
        data={'text': data, 'phoneNumber' : phone_number}
        coupon_data = self.post(BajajUrls.MESSAGES,content_type=None, data=data)
        self.assertTrue(coupon_data['status'])

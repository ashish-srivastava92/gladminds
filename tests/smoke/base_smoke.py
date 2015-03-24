import json
import requests
from django.test.testcases import TestCase
import os
from integration.core.constants import BajajUrls
import urllib


class BajajResourceTestCase(TestCase):

    def setUp(self):
        self.base_version = 'http://{0}/v1/'.format(os.environ['SERVER_NAME'])

    def assertSuccess(self, first, msg=None):
        if int(first) < 200 or int(first) > 299:
            raise self.failureException(msg)
        
    def login(self, dct=None):
        if dct is None:
            dct = {"username": os.environ['USERNAME'], "password": os.environ['PASSWORD']}
        resp = requests.post(self.base_version+BajajUrls.LOGIN, data=json.dumps(dct),
                             headers={'content_type': 'application/json'})
        self.assertSuccess(resp.status_code)
        return json.loads(resp.content)['access_token']

    def post(self, uri, content_type='application/json', data=None,
             headers={'content_type': 'application/json'}, params={}):
        params.update({'access_token': self.login()})
        print "111", self.base_version+uri
        resp = requests.post(self.base_version+uri, data=data)
        #print "222222222222", resp.status_code
        self.assertSuccess(resp.status_code)
        return json.loads(resp.content)

    def get(self, uri, content_type='application/json',
            headers={'content_type':'application/json'}, params={}):
        params.update({'access_token': self.login()})
        resp = requests.get(self.base_version+uri, headers=headers, params=params)
        self.assertSuccess(resp.status_code)
        return json.loads(resp.content)

    def delete(self, uri, content_type='application/json',
               headers={'content_type':'application/json'}, params={}):
        headers.update({'access_token': self.login()})
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
        
    def check_coupon(self,phone_number,data):
        #print "helooooooooooo"
        data={'text': data, 'phoneNumber' : phone_number}
        coupon_data = self.post(BajajUrls.MESSAGES,content_type=None, data=data)
        print coupon_data['message']
        #print "8888888888888",coupon_data['status']
        self.assertTrue(coupon_data['status'])

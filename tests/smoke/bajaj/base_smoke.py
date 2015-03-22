import json
import requests
from django.test.testcases import TestCase
import os
from integration.core.constants import BajajUrls


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
        resp = requests.post(self.base_version+uri, data=json.dumps(data), headers=headers)
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
                
    def assertCheckSchema(self,data,stored_data):
        self.check_schema(data,stored_data)

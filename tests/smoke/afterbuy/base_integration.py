import json
import requests
from django.test.testcases import TestCase
import os
from integration.core.constants import AfterbuyUrls


class AfterBuyResourceTestCase(TestCase):

    def setUp(self):
        self.base_version = 'http://{0}/afterbuy/v1/'.format(os.environ.get('SERVER_NAME',
                              'local.api.afterbuy.co:8000'))

    def assertSuccess(self, first, msg=None):
        if int(first) < 200 or int(first) > 299:
            raise self.failureException(msg)

    def login(self, dct=None):
        if dct is None:
            dct = {"phone_number": "9999999999", "password": "afterbuy"}
        resp = requests.post(self.base_version+AfterbuyUrls.LOGIN, data=json.dumps(dct),
                             headers={'content_type': 'application/json'})
        self.assertSuccess(resp.status_code)
        return json.loads(resp.content)['access_token']

    def post(self, uri, content_type='application/json', data=None,
             headers={'content_type': 'application/json'}, params={}):
        headers.update({'access_token': self.login()})
        resp = requests.post(self.base_version+uri, data=json.dumps(data), headers=headers)
        self.assertSuccess(resp.status_code)
        return json.loads(resp.content)

    def get(self, uri, content_type='application/json',
            headers={'content_type':'application/json'}, params={}):
        headers.update({'access_token': self.login()})
        resp = requests.get(self.base_version+uri, headers=headers, params=params)
        self.assertSuccess(resp.status_code)
        return json.loads(resp.content)

    def delete(self, uri, content_type='application/json',
               headers={'content_type':'application/json'}, params={}):
        headers.update({'access_token': self.login()})
        resp = requests.delete(self.base_version+uri, headers=headers, params=params)
        self.assertSuccess(resp.status_code)

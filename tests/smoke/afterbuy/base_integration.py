import json
import requests
from django.test.testcases import TestCase
import os


class AfterBuyResourceTestCase(TestCase):

    def setUp(self):
        self.base_version = 'http://{0}/afterbuy/v1/'.format(os.environ.get('SERVER_NAME',
                                                                      'local.api.afterbuy.co:8000'))

    def post(self, uri, content_type='application/json', data=None):
        return requests.post(self.base_version+uri, data=json.dumps(data))
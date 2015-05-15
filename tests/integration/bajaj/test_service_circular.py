from django.test.client import Client
import json
from test_constants import SERVICE_CIRCULAR
from integration.bajaj.base import BaseTestCase

client=Client(SERVER_NAME='bajaj')

class ServiceCircularTests(BaseTestCase):
    multi_db=True
    def setUp(self):
        self.create_user(username='bajaj', email='bajaj@gladminds.co', password='bajaj')
        self.base_version = 'http://local.bajaj.gladminds.co:8000'
        super(ServiceCircularTests, self).setUp()

    def post(self, uri, data, access_token=None):
        if access_token:
            uri = uri+'?access_token='+access_token
        resp = client.post(uri, data=data)
        return resp

    def get(self, uri, access_token, content_type='application/json'):
        resp = client.get(uri+'?access_token='+access_token, content_type=content_type)
        return resp
    
    def getCode(self, uri, access_token, content_type='application/json'):
        resp = client.get(uri+'&&access_token='+access_token, content_type=content_type)
        return resp
    
    def user_login(self):
        data={"username": "bajaj", "password": "bajaj" }
        uri='/v1/gm-users/login/';
        resp=client.post(self.base_version+uri, data=json.dumps(data),content_type='application/json')
        return json.loads(resp.content)['access_token']
    
    def test_get_service_circular(self):
        access_token = self.user_login()
        uri = '/v1/service-circular/save_circular/'
        resp = self.post(uri=uri, data=SERVICE_CIRCULAR, access_token=access_token)
        self.assertEquals(resp.status_code, 200)
        uri = '/v1/service-circular/'
        resp = self.get(uri, access_token, content_type='application/json')
        self.assertEquals(resp.status_code, 200)
        uri = '/v1/service-circular/?model_sku_code__sku_code=00DK04ZZ'
        resp = self.getCode(uri, access_token, content_type='application/json')
        self.assertEquals(resp.status_code, 200)
        
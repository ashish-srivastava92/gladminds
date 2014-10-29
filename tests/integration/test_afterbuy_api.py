''' Test Case for testing out the Afterbuy Api
'''
from tastypie.test import ResourceTestCase, TestApiClient
from django.test.client import Client
client = TestApiClient()
djangoClient = Client()


class TestAfterbuyApi(ResourceTestCase):
    def setUp(self):
        super(TestAfterbuyApi, self).setUp()

    def test_user_registration(self):
        create_mock_data = {'name': 'saurav','phone_number':'7760814041','email_id':'srv.sngh@gmail.com','password':'123'}
        uri = '/afterbuy/v1/user/registration/'
        resp = self.api_client.post(uri, format='json', data=create_mock_data)
        print client
        print resp.status_code
        self.assertEquals(1, 2)

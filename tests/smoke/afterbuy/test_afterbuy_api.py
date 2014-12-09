''' Smoke for testing out the Afterbuy Api
'''
from smoke.afterbuy import base_integration
from integration.core.constants import AfterbuyUrls


class TestAfterbuyApi(base_integration.AfterBuyResourceTestCase):
    def setUp(self):
        super(TestAfterbuyApi, self).setUp()

    def test_user_registration(self):
        mock_data = {'first_name': 'test', 'phone_number': '7760814041',
                     'email_id': 'srv.sngh@gmail.com', 'password': '123',
                     'otp_token': 'GMDEV123'}
        uri = AfterbuyUrls.REGISTRATION
        resp = self.post(uri, data=mock_data)
        self.assertEquals(200, resp.status_code)

    def test_user_login(self):
        login_data = {'phone_number':'7760814041', 'password':'123'}
        uri = 'consumers/login/'
        resp = self.post(uri, data=login_data)
        self.assertEquals(200, resp.status_code)
        # Checking login by email id
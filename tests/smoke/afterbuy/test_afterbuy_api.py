''' Smoke for testing out the Afterbuy Api
'''
from smoke.afterbuy import base_integration
from integration.core.constants import AfterbuyUrls, Constants
import json
import os


class TestAfterbuyAdminApi(base_integration.AfterBuyResourceTestCase):
    def setUp(self):
        super(TestAfterbuyAdminApi, self).setUp()

    def test_get_add_brand(self):
        data = self.get(AfterbuyUrls.BRAND, params={"name": Constants.BRAND,
                                                    "industry__name": Constants.INDUSTRY})
        if data['meta']['total_count']!=0:
            self.delete(AfterbuyUrls.BRAND, params={"name": Constants.BRAND,
                                                    "industry__name": Constants.INDUSTRY})
            self.delete(AfterbuyUrls.INDUSTRY, params={"name": Constants.INDUSTRY})

        self.post(AfterbuyUrls.BRAND, data={"name":Constants.BRAND,
                                                "industry":{"name":Constants.INDUSTRY}})

        data = self.get(AfterbuyUrls.BRAND, params={"name": Constants.BRAND,
                                                    "industry__name": Constants.INDUSTRY})
        self.assertEquals(int(data['meta']['total_count']), 1)
    
    def test_get_add_product_type(self):
#     def test_user_registration(self):
#         mock_data = {'first_name': 'test', 'phone_number': '7760814041',
#                      'email_id': 'srv.sngh@gmail.com', 'password': '123',
#                      'otp_token': 'GMDEV123'}
#         uri = AfterbuyUrls.REGISTRATION
#         resp = self.post(uri, data=mock_data)
#         self.assertEquals(200, resp.status_code)
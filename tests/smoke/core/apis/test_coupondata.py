''' Smoke for testing out the Afterbuy Api
'''
from smoke import base_smoke
from integration.core.constants import Urls, Constants, COUPON_SCHEMA
import json
import os


class TestBajajCouponDataApi(base_smoke.BrandResourceTestCase):
    def setUp(self):
        super(TestBajajCouponDataApi, self).setUp()

    def test_get_coupondata(self):
        data = self.get(Urls.COUPONS)
        data = data['objects'][0]
        self.assertCheckSchema(data, COUPON_SCHEMA)
''' Smoke for testing out the Afterbuy Api
'''
from smoke.bajaj import base_smoke
from integration.core.constants import BajajUrls, Constants, COUPON_SCHEMA
import json
import os
import urllib


class TestBajajCouponDataApi(base_smoke.BajajResourceTestCase):
    def setUp(self):
        super(TestBajajCouponDataApi, self).setUp()

    def test_get_coupondata(self):
        data = self.get(BajajUrls.COUPONS)
        data = data['objects'][0]
        unquoted = urllib.unquote(COUPON_SCHEMA)
        stored_data = json.loads(unquoted)
        self.assertCheckSchema(data, stored_data)
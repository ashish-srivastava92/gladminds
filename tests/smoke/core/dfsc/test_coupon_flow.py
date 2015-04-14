import json
import requests
from django.test.testcases import TestCase
import os
from smoke import base_smoke
from integration.core.constants import BajajUrls, Constants, COUPON_SCHEMA
from gladminds.core.constants import CouponStatus

class TestBajajCouponDataApi(base_smoke.BajajResourceTestCase):
    def setUp(self):
        super(TestBajajCouponDataApi, self).setUp()

    def test_couponcheck(self):
        phone_number="+919999999999"
        self.check_coupon_closed('USC001')
        data = 'A {0} {1} {2}'.format('SAP001', 450, 1)
        self.check_coupon(phone_number, data)
        self.check_coupon_inprogress('USC001')
         
    def check_coupon_status(self, unique_service_coupon, status):
        coupon = self.get(BajajUrls.COUPONS+'?unique_service_coupon='+unique_service_coupon)
        self.assertEqual(coupon['objects'][0]['status'], status)
        
    def check_coupon_inprogress(self,unique_service_coupon):
        coupon = self.get(BajajUrls.COUPONS+'?unique_service_coupon='+unique_service_coupon)
        self.assertEqual(coupon['objects'][0]['status'], CouponStatus.IN_PROGRESS)
        
    def check_coupon_closed(self,unique_service_coupon):
        coupon = self.get(BajajUrls.COUPONS+'?unique_service_coupon='+unique_service_coupon)
        self.assertEqual(coupon['objects'][0]['status'], CouponStatus.CLOSED)
        
    def test_check_exceed_limit(self):
        
        phone_number="+919999999999"
        data = 'A {0} {1} {2}'.format('SAP001', 2500, 1, )
        self.check_coupon(phone_number, data)
        self.check_coupon_status('USC002', 5)
        
    def test_check_closed(self):
        phone_number="+919999999999"
        self.check_coupon_closed('USC001')
        data = 'C {0} {1} '.format('SAP001', 'USC001')
        self.check_coupon(phone_number, data)
        self.check_coupon_status('USC001', 2)
        
        
        
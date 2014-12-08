import logging

from django.test import TestCase
from django.utils import unittest

from integration.bajaj.base import BaseTestCase
from integration.bajaj.test_brand_logic import Brand
from integration.bajaj.test_system_logic import System

from gladminds.bajaj.models import CouponData, UserProfile

logger = logging.getLogger('gladminds')

class FeedsResourceTest(BaseTestCase):
    multi_db=True

    def setUp(self):
        TestCase.setUp(self)
        self.brand = Brand(self)
        self.system = System(self)
        BaseTestCase.setUp(self)
        self.create_user(username='gladminds', email='gladminds@gladminds.co', password='gladminds')

    def test_service_advisor_feed(self):
        brand = self.brand
        brand.send_service_advisor_feed()
        brand.check_service_feed_saved_to_database()

    def test_service_advisor_dealer_relationship(self):
        brand = self.brand
        brand.send_service_advisor_feed()
        brand.check_service_advisor_dealer_relationship_saved_to_database()
        '''
           Checking out with new feed to change the status of service advisor
        '''
        brand.send_service_advisor_feed_with_new_status()
        brand.check_data_saved_to_database()
 
    def test_service_advisor_phone_number_updation_logic(self):
        brand = self.brand
        '''
           Checking out with new feed to change the status of service advisor
            Checking out with new feed to 
            1. update to a new unregistered/inactive phone number should pass
            2. updating with an active mobile number should fail
            3. Try to register a new SA with an active mobile number should fail
        '''
        brand.send_service_advisor_feed()
        brand.check_service_feed_saved_to_database()
  
        brand.send_sa_upate_mobile_feed()
        brand.service_advisor_database_upadted()
  
    def test_product_dispatch(self):
        brand = self.brand
        brand.send_service_advisor_feed()
        brand.send_dispatch_feed()
        brand.check_product_data_saved_to_database()
  
    def test_product_purchase(self):
        brand = self.brand
        brand.send_purchase_feed()
  
    def test_coupon_redamption_feed(self):
        brand = self.brand
        brand.send_service_advisor_feed()
        brand.send_dispatch_feed()
        brand.send_purchase_feed()
        brand.coupon_data_saved_to_database()

#FIXME: Needs to fix it by code changes
#     def test_partial_fail(self):
#         brand = self.brand
#         brand.send_as_feed_without_id()
#   
    def test_update_customer_number(self):
        brand = self.brand
        system = self.system
        brand.send_dispatch_feed()
        brand.send_purchase_feed()
        gm_user = UserProfile.objects.all()
        system.verify_result(input=len(gm_user), output=1)
        brand.send_purchase_feed_with_diff_cust_num()
        product_object = system.get_product_details(product_id='XXXXXXXXXX')
        system.verify_result(input=product_object.customer_phone_number, output="+919845340297")
        system.verify_result(input=UserProfile.objects.count(), output=1)
  
    def test_auth(self):
        brand = self.brand
        self.create_user(username='testuser', email='testuserpassword@gladminds.co', password='testuserpassword')
        brand.check_for_auth()
 
    @unittest.skip("Skipping Adding this functionality in future")
    def test_coupon_status_on_dispatch_feed(self):
        brand = self.brand
        system = self.system
        '''
            Test for testing out coupon status on dispatch feed
            Its default value is 1
        '''
 
        brand.send_dispatch_feed()
        system.verify_result(input=CouponData.objects.count(), output=2)
        coupon_data = CouponData.objects.all()[0]
        system.verify_result(input=CouponData.objects.count(), output=2)
        system.verify_result(input=coupon_data.unique_service_coupon, output=u"USC001")
        system.verify_result(input=coupon_data.status, output=2)
        coupon_data = CouponData.objects.all()[1]
        system.verify_result(input=coupon_data.status, output=2)
        system.verify_result(input=coupon_data.unique_service_coupons, output=u"USC002")
        system.verify_result(input=coupon_data.status, output=1)
 
    def test_coupon_status_without_ucn(self):
        brand = self.brand
        system = self.system
        '''
            Test for testing out dispatch feed without_ucn
        '''
        brand.send_dispatch_feed_without_ucn()
        system.verify_result(input=CouponData.objects.count(), output=1)
        coupon_data = CouponData.objects.all()[0]
        system.verify_result(input=coupon_data.unique_service_coupon, output=u"USC002")
 
    def test_asc_feed(self):
        brand = self.brand
        brand.send_asc_feed()
        brand.check_asc_feed_saved_to_database()


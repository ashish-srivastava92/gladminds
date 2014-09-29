import logging
from django.test import TestCase
from gladminds.models.common import \
     CouponData, GladMindUsers
from integration.base import BaseTestCase
from integration.test_brand_logic import Brand
from integration.test_system_logic import SystemFunction
from django.utils import unittest

logger = logging.getLogger('gladminds')

# base_test = BaseTestCase()


class FeedsResourceTest(BaseTestCase):

    def setUp(self):
        TestCase.setUp(self)
        self.brand = Brand(self)
        self.system = SystemFunction(self)
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
 
    def test_partial_fail(self):
        brand = self.brand
        brand.send_as_feed_without_id()
 
    def test_update_customer_number(self):
        brand = self.brand
        system = self.system
        brand.send_dispatch_feed()
        brand.send_purchase_feed()
        gm_user = GladMindUsers.objects.all()
        self.assertEqual(1, len(gm_user))
        brand.send_purchase_feed_with_diff_cust_num()
        product_object = system.get_product_details(vin='XXXXXXXXXX')
        self.assertEqual(product_object.customer_phone_number.phone_number, "+919845340297", "Customer Phone Number is not updated")
        self.assertEqual(GladMindUsers.objects.count(), 2, "Total GM User")
 
    def test_auth(self):
        brand = self.brand
        self.create_user(username='testuser', email='testuserpassword@gladminds.co', password='testuserpassword')
        brand.check_for_auth()
 
    @unittest.skip("Skipping Adding this functionality in future")
    def test_coupon_status_on_dispatch_feed(self):
        brand = self.brand
        '''
            Test for testing out coupon status on dispatch feed
            Its default value is 1
        '''
        brand.send_dispatch_feed()
 
        self.assertEquals(2, CouponData.objects.count())
        coupon_data = CouponData.objects.all()[0]
        self.assertEquals(u"USC001", coupon_data.unique_service_coupon)
        self.assertEquals(2, coupon_data.status)
        coupon_data = CouponData.objects.all()[1]
        self.assertEquals(u"USC002", coupon_data.unique_service_coupon)
        self.assertEquals(1, coupon_data.status, 'Default value should be 1')
 
    def test_coupon_status_without_ucn(self):
        brand = self.brand
        '''
            Test for testing out dispatch feed without_ucn
        '''
        brand.send_dispatch_feed_without_ucn()
 
        self.assertEquals(1, CouponData.objects.count())
        coupon_data = CouponData.objects.all()[0]
        self.assertEquals(u"USC002", coupon_data.unique_service_coupon)
 
    def test_asc_feed(self):
        brand = self.brand
        brand.send_asc_feed()
        brand.check_asc_feed_saved_to_database()


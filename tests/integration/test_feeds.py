import logging
from django.test import TestCase
from gladminds.models.common import \
     CouponData, GladMindUsers
from integration.base import BaseTestCase
from django.utils import unittest

logger = logging.getLogger('gladminds')

# base_test = BaseTestCase()


class FeedsResourceTest(BaseTestCase):

    def setUp(self):
        TestCase.setUp(self)
        BaseTestCase.setUp(self)
        self.create_user(username='gladminds', email='gladminds@gladminds.co', password='gladminds')

    def test_service_advisor_feed(self):
        self.create_service_advisor_through_feed()
        self.check_service_feed_saved_to_database()

    def test_service_advisor_dealer_relationship(self):
        self.create_service_advisor_through_feed()
        self.check_service_advisor_dealer_relationship_saved_to_database()
        '''
           Checking out with new feed to change the status of service advisor
        '''
        self.send_service_advisor_feed_with_new_status()
        self.check_data_saved_to_database()

    def test_service_advisor_phone_number_updation_logic(self):
        '''
           Checking out with new feed to change the status of service advisor
            Checking out with new feed to 
            1. update to a new unregistered/inactive phone number should pass
            2. updating with an active mobile number should fail
            3. Try to register a new SA with an active mobile number should fail
        '''
        self.create_service_advisor_through_feed()
        self.check_service_feed_saved_to_database()

        self.send_sa_upate_mobile_feed()
        self.service_advisor_database_upadted()

    def test_product_dispatch(self):
        self.create_service_advisor_through_feed()
        self.send_dispatch_feed()
        self.check_product_data_saved_to_database()

    def test_product_purchase(self):
        self.send_purchase_feed()

    def test_coupon_redamption_feed(self):
        self.create_service_advisor_through_feed()
        self.send_dispatch_feed()
        self.send_purchase_feed()
        self.coupon_data_saved_to_database()

    def test_partial_fail(self):
        self.send_as_feed_without_id()

    def test_update_customer_number(self):
        self.send_dispatch_feed()
        self.send_purchase_feed()
        gm_user = GladMindUsers.objects.all()
        self.assertEqual(1, len(gm_user))
        self.send_purchase_feed_with_diff_cust_num()
        product_object = self.get_product_details(vin='XXXXXXXXXX')
        self.assertEqual(product_object.customer_phone_number.phone_number, "+919845340297", "Customer Phone Number is not updated")
        self.assertEqual(GladMindUsers.objects.count(), 2, "Total GM User")

    def test_auth(self):
        self.create_user(username='testuser', email='testuserpassword@gladminds.co', password='testuserpassword')
        self.check_for_auth()

    @unittest.skip("Skipping Adding this functionality in future")
    def test_coupon_status_on_dispatch_feed(self):
        '''
            Test for testing out coupon status on dispatch feed
            Its default value is 1
        '''
        self.send_dispatch_feed()

        self.assertEquals(2, CouponData.objects.count())
        coupon_data = CouponData.objects.all()[0]
        self.assertEquals(u"USC001", coupon_data.unique_service_coupon)
        self.assertEquals(2, coupon_data.status)
        coupon_data = CouponData.objects.all()[1]
        self.assertEquals(u"USC002", coupon_data.unique_service_coupon)
        self.assertEquals(1, coupon_data.status, 'Default value should be 1')

    def test_coupon_status_without_ucn(self):
        '''
            Test for testing out dispatch feed without_ucn
        '''
        self.send_dispatch_feed_without_ucn()

        self.assertEquals(1, CouponData.objects.count())
        coupon_data = CouponData.objects.all()[0]
        self.assertEquals(u"USC002", coupon_data.unique_service_coupon)

    def test_asc_feed(self):
        self.send_asc_feed()
        self.check_asc_feed_saved_to_database()


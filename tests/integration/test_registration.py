from django.test import TestCase
from django.test.client import Client
from integration.base import BaseTestCase


class TestDealerRegistration(BaseTestCase):
    def setUp(self):
        self.client = Client()
        BaseTestCase.setUp(self)
 
    def test_new_dealer(self):
        self.dealer_login()


class TestCustomerRegistration(BaseTestCase):
    def setUp(self):
        TestCase.setUp(self)
        BaseTestCase.setUp(self)
        self.client = Client()
        self.create_user(username='gladminds', email='gladminds@gladminds.co', password='gladminds')
        self.send_dispatch_feed()
        self.send_purchase_feed()
        '''This both feed will create product data, product type ,brand database'''

    def test_temp_customer_registration(self):
        self.dealer_login()
        self.register_customer()

    def test_update_cutomer_mobile(self):
        product_obj = self.get_product_details(vin='XXXXXXXXXX')
        self.assertEqual(product_obj.customer_phone_number.phone_number, '+91666666')
        self.send_purchase_feed_with_diff_cust_num()
        product_obj = self.get_product_details(vin='XXXXXXXXXX')
        self.assertEqual(product_obj.customer_phone_number.phone_number, '+919845340297')
  
    def test_asc_registration_by_self(self):
        self.dealer_login()
        self.check_asc_exists('test_asc','test_asc','dealer')
  
    def test_asc_registration_by_dealer(self):
        self.check_asc_exists('test_asc','test_asc','self')

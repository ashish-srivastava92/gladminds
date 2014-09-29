from django.test import TestCase
from django.test.client import Client
from integration.base import BaseTestCase
from integration.test_brand_logic import Brand
from integration.test_system_logic import System


class TestDealerRegistration(BaseTestCase):
    def setUp(self):
        self.client = Client()
        BaseTestCase.setUp(self)
        self.system = System(self)

    def test_new_dealer(self):
        system = self.system
        system.dealer_login()


class TestCustomerRegistration(BaseTestCase):
    def setUp(self):
        TestCase.setUp(self)
        BaseTestCase.setUp(self)
        self.brand = Brand(self)
        brand = self.brand
        self.system = System(self)
        self.client = Client()
        self.create_user(username='gladminds', email='gladminds@gladminds.co', password='gladminds')
        brand.send_dispatch_feed()
        brand.send_purchase_feed()
        '''This both feed will create product data, product type ,brand database'''

    def test_temp_customer_registration(self):
        system = self.system
        system.dealer_login()
        system.register_customer()

    def test_update_cutomer_mobile(self):
        system = self.system
        brand = self.brand
        product_obj = system.get_product_details(vin='XXXXXXXXXX')
        self.assertEqual(product_obj.customer_phone_number.phone_number, '+91666666')
        brand.send_purchase_feed_with_diff_cust_num()
        product_obj = system.get_product_details(vin='XXXXXXXXXX')
        self.assertEqual(product_obj.customer_phone_number.phone_number, '+919845340297')

    def test_asc_registration_by_self(self):
        system = self.system
        system.dealer_login()
        system.check_asc_exists('test_asc','test_asc','dealer')

    def test_asc_registration_by_dealer(self):
        system = self.system
        system .check_asc_exists('test_asc','test_asc','self')

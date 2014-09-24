import os

from django.test.client import Client
from django.contrib.auth.models import User, Group
from gladminds.aftersell.models import common as aftersell_common
from integration.base_integration import GladmindsResourceTestCase


class TestDealerRegistration(GladmindsResourceTestCase):
    def setUp(self):
        self.client = Client()
        self.username = 'DEALER01'
        self.email = 'dealer@xyz.com'
        self.password = 'DEALER01@123'

    def test_new_dealer(self):
        self.test_user = User.objects.create_user(self.username, self.email, self.password)
        login = self.client.login(username=self.username, password=self.password)
        self.assertTrue(login)
        
class TestCustomerRegistration(GladmindsResourceTestCase):
    def setUp(self):
        super(TestCustomerRegistration, self).setUp()
        self.client = Client()
        user = User.objects.create_user('gladminds', 'gladminds@gladminds.co', 'gladminds')
        user.save()
        user_group = Group.objects.get(name='dealers')
        test_user = User.objects.create_user('DEALER01', 'dealer@xyz.com', 'DEALER01@123')
        test_user.groups.add(user_group)
        test_user.save()
        login = self.client.login(username='DEALER01', password='DEALER01@123')
        self.send_dispatch_feed()

    def register_customer(self, data):
        response = self.client.post('/aftersell/register/customer', data=data)
        return response
        
    def test_temp_customer_registration(self):
        data = {
                    'customer-phone': '9999999999',
                    'customer-name': 'TestUser',
                    'purchase-date': '11/5/2014',
                    'customer-vin': 'XXXXXXXXXX',
                    'customer-id': '',
                }
        response = self.register_customer(data)
        temp_customer_obj=self.get_temp_customer_obj(new_customer_name='TestUser')
        self.assertEqual(temp_customer_obj.new_customer_name, 'TestUser')
        self.assertEqual(response.status_code, 200)

    def test_update_cutomer_mobile(self):
        self.send_purchase_feed()
        product_obj = self.get_product_details(vin='XXXXXXXXXX')
        self.assertEqual(product_obj.customer_phone_number.phone_number, '+91666666')
        data = {
                    'customer-phone': '9999999999',
                    'customer-name': 'TestUser',
                    'purchase-date': '11/5/2014',
                    'customer-vin': 'XXXXXXXXXX',
                    'customer-id': 'GMCUSTOMER01',
                }
        response = self.register_customer(data)
        product_obj = self.get_product_details(vin='XXXXXXXXXX')
        self.assertEqual(product_obj.customer_phone_number.phone_number, '+919999999999')
        self.assertEqual(response.status_code, 200)

    def test_adding_asc_and_chang_password(self):
        self.test_user = User.objects.create_user('test_asc', 'testasc@gmail.com', 'test_asc_pass')
        login = self.client.login(username='test_asc', password='test_asc_pass')
        self.assertTrue(login)
        ascgroup = Group.objects.get(name='ascs')
        ascgroup.user_set.add(self.test_user)
        data = {'oldPassword': 'test_asc_pass', 'newPassword':'test_asc_pass_new'}
        self.client.post('/aftersell/provider/change-password', data)
        login = self.client.login(username='test_asc', password='test_asc_pass')
        self.assertFalse(login)
        login = self.client.login(username='test_asc', password='test_asc_pass_new')
        self.assertTrue(login)

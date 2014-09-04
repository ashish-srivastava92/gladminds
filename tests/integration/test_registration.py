import os
from django.conf import settings
from integration.base_integration import GladmindsResourceTestCase
from django.test.client import Client
from django.contrib.auth.models import User, Group


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

    def register_self_asc(self, data):
        response = self.client.post('/aftersell/asc/self-register/', data=data)
        return response
    
    def test_temp_asc_self_registration(self):
        data = {
                    'name' : 'test_asc',
                    'address' : 'ABCDEF',
                    'password' : '123',
                    'phone-number' : '9999999999',
                    'email' : 'abc@abc.com',
                    'pincode' : '562106'
                }
        response = self.register_self_asc(data)
        temp_asc_obj = self.get_temp_asc_obj(name='test_asc')
        self.assertEqual(temp_asc_obj.name, 'test_asc')
        self.assertEqual(response.status_code, 200)
    
    def register_asc_through_dealer(self, data):
        response = self.client.post('/aftersell/register/asc', data=data)
        return response
    
    def test_temp_asc_registration_through_dealer(self):
        data = {
                    'name' : 'test_asc',
                    'address' : 'ABCDEF',
                    'password' : '123',
                    'phone-number' : '9999999999',
                    'email' : 'abc@abc.com',
                    'pincode' : '562106'
                }
        response = self.register_asc_through_dealer(data)
        temp_asc_obj = self.get_temp_asc_obj(name='test_asc')
        self.assertEqual(temp_asc_obj.name, 'test_asc')
        self.assertEqual(response.status_code, 200)
        
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


    def test_adding_asc_and_chang_password(self):
        self.test_user = User.objects.create_user('test_asc', 'testasc@gmail.com', 'test_asc_pass')
        login = self.client.login(username='test_asc', password='test_asc_pass')
        self.assertTrue(login)
        ascgroup = Group.objects.create(name='ascs')
        ascgroup.user_set.add(self.test_user)
        data = {'oldPassword': 'test_asc_pass', 'newPassword':'test_asc_pass_new'}
        self.client.post('/aftersell/provider/change-password', data)
        login = self.client.login(username='test_asc', password='test_asc_pass')
        self.assertFalse(login)
        login = self.client.login(username='test_asc', password='test_asc_pass_new')
        self.assertTrue(login)

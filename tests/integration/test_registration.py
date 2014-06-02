import os
from django.conf import settings
from integration.base_integration import GladmindsResourceTestCase
from django.test.client import Client
from django.contrib.auth.models import User


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
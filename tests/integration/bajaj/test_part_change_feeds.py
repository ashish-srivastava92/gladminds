import logging

from django.test import TestCase
from django.utils import unittest

from integration.bajaj.base import BaseTestCase
from integration.bajaj.test_brand_logic import Brand
from integration.bajaj.test_system_logic import System

from gladminds.bajaj.models import CouponData, UserProfile

logger = logging.getLogger('gladminds')

class PartChangeFeedResourceTest(BaseTestCase):
    multi_db=True

    def setUp(self):
        TestCase.setUp(self)
        self.brand = Brand(self)
        self.system = System(self)
        BaseTestCase.setUp(self)
        self.create_user(username='bajaj', email='bajaj@gladminds.co', password='bajaj')
        self.access_token = self.brand.admin_login()

    def test_manufacture_data_feed(self):
        brand = self.brand
        system = self.system
        brand.send_manufacture_data_feed()
        saved_manufaturing_data=brand.get_manufaturing_data(self.access_token)
        system.verify_result(input=len(saved_manufaturing_data), output=2)
        system.verify_result(input=saved_manufaturing_data[0]['is_discrepant'], output=False)
        system.verify_result(input=saved_manufaturing_data[1]['is_discrepant'], output=True)
        

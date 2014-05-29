''' Test Case for testing out the Afterbuy Api
'''

from integration.base_integration import GladmindsResourceTestCase
from django.test.client import Client

client = Client()

class TestAfterbuy(GladmindsResourceTestCase):

    def setUp(self):
        pass

    def test_user_registration(self):
        pass

    def test_product_details(self):
        #client.get('/gm/', data={})
        pass
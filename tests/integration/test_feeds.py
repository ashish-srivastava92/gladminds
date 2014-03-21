import logging
import os
from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase
from gladminds.models.common import RegisteredDealer, ServiceAdvisor

logger = logging.getLogger('gladminds')


class FeedsResourceTest(TestCase):

    def setUp(self):
        TestCase.setUp(self)
        user = User.objects.create_user('gladminds', 'gladminds@gladminds.co', 'gladminds')
        user.save()

    def test_service_advisor_feed(self):
        file_path = os.path.join(settings.BASE_DIR, 'tests/integration/service_advisor_feed.xml')
        xml_data = open(file_path, 'r').read()
        response = self.client.post('/api/v1/bajaj/feed/?wsdl', data=xml_data,content_type='text/xml')

        self.assertEqual(200, response.status_code)
        self.assertEquals(1, RegisteredDealer.objects.count())
        dealer_data = RegisteredDealer.objects.all()[0]
        self.assertEquals(u"GMDEALER001", dealer_data.dealer_id)
        service_advisors = ServiceAdvisor.objects.filter(dealer_id=dealer_data)
        self.assertEquals(1, len(service_advisors))
        self.assertEquals(u"GMDEALER001SA01", service_advisors[0].service_advisor_id)
        self.assertEquals(service_advisors[0].status, "Y", "Service Advisor status should be active")

    def test_product_purchase(self):
        file_path = os.path.join(settings.BASE_DIR, 'tests/integration/product_purchase_feed.xml')
        xml_data = open(file_path, 'r').read()
        response = self.client.post('/api/v1/bajaj/feed/?wsdl', data=xml_data,content_type='text/xml')
        self.assertEqual(200, response.status_code)

    def test_product_dispatch(self):
        file_path = os.path.join(settings.BASE_DIR, 'tests/integration/product_dispatch_feed.xml')
        xml_data = open(file_path, 'r').read()
        response = self.client.post('/api/v1/bajaj/feed/?wsdl', data=xml_data,content_type='text/xml')
        self.assertEqual(200, response.status_code)

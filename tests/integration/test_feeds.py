import logging
import os
from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase
from gladminds.models.common import RegisteredDealer, ServiceAdvisor,\
    ProductData, CouponData
from gladminds import feed, exportfeed
from datetime import datetime, timedelta
from integration.base_integration import GladmindsResourceTestCase

logger = logging.getLogger('gladminds')


class FeedsResourceTest(GladmindsResourceTestCase):

    def setUp(self):
        TestCase.setUp(self)
        user = User.objects.create_user('gladminds', 'gladminds@gladminds.co', 'gladminds')
        user.save()

    def test_service_advisor_feed(self):
        file_path = os.path.join(settings.BASE_DIR, 'tests/integration/service_advisor_feed.xml')
        xml_data = open(file_path, 'r').read()
        response = self.client.post('/api/v1/bajaj/feed/?wsdl', data=xml_data,content_type='text/xml')
        
        self.assertEqual(200, response.status_code)
        self.assertEquals(2, RegisteredDealer.objects.count())
        dealer_data = RegisteredDealer.objects.all()[0]
        self.assertEquals(u"GMDEALER001", dealer_data.dealer_id)
        service_advisors = ServiceAdvisor.objects.filter(dealer_id=dealer_data)
        self.assertEquals(1, len(service_advisors))
        self.assertEquals(u"GMDEALER001SA01", service_advisors[0].service_advisor_id)
        self.assertEquals(service_advisors[0].status, "Y", "Service Advisor status should be active")

    def test_product_dispatch(self):
        file_path = os.path.join(settings.BASE_DIR, 'tests/integration/service_advisor_feed.xml')
        xml_data = open(file_path, 'r').read()
        response = self.client.post('/api/v1/bajaj/feed/?wsdl', data=xml_data,content_type='text/xml')
        self.assertEqual(200, response.status_code)

        file_path = os.path.join(settings.BASE_DIR, 'tests/integration/product_dispatch_feed.xml')
        xml_data = open(file_path, 'r').read()
        response = self.client.post('/api/v1/bajaj/feed/?wsdl', data=xml_data,content_type='text/xml')
        self.assertEqual(200, response.status_code)

        self.assertEquals(1, ProductData.objects.count())
        product_data = ProductData.objects.all()[0]
        self.assertEquals(u"XXXXXXXXXX", product_data.vin)

        self.assertEquals(1, CouponData.objects.count())
        coupon_data = CouponData.objects.all()[0]
        self.assertEquals(u"UUUUUUU", coupon_data.unique_service_coupon) 

    def test_product_purchase(self):
        file_path = os.path.join(settings.BASE_DIR, 'tests/integration/product_purchase_feed.xml')
        xml_data = open(file_path, 'r').read()
        response = self.client.post('/api/v1/bajaj/feed/?wsdl', data=xml_data,content_type='text/xml')
        self.assertEqual(200, response.status_code)

    def test_feed_log(self):
        pass

    def test_coupon_redamption_feed(self):
        file_path = os.path.join(settings.BASE_DIR, 'tests/integration/service_advisor_feed.xml')
        xml_data = open(file_path, 'r').read()
        response = self.client.post('/api/v1/bajaj/feed/?wsdl', data=xml_data,content_type='text/xml')
        self.assertEqual(200, response.status_code)

        file_path = os.path.join(settings.BASE_DIR, 'tests/integration/product_dispatch_feed.xml')
        xml_data = open(file_path, 'r').read()
        response = self.client.post('/api/v1/bajaj/feed/?wsdl', data=xml_data,content_type='text/xml')
        self.assertEqual(200, response.status_code)

        file_path = os.path.join(settings.BASE_DIR, 'tests/integration/product_purchase_feed.xml')
        xml_data = open(file_path, 'r').read()
        response = self.client.post('/api/v1/bajaj/feed/?wsdl', data=xml_data,content_type='text/xml')
        self.assertEqual(200, response.status_code)

        today = datetime.now()
        start_date = today - timedelta(days=1)
        end_date = today
        #redeem_obj = feed.CouponRedeemFeedToSAP()
        #items, item_batch = redeem_obj.export_data(start_date=start_date, end_date=end_date)

        #coupon_redeem = exportfeed.ExportCouponRedeemFeed(username=settings.SAP_CRM_DETAIL['username'], password = settings.SAP_CRM_DETAIL['password'], wsdl_url = settings.COUPON_WSDL_URL)
        #coupon_redeem.export(items=items, item_batch=item_batch)

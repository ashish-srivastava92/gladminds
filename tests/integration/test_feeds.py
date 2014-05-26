import logging
import os
from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase
from gladminds.models.common import \
    ProductData, CouponData, GladMindUsers

from gladminds.aftersell.models.common import RegisteredDealer,\
    ServiceAdvisorDealerRelationship, ServiceAdvisor
from datetime import datetime, timedelta
from integration.base_integration import GladmindsResourceTestCase
from gladminds import feed
import xml.etree.ElementTree as ET
from django.utils import unittest

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
        self.assertEquals(3, RegisteredDealer.objects.count())
        dealer_data = RegisteredDealer.objects.all()[0]
        self.assertEquals(u"GMDEALER001", dealer_data.dealer_id)
        service_advisors = ServiceAdvisor.objects.filter(service_advisor_id='GMDEALER001SA01')
        self.assertEquals(1, len(service_advisors))
        self.assertEquals(u"GMDEALER001SA01", service_advisors[0].service_advisor_id)

    def test_service_advisor_dealer_relationship(self):
        file_path = os.path.join(settings.BASE_DIR, 'tests/integration/service_advisor_feed.xml')
        xml_data = open(file_path, 'r').read()
        response = self.client.post('/api/v1/bajaj/feed/?wsdl', data=xml_data, content_type='text/xml')
        self.assertEqual(200, response.status_code)
        sa_dealer_rel_data = ServiceAdvisorDealerRelationship.objects.all()

        self.assertEquals(3, len(sa_dealer_rel_data))

        self.assertEquals(3, ServiceAdvisor.objects.count())

        sa_obj_1 = ServiceAdvisor.objects.filter(service_advisor_id='GMDEALER001SA01')

        dealer_obj_1 = RegisteredDealer.objects.filter(dealer_id='GMDEALER001')
        sa_dealer_rel_obj_1 = ServiceAdvisorDealerRelationship.objects.get(service_advisor_id=sa_obj_1[0], dealer_id=dealer_obj_1[0])
        self.assertEquals('Y', sa_dealer_rel_obj_1.status)

        sa_obj_2 = ServiceAdvisor.objects.filter(service_advisor_id='GMDEALER001SA02')

        dealer_obj_2 = RegisteredDealer.objects.filter(dealer_id='GMDEALER002')
        sa_dealer_rel_obj_2 = ServiceAdvisorDealerRelationship.objects.get(service_advisor_id=sa_obj_2[0], dealer_id=dealer_obj_2[0])
        self.assertEquals('Y', sa_dealer_rel_obj_2.status)

        '''
            Checking out with new feed to change the status of service advisor
        '''

        file_path = os.path.join(settings.BASE_DIR, 'tests/integration/service_advisor_feed_2.xml')
        xml_data = open(file_path, 'r').read()
        response = self.client.post('/api/v1/bajaj/feed/?wsdl', data=xml_data, content_type='text/xml')
        self.assertEqual(200, response.status_code)

        sa_obj_1 = ServiceAdvisor.objects.filter(service_advisor_id='GMDEALER001SA01')

        dealer_obj_1 = RegisteredDealer.objects.filter(dealer_id='GMDEALER001')
        sa_dealer_rel_obj_1 = ServiceAdvisorDealerRelationship.objects.get(service_advisor_id=sa_obj_1[0], dealer_id=dealer_obj_1[0])
        self.assertEquals('N', sa_dealer_rel_obj_1.status)

        sa_obj_2 = ServiceAdvisor.objects.filter(service_advisor_id='GMDEALER001SA02')

        dealer_obj_2 = RegisteredDealer.objects.filter(dealer_id='GMDEALER002')
        sa_dealer_rel_obj_2 = ServiceAdvisorDealerRelationship.objects.get(service_advisor_id=sa_obj_2[0], dealer_id=dealer_obj_2[0])
        self.assertEquals('N', sa_dealer_rel_obj_2.status)

        dealer_obj_3 = RegisteredDealer.objects.filter(dealer_id='GMDEALER003')
        sa_dealer_rel_obj_2 = ServiceAdvisorDealerRelationship.objects.get(service_advisor_id=sa_obj_2[0], dealer_id=dealer_obj_3[0])
        self.assertEquals('Y', sa_dealer_rel_obj_2.status)

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

        self.assertEquals(2, CouponData.objects.count())
        coupon_data = CouponData.objects.all()[0]
        self.assertEquals(u"USC001", coupon_data.unique_service_coupon) 

    def test_product_purchase(self):
        file_path = os.path.join(settings.BASE_DIR, 'tests/integration/product_purchase_feed.xml')
        xml_data = open(file_path, 'r').read()
        response = self.client.post('/api/v1/bajaj/feed/?wsdl', data=xml_data,content_type='text/xml')
        self.assertEqual(200, response.status_code)

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

        self.assertEqual(CouponData.objects.count(), 2, "Two coupon created")

        coupon_data = CouponData.objects.filter(unique_service_coupon='USC001')[0]
        self.assertEquals(u"USC001", coupon_data.unique_service_coupon)
        coupon_data.status = 2
        coupon_data.closed_date = datetime.now()
        coupon_data.actual_service_date = datetime.now()
        coupon_data.save()

        today = datetime.now()
        start_date = today - timedelta(days=1)
        end_date = today
        redeem_obj = feed.CouponRedeemFeedToSAP()
        feed_export_data = redeem_obj.export_data(start_date=start_date, end_date=end_date)

        self.assertEqual(len(feed_export_data[0]), 1, "Not accurate length of feeds log")
        self.assertEqual(feed_export_data[0][0]["GCP_UCN_NO"], u'USC001', "Not accurate UCN")

    def test_partial_fail(self):
        file_path = os.path.join(settings.BASE_DIR, 'tests/integration/without_sa_id_sa_feed.xml')
        xml_data = open(file_path, 'r').read()
        response = self.client.post('/api/v1/bajaj/feed/?wsdl', data=xml_data,content_type='text/xml')
        self.assertEqual(200, response.status_code)

        response_content = response.content
        xml_parser = ET.fromstring(response_content)

        status = xml_parser.findall('*//{http://api.gladmindsplatform.co/api/v1/bajaj/feed/}postDealerResult')[0].text
        self.assertEqual(status, 'FAILURE')

    def test_update_customer_number(self):
        file_path = os.path.join(settings.BASE_DIR, 'tests/integration/product_dispatch_feed.xml')
        xml_data = open(file_path, 'r').read()
        response = self.client.post('/api/v1/bajaj/feed/?wsdl', data=xml_data, content_type='text/xml')
        self.assertEqual(200, response.status_code)

        file_path = os.path.join(settings.BASE_DIR, 'tests/integration/product_purchase_feed.xml')
        xml_data = open(file_path, 'r').read()
        response = self.client.post('/api/v1/bajaj/feed/?wsdl', data=xml_data, content_type='text/xml')
        self.assertEqual(200, response.status_code)
        gm_user = GladMindUsers.objects.all()
        self.assertEqual(1, len(gm_user))

        file_path = os.path.join(settings.BASE_DIR, 'tests/integration/purchase_feed_with_diff_cust_num.xml')
        xml_data = open(file_path, 'r').read()
        response = self.client.post('/api/v1/bajaj/feed/?wsdl', data=xml_data, content_type='text/xml')
        self.assertEqual(200, response.status_code)
        gm_user = GladMindUsers.objects.all()
        self.assertEqual(gm_user[0].phone_number, "+919845340297", "Customer Phone Number is not updated")
        self.assertEqual(GladMindUsers.objects.count(), 1, "Total GM User")

    def test_authentication(self):
        user = User.objects.create_user('testuser', 'testuserpassword@gladminds.co', 'testuserpassword')
        user.save()

        file_path = os.path.join(settings.BASE_DIR, 'tests/integration/feeds_for_testing_auth.xml')
        xml_data = open(file_path, 'r').read()
        response = self.client.post('/api/v1/bajaj/feed/?wsdl', data=xml_data,content_type='text/xml')
        self.assertEqual(200, response.status_code)

    @unittest.skip("Skipping Adding this functionality in future")
    def test_coupon_status_on_dispatch_feed(self):
        '''
            Test for testing out coupon status on dispatch feed
            Its default value is 1
        '''
        file_path = os.path.join(settings.BASE_DIR, 'tests/integration/product_dispatch_feed.xml')
        xml_data = open(file_path, 'r').read()
        response = self.client.post('/api/v1/bajaj/feed/?wsdl', data=xml_data, content_type='text/xml')
        self.assertEqual(200, response.status_code)

        self.assertEquals(2, CouponData.objects.count())
        coupon_data = CouponData.objects.all()[0]
        self.assertEquals(u"USC001", coupon_data.unique_service_coupon)
        self.assertEquals(2, coupon_data.status)

        coupon_data = CouponData.objects.all()[1]
        self.assertEquals(u"USC002", coupon_data.unique_service_coupon)
        self.assertEquals(1, coupon_data.status, 'Default value should be 1')

    def test_coupon_status_without_ucn(self):
        '''
            Test for testing out dispatch feed without_ucn
        '''
        file_path = os.path.join(settings.BASE_DIR, 'tests/integration/product_dispatch_feed_without_ucn.xml')
        xml_data = open(file_path, 'r').read()
        response = self.client.post('/api/v1/bajaj/feed/?wsdl', data=xml_data, content_type='text/xml')
        self.assertEqual(200, response.status_code)

        self.assertEquals(1, CouponData.objects.count())
        coupon_data = CouponData.objects.all()[0]
        self.assertEquals(u"USC002", coupon_data.unique_service_coupon)
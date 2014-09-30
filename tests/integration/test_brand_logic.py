import logging

from gladminds.models import common
import xml.etree.ElementTree as ET
from django.db import transaction
from gladminds.aftersell.models import common as aftersell_common
import os
from django.conf import settings
from gladminds.core import feed
from datetime import datetime, timedelta

from django.test.client import Client


client = Client()

logger = logging.getLogger('gladminds')

# base_test = BaseTestCase()


class Brand(object):
    def __init__(self, tester):
        self.tester = tester

    def send_purchase_feed(self):
        file_path = os.path.join(settings.BASE_DIR, 'tests/integration/product_purchase_feed.xml')
        self.post_feed(file_path)

    def send_purchase_feed_with_diff_cust_num(self):
        file_path = os.path.join(settings.BASE_DIR, 'tests/integration/purchase_feed_with_diff_cust_num.xml')
        self.post_feed(file_path)

    def check_for_auth(self):
        file_path = os.path.join(settings.BASE_DIR, 'tests/integration/feeds_for_testing_auth.xml')
        self.post_feed(file_path)

    def send_as_feed_without_id(self):
        file_path = os.path.join(settings.BASE_DIR, 'tests/integration/without_sa_id_sa_feed.xml')
        xml_data = open(file_path, 'r').read()
        with transaction.atomic():
            response = self.tester.client.post('/api/v1/bajaj/feed/?wsdl', data=xml_data,content_type='text/xml')
            self.tester.assertEqual(200, response.status_code)

        response_content = response.content
        xml_parser = ET.fromstring(response_content)
        with transaction.atomic():
            status = xml_parser.findall('*//{http://api.gladmindsplatform.co/api/v1/bajaj/feed/}postDealerResult')[0].text
            self.tester.assertEqual(status, 'SUCCESS')

    def send_sa_upate_mobile_feed(self):
        file_path = os.path.join(settings.BASE_DIR, 'tests/integration/SA_mobile_update_data/SA_update_mobile_feed.xml')
        self.post_feed(file_path)

    def send_dispatch_feed(self):
        file_path = os.path.join(settings.BASE_DIR, 'tests/integration/product_dispatch_feed.xml')
        self.post_feed(file_path)

    def send_dispatch_feed_without_ucn(self):
        file_path = os.path.join(settings.BASE_DIR, 'tests/integration/product_dispatch_feed_without_ucn.xml')
        self.post_feed(file_path)

    def send_asc_feed(self):
        file_path = os.path.join(settings.BASE_DIR, 'tests/integration/asc_feed.xml')
        self.post_feed(file_path)

    def send_service_advisor_feed(self):
        file_path = os.path.join(settings.BASE_DIR, 'tests/integration/service_advisor_feed.xml')
        self.post_feed(file_path)

    def send_service_advisor_feed_with_new_status(self):
        file_path = os.path.join(settings.BASE_DIR, 'tests/integration/service_advisor_feed_2.xml')
        self.post_feed(file_path)

    def post_feed(self, file_path):
        xml_data = open(file_path, 'r').read()
        response = self.tester.client.post('/api/v1/bajaj/feed/?wsdl', data=xml_data, content_type='text/xml')
        self.tester.assertEqual(200, response.status_code)

    def send_check_message(self, **kwargs):
        response = client.post(kwargs['url'], kwargs['message'])
        return response

    def check_coupon_status(self, **kwargs):
        coupon_status = common.CouponData.objects.get(unique_service_coupon=kwargs['unique_service_coupon'])
        return coupon_status

    def get_coupon_obj(self, **kwargs):
        coupon_obj = common.CouponData(**kwargs)
        coupon_obj.save()
        return coupon_obj

    def get_product_obj(self, **kwargs):
        product_data = common.ProductData.objects.get(**kwargs)
        return product_data

    def check_asc_feed_saved_to_database(self):
        self.send_asc_feed()
        asc = aftersell_common.RegisteredDealer.objects.get(dealer_id='ASC001')
        self.tester.assertEquals('ASC001', asc.dealer_id)

    def check_service_feed_saved_to_database(self):
        self.tester.assertEquals(3, aftersell_common.RegisteredDealer.objects.count())
        dealer_data = aftersell_common.RegisteredDealer.objects.all()[0]
        self.tester.assertEquals(u"GMDEALER001", dealer_data.dealer_id)
        service_advisors = aftersell_common.ServiceAdvisor.objects.filter(service_advisor_id='GMDEALER001SA01')
        self.tester.assertEquals(1, len(service_advisors))
        self.tester.assertEquals(u"GMDEALER001SA01", service_advisors[0].service_advisor_id)

    def check_service_advisor_dealer_relationship_saved_to_database(self):
        sa_dealer_rel_data = aftersell_common.ServiceAdvisorDealerRelationship.objects.all()
        self.tester.assertEquals(3, len(sa_dealer_rel_data))
        self.tester.assertEquals(3, aftersell_common.ServiceAdvisor.objects.count())
        sa_obj_1 = aftersell_common.ServiceAdvisor.objects.filter(service_advisor_id='GMDEALER001SA01')
        dealer_obj_1 = aftersell_common.RegisteredDealer.objects.filter(dealer_id='GMDEALER001')
        sa_dealer_rel_obj_1 = aftersell_common.ServiceAdvisorDealerRelationship.objects.get(service_advisor_id=sa_obj_1[0], dealer_id=dealer_obj_1[0])
        self.tester.assertEquals('Y', sa_dealer_rel_obj_1.status)
        sa_obj_2 = aftersell_common.ServiceAdvisor.objects.filter(service_advisor_id='GMDEALER001SA02')
        dealer_obj_2 = aftersell_common.RegisteredDealer.objects.filter(dealer_id='GMDEALER002')
        sa_dealer_rel_obj_2 = aftersell_common.ServiceAdvisorDealerRelationship.objects.get(service_advisor_id=sa_obj_2[0], dealer_id=dealer_obj_2[0])
        self.tester.assertEquals('Y', sa_dealer_rel_obj_2.status)

    def check_data_saved_to_database(self):
        sa_obj_1 = aftersell_common.ServiceAdvisor.objects.filter(service_advisor_id='GMDEALER001SA01')
        self.tester.assertEquals('+9155555', sa_obj_1[0].phone_number)
        dealer_obj_1 = aftersell_common.RegisteredDealer.objects.filter(dealer_id='GMDEALER001')
        sa_dealer_rel_obj_1 = aftersell_common.ServiceAdvisorDealerRelationship.objects.get(service_advisor_id=sa_obj_1[0], dealer_id=dealer_obj_1[0])
        self.tester.assertEquals('N', sa_dealer_rel_obj_1.status)
        sa_obj_2 = aftersell_common.ServiceAdvisor.objects.filter(service_advisor_id='GMDEALER001SA02')
        dealer_obj_2 = aftersell_common.RegisteredDealer.objects.filter(dealer_id='GMDEALER002')
        sa_dealer_rel_obj_2 = aftersell_common.ServiceAdvisorDealerRelationship.objects.get(service_advisor_id=sa_obj_2[0], dealer_id=dealer_obj_2[0])
        self.tester.assertEquals('Y', sa_dealer_rel_obj_2.status)

    def coupon_data_saved_to_database(self):
        self.tester.assertEqual(common.CouponData.objects.count(), 2, "Two coupon created")
        coupon_data = common.CouponData.objects.filter(unique_service_coupon='USC001')[0]
        self.tester.assertEquals(u"USC001", coupon_data.unique_service_coupon)
        coupon_data.status = 2
        coupon_data.closed_date = datetime.now()
        coupon_data.actual_service_date = datetime.now()
        coupon_data.save()

        today = datetime.now()
        start_date = today - timedelta(days=1)
        end_date = today
        redeem_obj = feed.CouponRedeemFeedToSAP()
        feed_export_data = redeem_obj.export_data(start_date=start_date, end_date=end_date)

        self.tester.assertEqual(len(feed_export_data[0]), 1, "Not accurate length of feeds log")
        self.tester.assertEqual(feed_export_data[0][0]["GCP_UCN_NO"], u'USC001', "Not accurate UCN")

    def check_product_data_saved_to_database(self):
        self.tester.assertEquals(1, common.ProductData.objects.count())
        product_data = common.ProductData.objects.all()[0]
        self.tester.assertEquals(u"XXXXXXXXXX", product_data.vin)
        self.tester.assertEquals(2, common.CouponData.objects.count())
        coupon_data = common.CouponData.objects.all()[0]
        self.tester.assertEquals(u"USC001", coupon_data.unique_service_coupon)

    def service_advisor_database_upadted(self):
        sa_obj_1 = aftersell_common.ServiceAdvisor.objects.filter(service_advisor_id='GMDEALER001SA01')
        dealer_obj_1 = aftersell_common.RegisteredDealer.objects.filter(dealer_id='GMDEALER001')
        self.tester.assertEquals('+9112345', sa_obj_1[0].phone_number)
        sa_dealer_rel_obj_2 = aftersell_common.ServiceAdvisorDealerRelationship.objects.get(service_advisor_id=sa_obj_1[0], dealer_id=dealer_obj_1[0])
        self.tester.assertEquals('N', sa_dealer_rel_obj_2.status)
        sa_obj_2 = aftersell_common.ServiceAdvisor.objects.filter(service_advisor_id='GMDEALER001SA02')
        dealer_obj_2 = aftersell_common.RegisteredDealer.objects.filter(dealer_id='GMDEALER002')
        self.tester.assertEquals('+91555551', sa_obj_2[0].phone_number)
        dealer_obj_3 = aftersell_common.RegisteredDealer.objects.filter(dealer_id='GMDEALER003')
        sa_obj_3 = aftersell_common.ServiceAdvisor.objects.filter(service_advisor_id='GMDEALER001SA03')
        self.tester.assertEquals(0, len(sa_obj_3))
        self.tester.assertEquals(0, len(dealer_obj_3))


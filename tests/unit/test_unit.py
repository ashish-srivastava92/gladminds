import os
import json

from django.conf import settings
from django.contrib.auth.models import User
from tastypie.test import ResourceTestCase
from django.test import TestCase
from datetime import datetime, timedelta
from unit.base_unit import RequestObject, GladmindsUnitTestCase
from gladminds.utils import get_sa_list, get_coupon_info, get_customer_info, get_token, validate_otp
from gladminds.aftersell.models import logs
from django.db import connection
import boto


class TestAssertWorks(TestCase):

    def test_assert_equals(self):
        self.assertEquals(100, 100, '100 == 100')

    def test_assert_true(self):
        self.assertTrue(100 > 1, '100 > 1')


class TestUtils(GladmindsUnitTestCase):

    def setUp(self):
        super(TestUtils, self).setUp()
        brand_obj = self.get_brand_obj(brand_id='brand001', brand_name='bajaj')
        product_type_obj = self.get_product_type_obj(
            brand_id=brand_obj, product_name='DISCO120', product_type='BIKE')
        dealer_obj = self.get_delear_obj(dealer_id='DEALER001')
        customer_obj = self.get_customer_obj(phone_number='+919999999', customer_name='TestCustomer')
        product_obj = self.get_product_obj(vin="VINXXX001", product_type=product_type_obj, dealer_id=dealer_obj\
                                           , customer_phone_number=customer_obj, sap_customer_id='SAP001'\
                                           , product_purchase_date=datetime.now())
        service_advisor = self.get_service_advisor_obj(service_advisor_id='SA001Test', name='UMOTO', phone_number='+914444861111')
        self.get_dealer_service_advisor_obj(dealer_id=dealer_obj, service_advisor_id=service_advisor, status='Y')
        self.get_coupon_obj(unique_service_coupon='COUPON005', vin=product_obj, valid_days=30, valid_kms=500\
                            , service_type=1, status=4, mark_expired_on=datetime.now() - timedelta(days=2)\
                            , actual_service_date=datetime.now() - timedelta(days=20), extended_date=datetime.now() - timedelta(days=2))
        self.get_message_template(template_key='SEND_CUSTOMER_VALID_COUPON'\
                                  , template='Service Type {service_type}. UCN {coupon}.', description='Desc')
        asc_user = User(username='ASC001')
        asc_user.set_password('123')
        asc_user.save()
        self.get_asc_obj(user=asc_user, phone_number="+911234567890")


    def test_get_sa_list(self):
        request = RequestObject(user='DEALER001', data={
                                'customerId': 'SAP001', 'vin': 'VINXXX001'}, file={'jobCard': ''})
        sa_list = get_sa_list(request)
        self.assertEqual(len(sa_list), 1)
        coupon_info = get_coupon_info(request)
        self.assertEqual(coupon_info.keys(), ['status', 'message'])
        customer = get_customer_info(request)
        self.assertEquals(len(customer.keys()), 4)

    def test_otp(self):
        phone_number = '1234567890'
        token = get_token(phone_number)
        self.assertTrue(isinstance(token, int))
        self.assertTrue(validate_otp(token, phone_number))


class TestFeedLogWithRemark(ResourceTestCase):
    '''
    '''

    def setUp(self):
        TestCase.setUp(self)
        user = User.objects.create_user('gladminds', 'gladminds@gladminds.co',
                                         'gladminds')
        user.save()

    def test_remarks(self):
        file_path = os.path.join(settings.BASE_DIR,
                                 'etc/test_data/unit/test_feed_log_remark.xml')
        xml_data = open(file_path, 'r').read()
        self.client.post('/api/v1/bajaj/feed/?wsdl', data=xml_data,
                                    content_type='text/xml')

        feed_logs_obj = logs.DataFeedLog.objects.all()
        self.assertEqual(len(feed_logs_obj), 1)
        remark = json.loads(feed_logs_obj[0].remarks)
        self.assertEqual(len(remark), 1)
        file_name = feed_logs_obj[0].file_location.split("/")[-1]
        
        
        self.assertEqual(os.path.isfile("{0}/{1}".format(settings.BASE_DIR, file_name)), 
                         False, 'File should be deleted from local dir')
                             
        connection = boto.connect_s3(settings.S3_ID, settings.S3_KEY)
        s3_bucket = connection.get_bucket('gladminds')
                             
        file_uploaded_on_s3 = False
        for key in s3_bucket.list('aftersell/bajaj/feed-logs/dev'):
            uploaded_file = key.name.split("/")[-1]
            if uploaded_file == file_name:
                file_uploaded_on_s3=True 
        self.assertEqual(file_uploaded_on_s3, True, 'File is not Uploaded On S3')    
            
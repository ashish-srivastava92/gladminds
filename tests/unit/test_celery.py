from integration.base_integration import GladmindsResourceTestCase
from django.test.utils import override_settings
from gladminds.core.cron_jobs import sqs_tasks
from gladminds.core.cron_jobs.sqs_tasks import expire_service_coupon
from datetime import datetime, timedelta
from unit.base_unit import GladmindsUnitTestCase
from gladminds.core.utils import COUPON_STATUS
from gladminds.core.cron_jobs.taskmanager import get_data_feed_log_detail
from gladminds.bajaj import models as common
from gladminds.gm import models as gm_common
from gladminds.bajaj import models as aftersell_common
from django.db.models import Q
import time


class TestCelery(GladmindsResourceTestCase):

    @override_settings(CELERY_EAGER_PROPAGATES_EXCEPTIONS=True,
                       CELERY_ALWAYS_EAGER=True,
                       BROKER_BACKEND='django')
    def test_send_sms(self):
        result = sqs_tasks.send_service_detail.delay(
            phone_number='99999999', message='Test Message')
        self.assertTrue(result.successful())

    @override_settings(SMS_CLIENT="MOCK_FAIL")
    def test_send_sms_fail(self):
        result = sqs_tasks.send_service_detail.delay(
            phone_number='99999999', message='Test Message')
        self.assertFalse(result.successful())


class TestCronjobs(GladmindsUnitTestCase):
 
    def setUp(self):
        product_type_obj = self.get_product_type_obj(
            product_name='DISCO120', product_type='BIKE')
        dealer_obj = self.get_delear_obj(name='DEALER001')
        product_obj = self.get_product_obj(product_id="VINXXX001", product_type=product_type_obj,
                                           dealer_id=dealer_obj, customer_phone_number='+911111111111', 
                                           customer_name='test_user1', customer_id='SAP001')
        service_advisor = self.get_service_advisor_obj(
            service_advisor_id='SA001Test', name='UMOTO', phone_number='+914444861111')
        self.get_dealer_service_advisor_obj(
            dealer_id=dealer_obj, service_advisor_id=service_advisor, status='Y')
        service_advisor1 = self.get_service_advisor_obj(
            service_advisor_id='SA002Test', name='UMOTOR', phone_number='+919999999999')
        self.get_dealer_service_advisor_obj(
            dealer_id=dealer_obj, service_advisor_id=service_advisor1, status='Y')
        self.get_coupon_obj(unique_service_coupon='COUPON005', product=product_obj, valid_days=30, valid_kms=500,
                            service_type=1, mark_expired_on=datetime.now() + timedelta(days=1), status=COUPON_STATUS['Unused'])
        product_obj1 = self.get_product_obj(product_id="VINXXX002", product_type=product_type_obj,
                                            dealer_id=dealer_obj, customer_phone_number='8888888',
                                            customer_name='test_user2', customer_id='SAP002')
        self.get_coupon_obj(unique_service_coupon='COUPON004', actual_service_date=datetime.now() - timedelta(days=10), product=product_obj1,
                            valid_days=30, valid_kms=500, service_type=1, mark_expired_on=datetime.now() - timedelta(days=1), status=COUPON_STATUS['In Progress']\
                            ,extended_date=datetime.now()+timedelta(days=2))
        self.get_coupon_obj(unique_service_coupon='COUPON006', actual_service_date=datetime.now() - timedelta(days=40), product=product_obj,
                            valid_days=30, valid_kms=3000, service_type=2, mark_expired_on=datetime.now() - timedelta(days=1), status=COUPON_STATUS['In Progress']\
                            , extended_date=datetime.now()+timedelta(days=20))
        self.get_coupon_obj(unique_service_coupon='COUPON007', product=product_obj, valid_days=30, valid_kms=6000,
                            service_type=3, mark_expired_on=datetime.now() - timedelta(days=1), status=COUPON_STATUS['Unused'])
        self.get_coupon_obj(unique_service_coupon='COUPON008', product=product_obj, valid_days=30, valid_kms=6000,
                            service_type=3, mark_expired_on=datetime.now() - timedelta(days=10), status=COUPON_STATUS['In Progress']\
                            ,extended_date=datetime.now()-timedelta(days=2))
         
    def test_expire_service_coupon(self):
        expire_service_coupon()
        self.assertEqual(
            self.filter_coupon_obj('COUPON004').status, COUPON_STATUS['In Progress'])
        self.assertEqual(
            self.filter_coupon_obj('COUPON005').status, COUPON_STATUS['Unused'])
        self.assertEqual(
            self.filter_coupon_obj('COUPON006').status, COUPON_STATUS['In Progress'])
        self.assertEqual(
            self.filter_coupon_obj('COUPON007').status, COUPON_STATUS['Expired'])
        self.assertEqual(
            self.filter_coupon_obj('COUPON008').status, COUPON_STATUS['Expired'])


    def test_get_data_feed_log_detail(self):
        obj = self.get_datafeed_log(feed_type="Dispatch Feed",total_data_count=4,failed_data_count=0\
                                    ,success_data_count=4,timestamp=datetime.now(),action='Recieved', status='success')
        feeds = get_data_feed_log_detail(start_date=datetime.now()-timedelta(days=1), end_date=datetime.now()+timedelta(days=1))
        self.assertEqual(len(feeds), 1)
    
class TestTasks(GladmindsUnitTestCase):
    def setUp(self):
        super(TestTasks, self).setUp()
        self.phone_number = '+T0{0}'.format(str(time.time()))
        self.message = 'Thankyou message'
    
    def test_tasks(self):
        sqs_tasks.send_registration_detail(message=self.message,phone_number=self.phone_number)
        sqs_tasks.send_service_detail(message=self.message,phone_number=self.phone_number)
        sqs_tasks.send_coupon_validity_detail(message=self.message,phone_number=self.phone_number)
        sqs_tasks.send_coupon_detail_customer(message=self.message,phone_number=self.phone_number)
        sqs_tasks.send_reminder_message(message=self.message,phone_number=self.phone_number)
        sqs_tasks.send_coupon_close_message(message=self.message,phone_number=self.phone_number)
        sqs_tasks.send_coupon(message=self.message,phone_number=self.phone_number)
        sqs_tasks.send_close_sms_customer(message=self.message,phone_number=self.phone_number)
        sqs_tasks.send_brand_sms_customer(message=self.message,phone_number=self.phone_number)
        sqs_tasks.send_invalid_keyword_message(message=self.message,phone_number=self.phone_number)
        sqs_tasks.send_on_product_purchase(message=self.message,phone_number=self.phone_number)
        
    
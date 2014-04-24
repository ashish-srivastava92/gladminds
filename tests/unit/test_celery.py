from integration.base_integration import GladmindsResourceTestCase
from django.test.utils import override_settings
from gladminds.tasks import send_service_detail, expire_service_coupon
from datetime import datetime, timedelta
from unit.base_unit import GladmindsUnitTestCase
from gladminds.utils import COUPON_STATUS
from gladminds.taskmanager import get_data_feed_log_detail
from gladminds.models import common
from django.db.models import Q


class TestCelery(GladmindsResourceTestCase):

    @override_settings(CELERY_EAGER_PROPAGATES_EXCEPTIONS=True,
                       CELERY_ALWAYS_EAGER=True,
                       BROKER_BACKEND='django')
    def test_send_sms(self):
        result = send_service_detail.delay(
            phone_number='99999999', message='Test Message')
        self.assertTrue(result.successful())

    @override_settings(SMS_CLIENT="MOCK_FAIL")
    def test_send_sms_fail(self):
        result = send_service_detail.delay(
            phone_number='99999999', message='Test Message')
        self.assertFalse(result.successful())


class TestCronjobs(GladmindsUnitTestCase):

    def setUp(self):
        brand_obj = self.get_brand_obj(brand_id='brand001', brand_name='bajaj')
        product_type_obj = self.get_product_type_obj(
            brand_id=brand_obj, product_name='DISCO120', product_type='BIKE')
        dealer_obj = self.get_delear_obj(dealer_id='DEALER001')
        customer_obj = self.get_customer_obj(phone_number='9999999')
        product_obj = self.get_product_obj(vin="VINXXX001", product_type=product_type_obj,
                                           dealer_id=dealer_obj, customer_phone_number=customer_obj, sap_customer_id='SAP001')
        service_advisor = self.get_service_advisor_obj(
            service_advisor_id='SA001Test', name='UMOTO', phone_number='+914444861111')
        self.get_dealer_service_advisor_obj(
            dealer_id=dealer_obj, service_advisor_id=service_advisor, status='Y')
        service_advisor1 = self.get_service_advisor_obj(
            service_advisor_id='SA002Test', name='UMOTOR', phone_number='+919999999999')
        self.get_dealer_service_advisor_obj(
            dealer_id=dealer_obj, service_advisor_id=service_advisor1, status='Y')
        self.get_coupon_obj(unique_service_coupon='COUPON005', vin=product_obj, valid_days=30, valid_kms=500,
                            service_type=1, mark_expired_on=datetime.now() + timedelta(days=1), status=COUPON_STATUS['Unused'])
        customer_obj1 = self.get_customer_obj(phone_number='8888888')
        product_obj1 = self.get_product_obj(vin="VINXXX002", product_type=product_type_obj,
                                            dealer_id=dealer_obj, customer_phone_number=customer_obj1, sap_customer_id='SAP002')
        self.get_coupon_obj(unique_service_coupon='COUPON004', actual_service_date=datetime.now() - timedelta(days=10), vin=product_obj1,
                            valid_days=30, valid_kms=500, service_type=1, mark_expired_on=datetime.now() - timedelta(days=1), status=COUPON_STATUS['In Progress']\
                            ,extended_date=datetime.now()+timedelta(days=2))
        self.get_coupon_obj(unique_service_coupon='COUPON006', actual_service_date=datetime.now() - timedelta(days=40), vin=product_obj,
                            valid_days=30, valid_kms=3000, service_type=2, mark_expired_on=datetime.now() - timedelta(days=1), status=COUPON_STATUS['In Progress']\
                            , extended_date=datetime.now()+timedelta(days=20))
        self.get_coupon_obj(unique_service_coupon='COUPON007', vin=product_obj, valid_days=30, valid_kms=6000,
                            service_type=3, mark_expired_on=datetime.now() - timedelta(days=1), status=COUPON_STATUS['Unused'])
        self.get_coupon_obj(unique_service_coupon='COUPON008', vin=product_obj, valid_days=30, valid_kms=6000,
                            service_type=3, mark_expired_on=datetime.now() - timedelta(days=10), status=COUPON_STATUS['In Progress']\
                            ,extended_date=datetime.now()-timedelta(days=2))
        
    
    def tearDown(self):
        common.BrandData.objects.filter(brand_id='brand001').delete()
        common.RegisteredDealer.objects.filter(dealer_id='DEALER001').delete()
        common.GladMindUsers.objects.filter(Q(phone_number='9999999')|Q(phone_number='8888888')).delete()
        common.ServiceAdvisor.objects.filter(Q(service_advisor_id='SA001Test')|Q(service_advisor_id='SA002Test')).delete()

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
                                    ,success_data_count=4,timestamp=datetime.now(),action='Recieved')
        feeds = get_data_feed_log_detail(start_date=datetime.now()-timedelta(days=1), end_date=datetime.now()+timedelta(days=1))
        self.assertEqual(len(feeds), 1)
    

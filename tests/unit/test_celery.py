from integration.bajaj.base_integration import BrandResourceTestCase
from django.test.utils import override_settings
from gladminds import sqs_tasks
from unit.base_unit import GladmindsUnitTestCase
import time


class TestCelery(BrandResourceTestCase):

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
        
    
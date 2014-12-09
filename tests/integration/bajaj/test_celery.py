'''
    Test cases for testing Celery Jobs
'''
from celery.app.task import Task
import logging
from django.conf import settings 
from django.test.client import Client
from integration.bajaj import base_integration

logger = logging.getLogger('gladminds')
client=Client(SERVER_NAME='bajaj')


class CeleryTestCaseBase(base_integration.BrandResourceTestCase):
    def setUp(self):
        super(CeleryTestCaseBase, self).setUp()
        self.applied_tasks = []
        Task.apply_async = self.mock_apply_async
        logger.info(Task.apply_async)

    def tearDown(self):
        super(CeleryTestCaseBase, self).tearDown()

    def mock_apply_async(self, args=None, kwargs=None, task_id=None, producer=None,
                    link=None, link_error=None, **options):
        self.applied_tasks.append({"kwargs":kwargs, "options":options})
        return kwargs
    
    def validate_coupon(self, data, phone_number):
        data = 'A {1} {0} {2}'.format(data['kms'], data['sap_customer_id'], data['service_type'])
        result = client.post('/v1/messages', data={'text': data, 'phoneNumber' : phone_number})
        self.assertHttpOK(result)
        
    def test_delay_message(self):
        product_type_obj = self.get_product_type_obj(product_type='BIKE')
        self.dealer_obj = self.get_delear_obj(name='DEALER001', phone_number='+911111111111')
        self.product_obj = self.get_product_obj(product_id="VINXXX001", product_type=product_type_obj, dealer_id = self.dealer_obj, customer_phone_number = '232323232', customer_id='SAP001')
        self.get_coupon_obj(unique_service_coupon='USC001', product=self.product_obj, valid_days=30, valid_kms=500, service_type=1)

        sa_obj = self.get_service_advisor_obj(service_advisor_id='DEALER001SA001', name="SA001", phone_number='+919999999')
        self.get_dealer_service_advisor_obj(dealer_id=self.dealer_obj, service_advisor_id=sa_obj, status='Y')

        phone_number = "9999999"
        sms_dict = {'kms': 450, 'service_type': 1, 'sap_customer_id': 'SAP001'}
        self.validate_coupon(sms_dict, phone_number)

        customer_message_task_info = self.applied_tasks[1]
        self.assertEqual(customer_message_task_info['options']["countdown"], settings.DELAY_IN_CUSTOMER_UCN_MESSAGE, 'Set delay in celery job')
        self.assertEqual(customer_message_task_info['kwargs']["phone_number"], "232323232", 'Customer phone number should be correct')

        self.applied_tasks = []

'''
    Test cases for testing Celery Jobs
'''
from celery.app.task import Task
import logging
from gladminds.resource.resources import GladmindsResources
from gladminds.models import common
from gladminds.tasks import send_coupon_detail_customer
logger = logging.getLogger('gladminds')
from integration.base_integration import GladmindsResourceTestCase


class CeleryTestCaseBase(GladmindsResourceTestCase):
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

    def test_delay_message(self):
        self.brand_obj = self.get_brand_obj(brand_id='brand001', brand_name='bajaj')
        product_type_obj = self.get_product_type_obj(brand_id=self.brand_obj, product_name='DISCO120', product_type='BIKE')
        self.dealer_obj = self.get_delear_obj(dealer_id='DEALER001')
        self.customer_obj = self.get_customer_obj(phone_number='232323232')
        self.product_obj = self.get_product_obj(vin="VINXXX001", product_type=product_type_obj, dealer_id = self.dealer_obj, customer_phone_number = self.customer_obj, sap_customer_id='SAP001')
        self.get_coupon_obj(unique_service_coupon='USC001', vin=self.product_obj, valid_days=30, valid_kms=500, service_type=1)

        sa_obj = self.get_service_advisor_obj(service_advisor_id='DEALER001SA001', name="SA001", phone_number='9999999')
        self.get_dealer_service_advisor_obj(dealer_id=self.dealer_obj, service_advisor_id=sa_obj, status='Y')

        phone_number = "9999999"
        obj = GladmindsResources()
        sms_dict = {'kms': 450, 'service_type': 1, 'sap_customer_id': 'SAP001'}
        obj.validate_coupon(sms_dict, phone_number)

        customer_message_task_info = self.applied_tasks[1]
        self.assertEqual(customer_message_task_info['options']["countdown"], 1800, 'Set delay in celery job')
        self.assertEqual(customer_message_task_info['kwargs']["phone_number"], "232323232", 'Customer phone number should be correct')

        self.applied_tasks = []

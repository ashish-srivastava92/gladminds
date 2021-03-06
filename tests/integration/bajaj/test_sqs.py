from integration.bajaj import base_integration
from django.test.client import Client
import logging
import json

logger = logging.getLogger('gladminds')

client = Client()


class SQSTaskTest(base_integration.BrandResourceTestCase):

    def setUp(self):
        pass

    def _test_send_registration_detail(self):
        data = {
            "task_name": "send_registration_detail",
            "params": {
                "phone_number": "9845350297",
                "message": "Thanks for purchasing Bajaj Bike."
            }
         }
        result = client.post('/tasks/', data=json.dumps(data), \
                             content_type='application/json')
        self.assertEqual(result.status_code, 200, "Task Not Excecuted")

    def _test_send_service_detail(self):
        data = {
            "task_name": "send_service_detail",
            "params": {
                "phone_number": "9845350297",
                "message": "Please proceed for free service 1 for Customer ID SAP001"
            }
         }
        result = client.post('/tasks/', data=json.dumps(data), \
                             content_type='application/json')
        self.assertEqual(result.status_code, 200, "Task Not Excecuted")

    def test_send_on_product_purchase(self):
        data = {
            "task_name": "send_on_product_purchase",
            "params": {
                "brand": "bajaj",
                "phone_number": "9845350297",
                "message": "Dear testuser, Congrats on your purchase of Bajaj bike. Your customer id is 23232. Refer this id during servicing."
            }
         }
        result = client.post('/tasks/', data=json.dumps(data), \
                             content_type='application/json')
        self.assertEqual(result.status_code, 200, "Task Not Excecuted")

from integration import base_integration
from django.test.client import Client
import logging
import json

logger = logging.getLogger('gladminds')

client = Client()


class TestSQSTasks(base_integration.GladmindsResourceTestCase):

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


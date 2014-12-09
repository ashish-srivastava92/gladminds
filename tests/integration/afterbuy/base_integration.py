from django.test.client import Client
from tastypie.test import ResourceTestCase
from gladminds.management.commands import load_gm_migration_data, setup
import json


class AfterBuyResourceTestCase(ResourceTestCase):

    def setUp(self):
        super(AfterBuyResourceTestCase, self).setUp()
        load_email_obj = load_gm_migration_data.Command()
        load_email_obj.add_email_template()
        load_email_obj.add_sms_template()
        load_email_obj.add_group()
        setup_obj = setup.Command()
        setup_obj.handle()
        self.client = Client(SERVER_NAME='afterbuy')
        self.MESSAGE_URL = "/v1/messages"

    def post(self, uri, content_type='application/json', data=None):
        return self.client.post(uri, content_type=content_type, data=json.dumps(data))
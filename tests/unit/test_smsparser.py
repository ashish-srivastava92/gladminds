from gladminds import smsparser
import os
from gladminds.settings import BASE_DIR
import logging
import json
logger = logging.getLogger('test_case')
from gladminds.models import common
from tastypie.test import ResourceTestCase


class SmsParserTest(ResourceTestCase):

    def setUp(self):
        super(SmsParserTest, self).setUp()
        file_path = os.path.join(BASE_DIR, 'etc/data/template.json')
        message_templates = json.loads(open(file_path).read())
        for message_temp in message_templates:
            fields = message_temp['fields']
            temp_obj = common.MessageTemplate(template_key=fields['template_key']\
                       , template=fields['template'], description=fields['description'])
            temp_obj.save()
        self.assertEqual(len(message_templates), common.MessageTemplate.objects.count(), "Template is not saved on db")

    def test_sms_parse(self):
        mock_client_sms = "GCP_REG test.user@testcase.com Test User"
        test_args = smsparser.sms_parser(message=mock_client_sms)
        self.assertEqual(test_args['keyword'], 'gcp_reg')
        self.assertEqual(test_args['email_id'], 'test.user@testcase.com')
        self.assertEqual(test_args['name'], 'Test User')

    def test_invalid_message_format(self):
        with self.assertRaises(smsparser.InvalidFormat):
            mock_client_sms = "GCP_REG test.user@testcase.com"
            smsparser.sms_parser(message=mock_client_sms)

    def test_invalid_keyword(self):
        with self.assertRaises(smsparser.InvalidKeyWord):
            mock_client_sms = "ANNONYM test.user@testcase.com Test User"
            smsparser.sms_parser(message=mock_client_sms)

    def test_invalid_keyword_2(self):
        with self.assertRaises(smsparser.InvalidMessage):
            mock_client_sms = ""
            smsparser.sms_parser(message=mock_client_sms)

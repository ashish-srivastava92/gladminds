from gladminds import smsparser
from base_unit import GladmindsUnitTestCase

class SmsParserTest(GladmindsUnitTestCase):

    def test_sms_parse(self):
        mock_client_sms = "GCP_REG test.user@testcase.com Test User"
        test_args = smsparser.sms_parser(message = mock_client_sms)
        self.assertEqual(test_args['keyword'], 'gcp_reg')
        self.assertEqual(test_args['email_id'], 'test.user@testcase.com')
        self.assertEqual(test_args['name'], 'Test User')
    
    def test_invalid_message_format(self):
        with self.assertRaises(smsparser.InvalidFormat):
            mock_client_sms = "GCP_REG test.user@testcase.com"
            smsparser.sms_parser(message = mock_client_sms)
    
    def test_invalid_keyword(self):
         with self.assertRaises(smsparser.InvalidKeyWord):
             mock_client_sms = "ANNONYM test.user@testcase.com Test User"
             smsparser.sms_parser(message = mock_client_sms)
         
    def test_invalid_keyword(self):
        with self.assertRaises(smsparser.InvalidMessage):
            mock_client_sms = ""
            smsparser.sms_parser(message = mock_client_sms)
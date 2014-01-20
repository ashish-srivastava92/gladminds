import unittest
from gladminds import smsparser

class TestAssertWorks(unittest.TestCase):

    def test_sms_parse(self):
        mock_client_sms = "GCP_REG test.user@testcase.com Test User"
        test_args = smsparser.sms_parser(message = mock_client_sms)
        self.assertEqual(test_args['keyword'], 'gcp_reg')
        self.assertEqual(test_args['email_id'], 'test.user@testcase.com')
        self.assertEqual(test_args['name'], 'Test User')
    
    def test_render_sms_template(self):
        pass
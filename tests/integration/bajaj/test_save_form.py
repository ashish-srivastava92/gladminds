from integration.bajaj.base import BaseTestCase
from django.test.client import Client

from gladminds.bajaj import models


class TestSaveFormRegistration(BaseTestCase):

    def setUp(self):
        self.client = Client(SERVER_NAME='bajaj')
        pass

    def test_asc_registration(self):
        create_mock_data = {
                    u'name': u'TestASCUser',
                    u'address': u'TestASCUser Address',
                    u'pincode': u'111111',
                    u'password': u'password',
                    u'phone-number': u'9999999999',
                    u'email': u'TestASCUser@TestASCUser.com'
                }

        get_response = self.client.post('/aftersell/asc/self-register/', data=create_mock_data)
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(models.ASCTempRegistration.objects.count(), 1)
        self.assertEqual(models
                         .ASCTempRegistration.objects.all()[0].phone_number,
                          create_mock_data['phone-number'])

    def test_fail_registration_mail(self):
        create_mock_data = {
                    u'name': u'TestASCUser',
                    u'address': u'TestASCUser Address',
                    u'pincode': u'111111',
                    u'password': u'password',
                    u'phone-number': u'9999999999',
                    u'email': u'TestASCUser@TestASCUser.com'
                }

        get_response = self.client.post('/aftersell/asc/self-register/', data=create_mock_data)
        self.assertEqual(get_response.status_code, 200)

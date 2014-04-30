from integration.base_integration import GladmindsResourceTestCase
from django.test.client import Client
from gladminds.models import common


class TestRegisteration(GladmindsResourceTestCase):

    def setUp(self):
        self.client = Client()
        pass

    def test_asc_registeration(self):
        data = {
                    u'name': u'TestASCUser',
                    u'address': u'TestASCUser Address',
                    u'pincode': u'111111',
                    u'password': u'password',
                    u'phone_number': u'9999999999',
                    u'email': u'TestASCUser@TestASCUser.com'
                }

        response = self.client.post('/save/asc', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(common.ASCSaveForm.objects.count(), 1)
        self.assertEqual(common.ASCSaveForm.objects.all()[0].phone_number,
                          data['phone_number'])

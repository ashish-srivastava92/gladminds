from tastypie.test import ResourceTestCase
from django.core import management


class GladmindsResourceTestCase(ResourceTestCase):

    def setUp(self):
        super(GladmindsResourceTestCase, self).setUp()
        management.call_command('loaddata', 'etc/testdata/template.json', verbosity=0)
        management.call_command('loaddata', 'etc/testdata/customer.json', verbosity=0)
        management.call_command('loaddata', 'etc/testdata/brand.json', verbosity=0)
        management.call_command('loaddata', 'etc/testdata/producttype.json', verbosity=0)
        management.call_command('loaddata', 'etc/testdata/dealer.json', verbosity=0)
        management.call_command('loaddata', 'etc/testdata/serviceadvisor.json', verbosity=0)
        management.call_command('loaddata', 'etc/testdata/product.json', verbosity=0)
        management.call_command('loaddata', 'etc/testdata/coupon.json', verbosity=0)
        self.MESSAGE_URL = "/v1/messages"

    def assertSuccessfulHttpResponse(self, resp, msg=None):
        """
        Ensures the response is returning status between 200 and 299,
         both inclusive 
        """
        return self.assertTrue(resp.status_code >= 200 
                               and resp.status_code <= 299, msg) 

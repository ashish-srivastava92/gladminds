import unittest
from django.core import management


class GladmindsUnitTestCase(unittest.TestCase):
    def setUp(self):
        super(GladmindsUnitTestCase, self).setUp()
        management.call_command('loaddata', 'etc/testdata/template.json', verbosity=0)
        management.call_command('loaddata', 'etc/testdata/customer.json', verbosity=0)
        management.call_command('loaddata', 'etc/testdata/brand.json', verbosity=0)
        management.call_command('loaddata', 'etc/testdata/producttype.json', verbosity=0)
        management.call_command('loaddata', 'etc/testdata/dealer.json', verbosity=0)
        management.call_command('loaddata', 'etc/testdata/serviceadvisor.json', verbosity=0)
        management.call_command('loaddata', 'etc/testdata/product.json', verbosity=0)
        management.call_command('loaddata', 'etc/testdata/coupon.json', verbosity=0)

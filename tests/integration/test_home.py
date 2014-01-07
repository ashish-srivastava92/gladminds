# This is a dummy integration test. You would write your
# Django integration Tests here.
from django.test import TestCase


class TestHome(TestCase):

    def test_home(self):
        r = self.client.get('/')
        self.assertEqual(r.status_code, 404,
                         'Its an Empty Project!')

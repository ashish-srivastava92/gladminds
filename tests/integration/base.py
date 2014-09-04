from tastypie.test import ResourceTestCase
from django.core import management
from gladminds.models import common
from gladminds.aftersell.models import common as aftersell_common
import os
from django.conf import settings
import json
from time import sleep
from datetime import datetime
from django.test import TestCase

__BACKOFF = [0.5, 1, 2, 4, 8, 16, 32, 64]


def _exponential_backoff(index):
    if index >= len(__BACKOFF):
        index = len(__BACKOFF) - 1
    if index < 0:
        index = 0
    return __BACKOFF[index]


def wait_for_sms(mobile, check_date=None, time_to_check_for=128):
    total_time = 0
    for i in range(10):
        #check for audit (use check date for filtering)
        if total_time > time_to_check_for:
            raise
        t = _exponential_backoff(i)
        total_time += t
        sleep(t)
    raise


class BaseTestCase(ResourceTestCase):

    def setUp(self):
        TestCase.setUp(self)

    def assert_successful_http_response(self, resp, msg=None):
        return self.assertTrue(resp.status_code >= 200 
                               and resp.status_code <= 299, msg)

    def assert_sms_received(self, mobile, check_date=datetime.now(), time_to_check_for=128, msg="sms failed"):
        try:
            wait_for_sms(mobile, check_date, time_to_check_for)
            return
        except:
            raise self.failureException(msg)

    def check_sms_sent(self, mobile):
        pass

    def check_service_type_of_coupon(self, id, service_type):
        pass

    def send_asc_feed(self):
        file_path = os.path.join(settings.BASE_DIR, 'tests/integration/asc_feed.xml')
        xml_data = open(file_path, 'r').read()
        response = self.client.post('/api/v1/bajaj/feed/?wsdl', data=xml_data,content_type='text/xml')
        self.assert_successful_http_response(response)

    def check_asc_feed_saved_to_db(self):
        self.send_asc_feed()
        asc = aftersell_common.RegisteredDealer.objects.get(dealer_id='ASC001')
        self.assertEquals('ASC001', asc.dealer_id)

        
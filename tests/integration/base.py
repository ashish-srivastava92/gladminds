from tastypie.test import ResourceTestCase
from django.core import management
from gladminds.models import common
from gladminds.aftersell.models import common as aftersell_common
import os
from django.conf import settings
import json
from time import sleep
from datetime import datetime

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
        pass

    def assertSuccessfulHttpResponse(self, resp, msg=None):
        return self.assertTrue(resp.status_code >= 200 
                               and resp.status_code <= 299, msg)

    def assertSmsReceived(self, mobile, check_date=datetime.now(), time_to_check_for=128, msg="sms failed"):
        try:
            wait_for_sms(mobile, check_date, time_to_check_for)
            return
        except:
            raise self.failureException(msg)

    def checkSmsSent(self, mobile):
        pass

    def checkServiceTypeOfCoupon(self, id, service_type):
        pass
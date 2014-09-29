from tastypie.test import ResourceTestCase
from django.contrib.auth.models import User, Group
from gladminds.models import common
from gladminds.aftersell.models import common as aftersell_common
from gladminds.management.commands import load_gm_migration_data
from time import sleep
from datetime import datetime

from django.test.client import Client

client = Client()

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
        super(BaseTestCase, self).setUp()
        self.client = Client()
        self.access_token = 'testaccesstoken'
        load_email_obj = load_gm_migration_data.Command()
        load_email_obj.add_email_template()
        load_email_obj.add_sms_template()
        load_email_obj.add_group()

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
###############################create data in database#########################################################################

    def create_user(self, **kwargs):
        user = User.objects.create_user(kwargs['username'], kwargs['email'], kwargs['password'])
        user.save()
        if kwargs.get('group_name'):
            user_group = Group.objects.get(name=kwargs['group_name'])
            user.groups.add(user_group)
        if kwargs.get('group_name'):
            user_profile = aftersell_common.UserProfile(user=user, phone_number=kwargs['phone_number'])
            user_profile.save()
            return user_profile

    def get_user_obj(self, **kwargs):
        user_obj = User.objects.get(**kwargs)
        return user_obj


#########################################send feed function################################################################



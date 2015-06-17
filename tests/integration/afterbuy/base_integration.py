from gladminds.afterbuy import models
from django.test.client import Client
from tastypie.test import ResourceTestCase
from gladminds.management.commands import load_gm_migration_data, setup
import json
from gladminds.afterbuy import models as afterbuy_models
from boto.beanstalk.response import Response
from django.contrib.auth.models import User, Group
from gladminds.core.auth_helper import GmApps, add_user_to_group, Roles
from gladminds.core.signals import add_group

client  =  Client(SERVER_NAME='afterbuy')

class AfterBuyResourceTestCase(ResourceTestCase):

    def setUp(self):
        super(AfterBuyResourceTestCase, self).setUp()
        load_email_obj = load_gm_migration_data.Command()
        load_email_obj.add_email_template()
        load_email_obj.add_sms_template()
        load_email_obj.add_group()
#         setup_obj = setup.Command()
#         setup_obj.handle()
        self.client = Client(SERVER_NAME='afterbuy')
        self.MESSAGE_URL = "/v1/messages"
        

    def create_afterbuy_user(self):
        user_obj = User(username="glad", email="ab@ab.co")
        password = 123
        user_obj.set_password(password)
        user_obj.save(using=GmApps.AFTERBUY)
        glad_obj = models.Consumer(user=user_obj, phone_number='7760814041')
        glad_obj.save()        
        return glad_obj

    def post(self, uri, content_type='application/json', data=None):
        resp = self.login()
        uri = uri + '?access_token=' + json.loads(resp.content)['access_token']
        return self.client.post(uri, content_type=content_type, data=json.dumps(data))

    def get(self, uri, content_type='application/json', filters=None):
        resp = self.login()
        return self.client.get(uri)

    def login(self):
        login_data = {"phone_number":"7760814041", "password":"123"}
        uri = '/afterbuy/v1/consumers/login/'
        response = self.client.post(uri, data=json.dumps(login_data), content_type='application/json')
        return response

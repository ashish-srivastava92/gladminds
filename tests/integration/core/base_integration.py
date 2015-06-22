import os
import json

from django.conf import settings
from django.test.client import Client
from tastypie.test import ResourceTestCase
from django.core import management
from django.contrib.auth.models import User, Group
from gladminds.management.commands import load_gm_migration_data, setup
from gladminds.core.model_fetcher import get_model
from gladminds.core.auth_helper import OTHER_GROUPS

class CoreResourceTestCase(ResourceTestCase):
    multi_db=True

    def setUp(self):
        super(CoreResourceTestCase, self).setUp()
        load_email_obj = load_gm_migration_data.Command()
        load_email_obj.add_email_template()
        load_email_obj.add_sms_template()
        load_email_obj.add_group()
        load_email_obj.add_constants()
        
    def add_group(self, brand, group):
        group_count = Group.objects.filter(name=group).using(brand).count()
        if group_count == 0:
            group_obj = Group(name=group)
            group_obj.save(using=brand)
            return group_obj

    def create_user(self, **kwargs):
        brand=kwargs['brand']
        user = User.objects.create_user(kwargs['username'], kwargs['email'], kwargs['password'])
        user.save(using=brand)
        if kwargs.get('group_name'):
            group=kwargs['group_name']
            try:
                user_group = Group.objects.get(name=group).using(brand)
            except:
                user_group=self.add_group(brand, group)
            user.groups.add(user_group)
        if kwargs.get('phone_number'):
            user_profile = get_model('UserProfile')(user=user, phone_number=kwargs['phone_number'])
            user_profile.save(using=brand)
            return user_profile
    
    ''' function returns access_token after login'''
    def user_login(self, data):
        resp=self.post(uri='/v1/gm-users/login/', data=data)
        return json.loads(resp.content)['access_token']

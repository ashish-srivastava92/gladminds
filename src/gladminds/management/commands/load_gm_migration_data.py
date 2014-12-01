import os
import json

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from django.conf import settings

from gladminds.bajaj.models import MessageTemplate, EmailTemplate
from gladminds.bajaj import models as common
from gladminds.bajaj.feeds import feed
from gladminds.core.utils import get_model
from gladminds.core.auth_helper import ALL_APPS

BASIC_FEED = feed.BaseFeed()

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        self.add_sms_template()
        self.add_email_template()
        #self.add_group()

    def add_group(self):
        print "Loading groups..."
        file_path = os.path.join(settings.PROJECT_DIR, 'template_data/group.json')
        groups = json.loads(open(file_path).read())
        Group.objects.all().delete()
        for group in groups:
            group = Group(id=group['fields']["id"],name=group['fields']["name"])
            group.save()
        print "Loaded groups..."
         
        
    
    def add_sms_template(self):
        print "Loading sms template..."
        file_path = os.path.join(settings.PROJECT_DIR, 'template_data/template.json')
        message_templates = json.loads(open(file_path).read())
        for app in ALL_APPS:
            mt = get_model('MessageTemplate', app)
            #mt = getattr(import_module('gladminds.{0}.models'.format(app)), 'MessageTemplate')
            mt.objects.all().delete()
            for message_temp in message_templates:
                fields = message_temp['fields']
                temp_obj = mt(template_key=fields['template_key']\
                           , template=fields['template'], description=fields['description'])
                temp_obj.save()
            print "Loaded sms template..."
    
    def add_email_template(self):
        print "Loading email template..."
        file_path = os.path.join(settings.PROJECT_DIR, 'template_data/email_template.json')
        email_templates = json.loads(open(file_path).read())
        for app in ALL_APPS:
            et = get_model('EmailTemplate', app)
            et.objects.all().delete()
            for email_temp in email_templates:
                fields = email_temp['fields']
                temp_obj = et(template_key=fields['template_key']\
                           , sender=fields['sender'], receiver=fields['receiver'],\
                            subject=fields['subject'], body=fields['body'],\
                            description=fields['description'])
                temp_obj.save()
            print "Loaded email template..."   
        
    def add_user_for_existing_dealer(self):
        print "Loading users for existing dealer...."
        all_dealers = common.Dealer.objects.all()
        for dealer in all_dealers:
            BASIC_FEED.register_user('dealer', username=dealer.dealer_id)
        print "Loaded users for existing dealer...."
        
    def add_user_in_gladminds_table(self):
        print "Adding users in ...."
        all_gladminds_users = common.UserProfile.objects.all()
        for gladminds_user in all_gladminds_users:
            user = BASIC_FEED.register_user('customer', username=gladminds_user.gladmind_customer_id)
            gladminds_user.user = user
            gladminds_user.save()
        print "Loading users for existing dealer...."
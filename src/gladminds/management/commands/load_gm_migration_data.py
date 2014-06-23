from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
import os
from django.conf import settings
import json
from gladminds.models import common

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        self.add_group()
        self.add_sms_template()
        self.add_email_template()
        
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
        common.MessageTemplate.objects.all().delete()
        for message_temp in message_templates:
            fields = message_temp['fields']
            temp_obj = common.MessageTemplate(template_key=fields['template_key']\
                       , template=fields['template'], description=fields['description'])
            temp_obj.save()
        print "Loaded sms template..."
    
    def add_email_template(self):
        print "Loading email template..."
        file_path = os.path.join(settings.PROJECT_DIR, 'template_data/email_template.json')
        email_templates = json.loads(open(file_path).read())
        common.EmailTemplate.objects.all().delete()
        for email_temp in email_templates:
            fields = email_temp['fields']
            temp_obj = common.EmailTemplate(template_key=fields['template_key']\
                       , sender=fields['sender'], reciever=fields['reciever'],\
                        subject=fields['subject'], body=fields['body'],\
                        description=fields['description'])
            temp_obj.save()
        print "Loaded email template..."        
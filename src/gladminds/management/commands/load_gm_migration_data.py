from django.core.management.base import BaseCommand
import os
from django.conf import settings
import json
from gladminds.models import common

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        self.add_group()
        self.add_sms_template()
        
    def add_group(self):
        from django.contrib.auth.models import Group
        file_path = os.path.join(settings.BASE_DIR, 'etc/data/group.json')
        email_templates = json.loads(open(file_path).read())
        Group.objects.all().delete()
        for email_temp in email_templates:
            print email_temp
            group = Group(name=email_temp['fields']["name"])
            group.save()
        
        
    
    def add_sms_template(self):
        file_path = os.path.join(settings.BASE_DIR, 'etc/data/template.json')
        message_templates = json.loads(open(file_path).read())
        common.MessageTemplate.objects.all().delete()
        for message_temp in message_templates:
            fields = message_temp['fields']
            temp_obj = common.MessageTemplate(template_key=fields['template_key']\
                       , template=fields['template'], description=fields['description'])
            temp_obj.save()
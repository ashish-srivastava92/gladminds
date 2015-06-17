import csv
import time
import random

from datetime import datetime
from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
# from gladminds.core import utils

from gladminds.core.auth_helper import Roles
from gladminds.core.model_fetcher import get_model
APP='bajaj'
user_profile = get_model('UserProfile', APP)
TEMP_SA_ID_PREFIX = settings.TEMP_SA_ID_PREFIX

class Command(BaseCommand):

    def mobile_format(self, phone_number):
        return '+91' + phone_number[-10:]
    
    def handle(self, *args, **options):
        self.upload_dealer_data()
        self.upload_service_advisor_data()

    def register_user(self, group, username):
        user_group = Group.objects.using(APP).get(name=group)
        new_user = User.objects.using(APP).create(username=username)
        password = username + settings.PASSWORD_POSTFIX
        new_user.set_password(password)
        new_user.save(using=APP)
        new_user.groups.add(user_group)
        new_user.save(using=APP)
        user_details = user_profile(user=new_user)
        user_details.save()
        return user_details

    def upload_dealer_data(self):
        print "Started running dealer function..."
        file_list = ['sa_data_goa_dl_hr.csv']
        dealer_list = []
        dealer_model = get_model('Dealer', APP)

        for i in range(0, 1):
            with open(settings.PROJECT_DIR + '/' + file_list[i], 'r') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=',')
                next(spamreader)
                for row_list in spamreader:
                    temp ={}
                    temp['dealer_id'] = row_list[1].strip() 
                    temp['name'] = row_list[2].strip()
                    temp['city'] = row_list[3].strip()
                    try:
                        temp['use_cdms'] = row_list[6].strip()
                    except:
                        temp.setdefault('use_cdms', True)
#                     temp['state'] = row_list[4].strip()

                    dealer_list.append(temp)
        
        for dealer in dealer_list:
            print "...Loading Dealer..", dealer
            try:
                dealer_object = dealer_model.objects.get(user__user__username = dealer['dealer_id'])
            except Exception as ex:
                new_user=self.register_user(group=Roles.DEALERS, username=dealer['dealer_id'])
                dealer_object = dealer_model(dealer_id=dealer['dealer_id'], user=new_user, use_cdms=dealer['use_cdms'])
                dealer_object.save()
            user_obj = dealer_object.user.user
            user_pro_obj = dealer_object.user
            first_name = dealer['name']
            last_name = ''
            if len(dealer['name'])>30:
                full_name = dealer['name'].split(' ')
                first_name = ' '.join(full_name[0:3])
                last_name = ' '.join(full_name[3:])
            user_obj.first_name = first_name
            user_obj.last_name = last_name
            user_obj.save(using=APP)
            user_pro_obj.address = dealer['city']
            user_pro_obj.save()

    def upload_service_advisor_data(self):
        print "Started running SA function..."
        file_list = ['sa_data_goa_dl_hr.csv']
        file = open("sa_details.txt", "w")
        sa_list = []
        dealer_model = get_model('Dealer', APP)
        sa_model = get_model('ServiceAdvisor', APP)

        for i in range(0, 1):
            with open(settings.PROJECT_DIR + '/' + file_list[i], 'r') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=',')
                next(spamreader)
                for row_list in spamreader:
                    temp={}
                    temp['city'] = (row_list[3].strip())
                    temp['dealer_id'] = row_list[1].strip()
                    temp['name'] = row_list[4].strip()
                    temp['number'] = self.mobile_format(row_list[5].strip())
                                       
                    sa_list.append(temp)
        
        for sa in sa_list:
            if not sa['name']=='':
                print "...Loading SA..", sa
                dealer_object = dealer_model.objects.get(dealer_id = sa['dealer_id'])
                try:
                    try:
                        sa_object = sa_model.objects.get(user__phone_number = sa['number'], status='Y')
                    except Exception as ex:
                        file.write("{0}: {1}".format(sa['number'], ex))
                        service_advisor_id = TEMP_SA_ID_PREFIX + str(random.randint(10**5, 10**6))
                        new_user=self.register_user(group=Roles.SERVICEADVISOR, username=service_advisor_id)
                        sa_object = sa_model(service_advisor_id = service_advisor_id,
                                             user=new_user,
                                             status='Y',
                                             dealer_id=dealer_object.user_id)
                        sa_object.save()
                    if sa_object.dealer_id!=dealer_object.user_id:
                        raise ValueError('ACTIVE UNDER {0}'.format(sa_object.dealer_id.dealer_id))
                    user_obj = sa_object.user.user
                    user_pro_obj = sa_object.user
                    first_name = sa['name']
                    last_name = ''
                    if len(sa['name'])>30:
                        full_name = sa['name'].split(' ')
                        first_name = ' '.join(full_name[0:3])
                        last_name = ' '.join(full_name[3:])
                    user_obj.first_name = first_name
                    user_obj.last_name = last_name
                    user_obj.save(using=APP)
                    user_pro_obj.address = sa['city']
                    user_pro_obj.phone_number = sa['number']
                    user_pro_obj.save()
                except Exception as ex:
                    file.write("{0}: {1}".format(sa['number'], ex))  
        file.close()
import csv
import logging
import datetime
from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
from gladminds.core.model_fetcher import get_model
# from gladminds.core.utils import generate_temp_id, mobile_format
from gladminds.core.auth_helper import Roles, GmApps
from django.contrib.auth.models import Group, User
from django.core.exceptions import ObjectDoesNotExist
APP='bajaj'
logger = logging.getLogger("gladminds")
_BAJAJ_ZSM = [('mspendharkar@bajajauto.co.in', 'mspendharkar@bajajauto.co.in', 'milindpendharkar@123', 'Milind Pendharkar')]

class Command(BaseCommand):

    def handle(self, *args, **options):
#         self.create_zonal_managers()
#         self.upload_asm_data()
        self.upload_asm_dealer_data()
    
    def register_user(self, group, username=None, phone_number=None,
                      first_name='', last_name='', email='', address='',
                      state='', pincode='', APP=APP):
        user_profile = get_model('UserProfile', APP)
        logger.info('New {0} Registration with id - {1}'.format(group, username))
        try:
            user_group = Group.objects.using(APP).get(name=group)
        except ObjectDoesNotExist as ex:
            logger.info(
                "[Exception: new_ registration]: {0}"
                .format(ex))
            user_group = Group.objects.using(APP).create(name=group)
            user_group.save(using=APP)
        if len(first_name)>30:
            full_name = first_name.split(' ')
            first_name = ' '.join(full_name[0:2])
            last_name = ' '.join(full_name[2:])
        else:
            first_name = first_name
            last_name = ' '
        if username:
            try:
                user_details = user_profile.objects.select_related('user').get(user__username=username)
                new_user = user_details.user
                user_details.phone_number=phone_number
                user_details.address=address
                user_details.save()
                new_user.first_name=first_name
                new_user.last_name=last_name
                new_user.save(using=APP)
            except ObjectDoesNotExist as ex:
                logger.info(
                    "[Exception: new_ registration]: {0}"
                    .format(ex))    
                new_user = User(
                    username=username, first_name=first_name, last_name=last_name, email=email)
                if not group in [Roles.DEALERS]:
                    password = email.split('@')[0] + '!123'
                    new_user.is_staff = True
                else:
                    password=username+'@123'
                new_user.set_password(password)
                new_user.save(using=APP)
                new_user.groups.add(user_group)
                new_user.save(using=APP)
                logger.info(group + ' {0} registered successfully'.format(username))
                user_details = user_profile(user=new_user,
                                        phone_number=phone_number, address=address,
                                        state=state, pincode=pincode)
                user_details.save()
            return user_details
        else:
            logger.info('{0} id is not provided.'.format(str(group)))
            raise Exception('{0} id is not provided.'.format(str(group)))   

    def create_zonal_managers(self):
        print ''' Started uploading Zonal Service Manager data'''
        file_list = ['DSS_ZSM_DATA.csv']
        zsm_list = []
        ZSM = get_model('ZonalServiceManager', APP)
        USER_PROFILE = get_model('UserProfile', APP)
        
        for i in range(0, 1):
            with open(settings.PROJECT_DIR + '/' + file_list[i], 'r') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=',')
                next(spamreader)
                for row_list in spamreader:
                    temp ={}
                    temp['id'] = row_list[3].strip()  
                    temp['name'] = row_list[4].strip()
                    temp['region'] = row_list[5].strip()
                    temp['number'] = row_list[6].strip()
                    temp['email'] = row_list[7].strip()
                    zsm_list.append(temp)
        try:
            for zsm in zsm_list:
                print "create zonal managers", zsm
                profile_obj = self.register_user(Roles.ZSM,
                                                       username=zsm['email'],
                                                       phone_number=zsm['number'],
                                                       email=zsm['email'],
                                                       first_name=zsm['name'])
                try:
                    zsm_obj =  ZSM.objects.get(user=profile_obj)
                except:
                    zsm_obj = ZSM(user=profile_obj)
                zsm_obj.zsm_id = zsm['id']
                zsm_obj.regional_office = zsm['region']
                zsm_obj.save()
        except Exception as ex:
            print "[create zsm ]" , ex

    def upload_asm_data(self):
        print ''' Started uploading Area Service Manager data'''
        file_list = ['DSS_ASM_DATA.csv']
        asm_list = []
        ASM = get_model('AreaServiceManager', APP)
        ZSM = get_model('ZonalServiceManager', APP)
        USER_PROFILE = get_model('UserProfile', APP)
        
        for i in range(0, 1):
            with open(settings.PROJECT_DIR + '/' + file_list[i], 'r') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=',')
                next(spamreader)
                for row_list in spamreader:
                    temp ={}
                    temp['zsm_id'] = row_list[0].strip()  
                    temp['id'] = row_list[4].strip()
                    temp['name'] = row_list[5].strip()
                    temp['area'] = row_list[6].strip()
                    temp['region'] = row_list[7].strip()
                    temp['number'] = row_list[8].strip()
                    temp['email'] = row_list[9].strip()
                    asm_list.append(temp)
        try:            
            for asm in asm_list:
                print "create area managers", asm
                asm_user_pro = self.register_user(Roles.AREASERVICEMANAGER,
                                                           username=asm['email'],
                                                           phone_number=asm['number'],
                                                           email=asm['email'],
                                                           first_name=asm['name'])
                zsm_object = ZSM.objects.get(zsm_id=asm['zsm_id'])
                try:
                    asm_object = ASM.objects.get(user=asm_user_pro)
                except Exception as ex:
                    asm_object = ASM(user=asm_user_pro)
                    asm_object.save()
                asm_object.asm_id=asm['id']
                asm_object.area = asm['area'].upper()
                asm_object.zsm=zsm_object
                asm_object.save()
        except Exception as ex:
            print "[create asm ]" , ex, asm

    def upload_asm_dealer_data(self):
        print ''' Started uploading Area Service Manager data'''
        file_list = ['DSSS_ASM_DEALER_MAP.csv']
        dealer_list = []
        count=0
        DEALER = get_model('Dealer', APP)
        ASM = get_model('AreaServiceManager', APP)
        USER_PROFILE = get_model('UserProfile', APP)
        
        for i in range(0, 1):
            with open(settings.PROJECT_DIR + '/' + file_list[i], 'r') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=',')
                next(spamreader)
                for row_list in spamreader:
                    temp ={}
                    temp['asm_id'] = row_list[0].strip()  
                    temp['dealer_id'] = row_list[1].strip()
                    temp['name'] = row_list[2].strip().upper()
                    temp['area'] = row_list[3].strip().upper()
                    dealer_list.append(temp)
        for dealer in dealer_list:
            try:
                print "map dealer", dealer            
                asm_object = ASM.objects.get(asm_id=dealer['asm_id'])
                dealer_user_pro = self.register_user(Roles.DEALERS,
                                                           username=dealer['dealer_id'],
                                                           first_name=dealer['name'],
                                                           address=dealer['area'])
                try:
                    dealer_object = DEALER.objects.get(user=dealer_user_pro)
                except Exception as ex:
                    dealer_object = DEALER(dealer_id=dealer['dealer_id'],
                                           user=dealer_user_pro)
                    dealer_object.save()
                dealer_object.asm=asm_object
                dealer_object.save()
            except Exception as ex:
                print "[map dealer and asm ]" , ex, dealer
                continue
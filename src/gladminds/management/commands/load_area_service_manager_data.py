import csv
import logging
import datetime
from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
from gladminds.core.loaders.module_loader import get_model
from gladminds.core.utils import generate_temp_id, mobile_format
from gladminds.core.auth_helper import Roles, GmApps
from django.contrib.auth.models import Group, User
from django.core.exceptions import ObjectDoesNotExist
APP='bajaj'
logger = logging.getLogger("gladminds")

class Command(BaseCommand):

    def handle(self, *args, **options):
        self.upload_asm_data()
    
    def register_user(self, group, username=None, phone_number=None,
                      first_name='', last_name='', email='', address='',
                      state='', pincode=''):
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
        if username:
            try:
                user_details = user_profile.objects.select_related('user').get(user__username=username)
            except ObjectDoesNotExist as ex:
                logger.info(
                    "[Exception: new_ registration]: {0}"
                    .format(ex))    
                new_user = User(
                    username=username, first_name=first_name, last_name=last_name, email=email)
                if group =='customer':
                    password = settings.PASSWORD_POSTFIX
                else:
                    password = username + settings.PASSWORD_POSTFIX
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

    def upload_asm_data(self):
        print ''' Started uploading Area Service Manager data'''
        file_list = ['AREA_SERVICE_MANAGER_DATA.csv']
        asm_list = []
        ASM = get_model('AreaServiceManager', APP)
        DEALER = get_model('Dealer', APP)
        ZSM = get_model('ZonalServiceManager', APP)
        ASC = get_model('AuthorizedServiceCenter', APP)
        USER_PROFILE = get_model('UserProfile', APP)
        
        for i in range(0, 1):
            with open(settings.PROJECT_DIR + '/' + file_list[i], 'r') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=',')
                next(spamreader)
                for row_list in spamreader:
                    temp ={}
                    temp['dealer_id'] = row_list[0].strip()
                    temp['dealer_name'] = row_list[1].strip()
                    temp['dealer_city'] = row_list[2].strip()
                    temp['dealer_state'] = row_list[3].strip()  
                    temp['dealer_email'] = row_list[4].strip()
                    temp['asc_name'] = row_list[5].strip()
                    temp['asc_id'] = row_list[6].strip()
                    temp['asc_email'] = row_list[7].strip()
                    temp['asc_city'] = row_list[8].strip()
                    temp['asc_state'] = row_list[9].strip()
                    temp['asc_owner_name'] = row_list[10].strip()
                    temp['asc_owner_phone'] = row_list[11].strip()
                    temp['asm_name'] = row_list[12].strip()
                    temp['asm_email'] = row_list[13].strip()
                    temp['zsm_name'] = row_list[14].strip()
                    temp['zsm_email'] = row_list[15].strip()  
                    asm_list.append(temp)
                    
        for asm in asm_list:
            asm_user_pro = self.register_user(Roles.AREASERVICEMANAGER,
                                                       username=asm['asm_email'],
                                                       email=asm['asm_email'],
                                                       first_name=asm['asm_name'])
            zsm_object = ZSM.objects.get(user__user__username=asm['zsm_email'])
            asm_object = ASM(user=asm_user_pro, zsm=zsm_object)
            asm_object.save()
                 
        for dealer in asm_list:
            dealer_obj = DEALER.objects.filter(dealer_id=dealer['dealer_id'])
            if not dealer_obj:
                if len(dealer['dealer_name'])>30:
                    full_name = dealer['dealer_name'].split(' ')
                    first_name = ' '.join(full_name[0:3])
                    last_name = ' '.join(full_name[3:])
                else:
                    first_name = dealer['dealer_name']
                    last_name = ' '
                dealer_user_pro = self.register_user(Roles.DEALERS,
                                                     username=dealer['dealer_id'],
                                                     first_name=first_name,
                                                     last_name=last_name,
                                                     email=dealer['dealer_email'],
                                                     address=dealer['dealer_city'],
                                                     state=dealer['dealer_state'])
                dealer_object = DEALER(dealer_id=dealer['dealer_id'], user=dealer_user_pro)
                dealer_object.save()

        for asc in asm_list:
            try:
                asc_object = ASC.objects.get(asc_id=asc['asc_id'])
             
            except Exception as ex:
                if len(asc['dealer_name'])>30:
                        full_name = asc['dealer_name'].split(' ')
                        first_name = ' '.join(full_name[0:3])
                        last_name = ' '.join(full_name[3:])
                else:
                    first_name = asc['dealer_name']
                    last_name = ' '
                asc_user_pro_obj = self.register_user(Roles.ASCS,
                                                     username=asc['asc_id'],
                                                     first_name=first_name,
                                                     last_name=last_name,
                                                     email=asc['asc_email'],
                                                     address=asc['asc_city'],
                                                     state=asc['asc_state'])
                 
                asc_object = ASC(asc_id=asc['asc_id'], user=asc_user_pro_obj)
                asc_object.save()    
            try:     
                asc_dealer = DEALER.objects.get(dealer_id=asc['dealer_id'])
            except Exception as ex:
                asc_dealer = None
                
            asc_asm = ASM.objects.filter(user__user__username=asc['asm_email'])
            asc_object.dealer = asc_dealer
            asc_object.asm = asc_asm[0]
            asc_object.asc_owner = asc['asc_owner_name']
            asc_object.asc_owner_phone = asc['asc_owner_phone']
            asc_object.save()
            

import csv
import logging
from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
from gladminds.core.model_fetcher import get_model
from gladminds.core.auth_helper import Roles
from django.contrib.auth.models import Group, User
APP='bajaj'
logger = logging.getLogger("gladminds")

class Command(BaseCommand):

    def handle(self, *args, **options):
        self.upload_asm_data()
    
    def register_user(self, group, username=None, phone_number=None,
                      first_name='', last_name='', email='', address='',
                      state='', pincode='', APP=APP):
        user_profile = get_model('UserProfile', APP)
        try:
            user_group = Group.objects.using(APP).get(name=group)
        except ObjectDoesNotExist as ex:
            user_group = Group.objects.using(APP).create(name=group)
            user_group.save(using=APP)
        if username:
            try:
                user_details = user_profile.objects.select_related('user').get(user__username=username)
            except ObjectDoesNotExist as ex:
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
                user_details.save(using=APP)
            return user_details
        else:
            logger.info('{0} id is not provided.'.format(str(group)))
            raise Exception('{0} id is not provided.'.format(str(group)))   

    def upload_asc_with_asm_data(self):
        '''Uploads data of ASC with their
           associated ASM and the ZSM'''
        print ''' Started uploading Area Service Manager data'''
        file_list = ['AREA_SERVICE_MANAGER_DATA.csv']
        asm_list = []
        ASM = get_model('AreaServiceManager', APP)
        DEALER = get_model('Dealer', APP)
        ZSM = get_model('ZonalServiceManager', APP)
        ASC = get_model('AuthorizedServiceCenter', APP)
        USER_PROFILE = get_model('UserProfile', APP)
        
        for i in range(0, 1):
            with open(settings.PROJECT_DIR + '/upload_data/' + file_list[i], 'r') as csvfile:
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
            try:
                print "check ASM...", asm['asm_email']
                asm_object = ASM.objects.using('bajaj').get(user__user__username=asm['asm_email'])
            except:
                print "ADD ASM...", asm['asm_email']
                asm_user_pro = self.register_user(Roles.AREASERVICEMANAGER,
                                                       username=asm['asm_email'],
                                                       email=asm['asm_email'],
                                                       first_name=asm['asm_name'])
                zsm_object = ZSM.objects.get(user__user__username=asm['zsm_email'])
                asm_object = ASM(user=asm_user_pro, zsm=zsm_object, asm_id=None)
                asm_object.save(using=APP)
                 
        for dealer in asm_list:
            print "check dealer...", dealer['dealer_id']
            if dealer['dealer_id']:
                dealer_obj = DEALER.objects.filter(dealer_id=dealer['dealer_id'])
                if not dealer_obj:
                    print "add dealer...", dealer['dealer_id']
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
                    dealer_object.save(using=APP)

        for asc in asm_list:
            print "load asc...", asc['asc_id']
            try:
                if len(asc['asc_name'])>30:
                        full_name = asc['asc_name'].split(' ')
                        first_name = ' '.join(full_name[0:3])
                        last_name = ' '.join(full_name[3:])
                else:
                    first_name = asc['asc_name']
                    last_name = ' '
                asc_object = ASC.objects.get(asc_id=asc['asc_id'])
                asc_user=asc_object.user.user
                asc_user.first_name=first_name
                asc_user.last_name=last_name
                asc_user.save(using=APP)
            except Exception as ex:
                print "add asc...", asc['asc_id']
                asc_user_pro_obj = self.register_user(Roles.ASCS,
                                                     username=asc['asc_id'],
                                                     first_name=first_name,
                                                     last_name=last_name,
                                                     email=asc['asc_email'],
                                                     address=asc['asc_city'],
                                                     state=asc['asc_state'])
                 
                asc_object = ASC(asc_id=asc['asc_id'], user=asc_user_pro_obj)
                asc_object.save(using=APP)
            try:     
                asc_dealer = DEALER.objects.get(dealer_id=asc['dealer_id'])
            except Exception as ex:
                asc_dealer = None
            
            asc_asm = ASM.objects.filter(user__user__username=asc['asm_email'])
            asc_object.dealer = asc_dealer
            asc_object.asm = asc_asm[0]
            asc_object.asc_owner = asc['asc_owner_name']
            asc_object.asc_owner_phone = asc['asc_owner_phone']
            asc_object.save(using=APP)

        

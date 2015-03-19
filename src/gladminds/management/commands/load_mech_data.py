import csv
import datetime
from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from gladminds.core.loaders.module_loader import get_model
from gladminds.core.utils import generate_temp_id, mobile_format
APP='bajaj'

class Command(BaseCommand):

    def handle(self, *args, **options):
        self.upload_dist_data()
        self.upload_mech_data()
    
    def upload_dist_data(self):
        print "Started uploading distributor..."
        file_list = ['DIST_DATA.csv']
        dealer_list = []
        asm = get_model('AreaSparesManager', APP)
        dist = get_model('Distributor', APP)
        user_profile = get_model('UserProfile', APP)

        for i in range(0, 1):
            with open(settings.PROJECT_DIR + '/' + file_list[i], 'r') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=',')
                next(spamreader)
                for row_list in spamreader:
                    temp ={}
                    temp['asm_id'] = row_list[0].strip()
                    temp['id'] = row_list[1].strip()
                    temp['name'] = row_list[2].strip()
                    temp['email'] = row_list[4].strip()  
                    temp['mobile'] = row_list[5].strip()
                    temp['city'] = row_list[6].strip()  
                    dealer_list.append(temp)
        
        for dealer in dealer_list:
            dist_object = dist.objects.filter(distributor_id=dealer['id'])
            if not dist_object:
                dist_user_pro_object = user_profile.objects.filter(user__username=dealer['id'])
                if not dist_user_pro_object:
                    password=dealer['id']+'@123'
                    dist_user_object = User.objects.using(APP).create(username=dealer['id'])
                    dist_user_object.set_password(password)
                    dist_user_object.email = dealer['email']
                    dist_user_object.first_name = dealer['name']
                    dist_user_object.save(using=APP)
                    dist_user_pro_object = user_profile(user=dist_user_object,
                                                phone_number=dealer['mobile'],
                                                address=dealer['city'])
                    dist_user_pro_object.save()
                else:
                    dist_user_pro_object = dist_user_pro_object[0]
                asm_object = asm.objects.get(asm_id=dealer['asm_id'])
                dist_object = dist(distributor_id=dealer['id'],
                                          asm=asm_object,
                                          user=dist_user_pro_object,
                                          name=dealer['name'],
                                          email=dealer['email'],
                                          phone_number=dealer['mobile'],
                                          city=dealer['city'])
                dist_object.save()

    def empty_to_none(self, value):
        if value=='':
            return None
        else:
            return int(value)

    def upload_mech_data(self):
        print "Started uploading mech data..."
        file_list = ['MECHANIC_DATA.csv']
        mech_list = []
        retailer = get_model('Retailer', APP)
        dist = get_model('Distributor', APP)
        user_profile = get_model('UserProfile', APP)
        mech = get_model('Member', APP)

        for i in range(0, 1):
            with open(settings.PROJECT_DIR + '/' + file_list[i], 'r') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=',')
                next(spamreader)
                for row_list in spamreader:
                    temp ={}
                    temp['form_no'] = self.empty_to_none(row_list[0].strip())
                    temp['first_name'] = row_list[1].strip()

                    temp['last_name'] = row_list[3].strip()
                    dob=row_list[4].strip()
                    if dob:
                        temp['dob'] = datetime.datetime.strptime(dob, '%d/%m/%Y')
                    else:
                        temp['dob'] = None
                    temp['shop_name'] = row_list[5].strip()
                    temp['shop_no'] = row_list[6].strip()
                    temp['shop_address'] = row_list[7].strip()
                    temp['locality'] = row_list[8].strip()
                    temp['tehsil'] = row_list[9].strip()

                    temp['district'] = (row_list[11].strip()).upper()
                    temp['state'] = row_list[12].strip()
                    temp['pincode'] = row_list[13].strip()
                    temp['dist_id'] = row_list[14].strip()
                    temp['wall_len'] = self.empty_to_none(row_list[16].strip())
                    temp['wall_width'] = self.empty_to_none(row_list[17].strip())
                    temp['mobile'] = row_list[18].strip()
                    temp['two_stroke'] = self.empty_to_none(row_list[19].strip())
                    temp['four_stroke'] = self.empty_to_none(row_list[20].strip())
                    temp['cng_lpg'] = self.empty_to_none(row_list[21].strip())
                    temp['diesel'] = self.empty_to_none(row_list[22].strip())
                    temp['spare_month'] = self.empty_to_none(row_list[23].strip())
                    temp['genuine'] = self.empty_to_none(row_list[24].strip())
                    temp['ret_name'] = row_list[26].strip()
                    temp['ret_town'] = row_list[27].strip()

                    reg = row_list[29].strip()
                    if reg:
                        temp['reg_date'] = datetime.datetime.strptime(reg, '%d/%m/%Y')
                    else:
                        temp['reg_date'] = None

                    temp['complete'] = row_list[31].strip()
                    temp['mech_id'] = row_list[32].strip()
                    mech_list.append(temp)
        for mechanic in mech_list:
            mobile = mobile_format(mechanic['mobile'])
            mech_object = mech.objects.filter(phone_number=mobile)
            if not mech_object:
                if not mechanic['mech_id']:
                    mech_id = generate_temp_id('TME')
                else:
                    mech_id=mechanic['mech_id']
                if mechanic['dist_id']:
                    dist_object = dist.objects.get(distributor_id=mechanic['dist_id'])
                else:
                    dist_object = None
                
                ret_obj = retailer.objects.filter(retailer_name=mechanic['ret_name'])
                if not ret_obj:
                    ret_obj = retailer(retailer_name=mechanic['ret_name'],
                             retailer_town=mechanic['ret_town'])
                    ret_obj.save()
                else:
                    ret_obj = ret_obj[0]
                
                mech_object = mech(registered_by_distributor=dist_object,
                                preferred_retailer=ret_obj,
                                mechanic_id=mech_id,
                                first_name = mechanic['first_name'],
                                last_name = mechanic['last_name'],
                                date_of_birth=mechanic['dob'],
                                phone_number=mobile,           
                                form_number=mechanic['form_no'],
                                registered_date=mechanic['reg_date'],
                                shop_number =  mechanic['shop_no'],
                                shop_name =  mechanic['shop_name'],
                                shop_address =  mechanic['shop_address'],
                                locality =  mechanic['locality'],
                                tehsil =  mechanic['tehsil'],
                                district =  mechanic['district'],
                                state =  mechanic['state'],
                                pincode =  mechanic['pincode'],
                                shop_wall_length =  mechanic['wall_len'],
                                shop_wall_width =  mechanic['wall_width'],
                                serviced_2S =  mechanic['two_stroke'],
                                serviced_4S =  mechanic['four_stroke'],
                                serviced_CNG_LPG =  mechanic['cng_lpg'],
                                serviced_diesel =  mechanic['diesel'],
                                spare_per_month =  mechanic['spare_month'],
                                genuine_parts_used =  mechanic['genuine'],
                                form_status = mechanic['complete']
                                )
                mech_object.save()

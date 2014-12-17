import csv
import datetime
from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from gladminds.core.utils import get_model, generate_temp_id, mobile_format
APP='bajaj'

class Command(BaseCommand):

    def handle(self, *args, **options):
        self.upload_asc_data()
    
    def empty_to_none(self, value):
        if value=='':
            return None
        else:
            return int(value)

    def upload_asc_data(self):
        print "Started running function..."
        file_list = ['MECHANIC_DATA.csv']
        file = open("mech_data.txt", "w")
        dealer_list = []
        retailer = get_model('Retailer', APP)
        dist = get_model('Distributor', APP)
        user_profile = get_model('UserProfile', APP)
        mech = get_model('Mechanic', APP)

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

                    temp['district'] = row_list[11].strip()
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
                    dealer_list.append(temp)
        for dealer in dealer_list:
            try:
                mobile = mobile_format(dealer['mobile'])
                mech_object = mech.objects.filter(phone_number=mobile)
                if not mech_object:
                    if not dealer['mech_id']:
                        mech_id = generate_temp_id('TME')
                    else:
                        mech_id=dealer['mech_id']
                    print "MECH ID", mech_id
                    
                    if dealer['dist_id']:
                        dist_object = dist.objects.get(distributor_id=dealer['dist_id'])
                    else:
                        dist_object = None
 
                    ret_obj = retailer.objects.filter(retailer_name=dealer['ret_name'])
                    if not ret_obj:
                        ret_obj = retailer(retailer_name=dealer['ret_name'],
                                 retailer_town=dealer['ret_town'])
                        ret_obj.save()
                    else:
                        ret_obj = ret_obj[0]
                    
                    mech_object = mech(registered_by=dist_object,
                                    preferred_retailer=ret_obj,
                                    mechanic_id=mech_id,
                                    first_name = dealer['first_name'],
                                    last_name = dealer['last_name'],
                                    date_of_birth=dealer['dob'],
                                    phone_number=mobile,           
                                    form_number=dealer['form_no'],
                                    registered_date=dealer['reg_date'],
                                    shop_number =  dealer['shop_no'],
                                    shop_name =  dealer['shop_name'],
                                    shop_address =  dealer['shop_address'],
                                    locality =  dealer['locality'],
                                    tehsil =  dealer['tehsil'],
                                    district =  dealer['district'],
                                    state =  dealer['state'],
                                    pincode =  dealer['pincode'],
                                    shop_wall_length =  dealer['wall_len'],
                                    shop_wall_width =  dealer['wall_width'],
                                    two_stroke_serviced =  dealer['two_stroke'],
                                    four_stroke_serviced =  dealer['four_stroke'],
                                    cng_lpg_serviced =  dealer['cng_lpg'],
                                    diesel_serviced =  dealer['diesel'],
                                    spare_per_month =  dealer['spare_month'],
                                    genuine_parts_used =  dealer['genuine'],
                                    form_status = dealer['complete']
                                    )
                    mech_object.save()
                    file.write("success dealer id is..." + mech_id+'\n')
                else:
                    file.write("already exist dealer id is..." + dealer['mech_id'] +'\n')
            except Exception as ex:
                ex = "{0}: {1} /n".format(dealer['mech_id'], ex)
                file.write(ex)
                break
#                 file.write("Failed dealer id is..." + dealer['id'])
        file.close()

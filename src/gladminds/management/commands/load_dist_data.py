import csv

from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from gladminds.core.loaders.module_loader import get_model
APP='bajaj'

class Command(BaseCommand):

    def handle(self, *args, **options):
        self.upload_asc_data()

    def upload_asc_data(self):
        print "Started running function..."
        file_list = ['DIST_DATA.csv']
        file = open("dist_data.txt", "w")
        dealer_list = []
        asm = get_model('AreaServiceManager', APP)
        dist = get_model('Distributor', APP)
        user_profile = get_model('UserProfile', APP)

#ASM ID Association,Distributor ID,Distributor Name,Distributor Contact,Dist Mail,Dist Mobile Number,City
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
            try:
                dist_object = dist.objects.filter(distributor_id=dealer['id'])
                if not dist_object:
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
                    asm_object = asm.objects.get(asm_id=dealer['asm_id'])
                    dist_object = dist(distributor_id=dealer['id'],
                                              asm=asm_object,
                                              user=dist_user_pro_object)
                    dist_object.save()
                    file.write("success dealer id is..." + dealer['id'])
                else:
                    file.write("already exist dealer id is..." + dealer['id'])
            except Exception as ex:
                ex = "{0} /n".format(ex)
                file.write(ex)
#                 file.write("Failed dealer id is..." + dealer['id'])
        file.close()

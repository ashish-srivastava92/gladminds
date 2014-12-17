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
        self.upload_asc_data()
    
    def empty_to_none(self, value):
        if value=='':
            return None
        else:
            return int(value)

#Part No    Desc    Type    Category     Segment    Model    Supplier

    def upload_asc_data(self):
        print "Started running function..."
        file_list = ['PART_MASTER_DATA.csv']
        file = open("part_master_data.txt", "w")
        spare_list = []
        spare_master = get_model('SparePartMasterData', APP)
        spare_type = get_model('ProductType', APP)
        for i in range(0, 1):
            with open(settings.PROJECT_DIR + '/' + file_list[i], 'r') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=',')
                next(spamreader)
                for row_list in spamreader:
                    temp ={}
                    temp['part_no'] = row_list[0].strip()
                    temp['desc'] = row_list[1].strip()

                    temp['type'] = row_list[2].strip()
                    temp['category']=row_list[3].strip()
                    temp['segment'] = row_list[4].strip()
                    temp['model'] = row_list[5].strip()
                    temp['supplier'] = row_list[6].strip()
                    spare_list.append(temp)
        for spare in spare_list:
            try:
                spare_object = spare_master.objects.filter(serial_number=spare['part_no'])
                if not spare_object:
                    spare_type_object = spare_type.objects.filter(product_type=spare['type'])
                    if not spare_type_object:
                        spare_type_object = spare_type(product_type=spare['type'])
                    else:
                        spare_type_object = spare_type_object[0]
                    spare_object = spare_master(
                                                product_type=spare_type_object,
                                                serial_number = spare['part_no'],
                                                part_model = spare['model'],
                                                description = spare['desc'],
                                                category = spare['category'],
                                                segment_type = spare['segment'],
                                                supplier = spare['supplier']
                                    )
                    spare_object.save()
                    file.write("success part number is..." + spare['part_no']+'\n')
                else:
                    file.write("already exist part number is..." + spare['part_no'] +'\n')
            except Exception as ex:
                ex = "{0}: {1} /n".format(spare['part_no'], ex)
                file.write(ex)
        file.close()

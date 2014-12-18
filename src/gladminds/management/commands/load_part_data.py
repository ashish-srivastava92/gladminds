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
        self.upload_part_master_data()
        self.upload_part_upc_data()
        self.upload_part_point_data()

    def upload_part_master_data(self):
        print "Started uploading part master..."
        file_list = ['PART_MASTER_DATA.csv']
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
    
    def upload_part_upc_data(self):
        print "Started uploading part upc..."
        file_list = ['PART_UPC_DATA.csv']
        spare_list = []
        spare_master = get_model('SparePartMasterData', APP)
        spare_part = get_model('SparePart', APP)
        for i in range(0, 1):
            with open(settings.PROJECT_DIR + '/' + file_list[i], 'r') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=',')
                next(spamreader)
                for row_list in spamreader:
                    temp ={}
                    temp['part_no'] = row_list[0].strip()
                    temp['UPC'] = row_list[1].strip()
                    spare_list.append(temp)
        for spare in spare_list:
            spare_object = spare_part.objects.filter(unique_part_code = spare['UPC'])
            if not spare_object:
                spare_master_object = spare_master.objects.filter(serial_number=spare['part_no'])
                
                spare_object = spare_part(
                                            part_number=spare_master_object[0],
                                            unique_part_code = spare['UPC'])
                spare_object.save()

    def upload_part_point_data(self):
        print "Started uploading part points..."
        file_list = ['PART_POINTS_DATA.csv']
        spare_list = []
        spare_master = get_model('SparePartMasterData', APP)
        spare_part = get_model('SparePart', APP)
        for i in range(0, 1):
            with open(settings.PROJECT_DIR + '/' + file_list[i], 'r') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=',')
                next(spamreader)
                for row_list in spamreader:
                    temp ={}
                    temp['part_no'] = row_list[0].strip()
                    temp['MRP'] = row_list[1].strip()
                    temp['valid_from'] = datetime.datetime.strptime(row_list[2].strip(), '%m/%d/%Y')
                    temp['valid_to'] = datetime.datetime.strptime(row_list[3].strip(), '%m/%d/%Y')
                    temp['territory'] = row_list[4].strip()
                    temp['price'] = row_list[5].strip()
                    temp['points'] = row_list[6].strip()
                    spare_list.append(temp)
        for spare in spare_list:
            spare_object = spare_part.objects.get(part_number__serial_number=spare['part_no'])
            spare_object.points = spare['points']
            spare_object.price = spare['price']
            spare_object.mrp = spare['MRP']
            spare_object.validity_from = spare['valid_from']
            spare_object.validity_to = spare['valid_to']
            spare_object.territory = spare['territory']
            spare_object.save()

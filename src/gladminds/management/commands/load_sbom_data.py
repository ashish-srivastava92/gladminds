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

class Command(BaseCommand):

    def handle(self, *args, **options):
        self.upload_sbom_data()
        
    def upload_sbom_data(self):
        print ''' Started uploading SBOM data data'''
        file_list = ['brand_product_range.csv']
        db_mapping = { 'Motorcycle' : 'bajaj',
                      'Commercial Vehicle' : 'bajajcv',
                      'Probiking' : 'probiking'
                      }
        product_list = []
        brand_vertical = get_model('BrandVertical', APP)
        for i in range(0, 1):
            with open(settings.PROJECT_DIR + '/' + file_list[i], 'r') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=',')
                next(spamreader)
                for row_list in spamreader:
                    temp ={}
                    temp['sku_code'] = row_list[0].strip()
                    temp['description'] = row_list[1].strip()
                    temp['vertical'] = row_list[2].strip()
                    product_list.append(temp)
        
        brand = brand_vertical.objects.get(name='Motorcycle')
        for product in product_list:
            try:
                app = db_mapping.get(product['vertical'])
                brand_product_range = get_model('BrandProductRange', app)
                brand_product_obj = brand_product_range.objects.using(app).get(sku_code=product['sku_code'])
            except Exception as ObjectDoesNotExist:
                brand_product_obj = brand_product_range(sku_code=product['sku_code'],
                                                        description=product['description'],
                                                        vertical=product['vertical'])
                brand_product_obj.save(using=app)
                
                
        file_list = ['sbom_mc_data.csv']
        product_list = self.read_from_csv(file_list)
        self.upload_bom_data(app='bajaj', product_list=product_list)
        
        file_list = ['sbom_cv_data.csv']
        product_list = self.read_from_csv(file_list)
        self.upload_bom_data(app='bajajcv', product_list=product_list)
        
        file_list = ['sbom_probiking_data.csv']
        product_list = self.read_from_csv(file_list)
        self.upload_bom_data(app='probiking', product_list=product_list)
    
    def read_from_csv(self, file_list):
        file_list = file_list
        product_list = []
        for i in range(0, 1):
            with open(settings.PROJECT_DIR + '/' + file_list[i], 'r') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=',')
                next(spamreader)
                for row_list in spamreader:
                    temp ={}
                    temp['bom_number'] = row_list[1].strip()
                    temp['part_number'] = row_list[2].strip()
                    temp['revision_number'] = row_list[3].strip()
                    temp['quantity'] = row_list[4].strip()
                    temp['uom'] = row_list[5].strip()
                    temp['valid_from'] = row_list[6].strip()
                    temp['valid_to'] = row_list[7].strip()
                    temp['plate_id'] = row_list[8].strip()
                    temp['plate_txt'] = row_list[9].strip()
                    temp['serial_number'] = row_list[10].strip()
                    temp['change_number'] = row_list[11].strip()
                    temp['change_number_to'] = row_list[12].strip()
                    temp['item'] = row_list[13].strip()
                    temp['item_id'] = row_list[14].strip()
                    temp['sku_code'] = row_list[15].strip()
                    product_list.append(temp)
        return product_list
    
    def upload_bom_data(self, app, product_list):
        BOMHEADER = get_model('BOMHeader', app)
        BOMPLATE = get_model('BOMPlate', app)
        BOMPART = get_model('BOMPart', app)
        BOMPLATEPART = get_model('BOMPlatePart', app)
        for product in product_list:
            try:
                bom_header_obj = BOMHEADER.objects.using(app).get(bom_number=product['bom_number'])
            except Exception as ObjectDoesNotExist:
                bom_header_obj = BOMHEADER(bom_number=product['bom_number'], sku_code=product['sku_code'])
                bom_header_obj.save(using=app)
            try:
                bom_plate_obj = BOMPLATE.objects.using(app).get(plate_id=product['plate_id'])
            except Exception as ObjectDoesNotExist:
                bom_plate_obj = BOMPLATE(plate_id=product['plate_id'], plate_txt=product['plate_txt'])
                bom_plate_obj.save(using=app)
            try:
                bom_part_obj = BOMPART.objects.using(app).get(part_number=product['part_number'],
                                                              revision_number=product['revision_number'])
            except Exception as ObjectDoesNotExist:
                bom_part_obj = BOMPART(part_number=product['part_number'],
                                       revision_number=product['revision_number'])
                bom_part_obj.save(using=app)
            bom_plate_part_obj = BOMPLATEPART(bom=bom_header_obj, plate=bom_plate_obj, part=bom_part_obj,
                                              quantity=product['quantity'], uom=product['uom'],
                                              valid_from=product['valid_from'], valid_to=product['valid_to'],
                                              serial_number=product['serial_number'],
                                              change_number=product['change_number'],
                                              change_number_to=product['change_number_to'],
                                              item=product['item'], item_id=product['item_id']
                                              )
            bom_plate_part_obj.save(using=app)

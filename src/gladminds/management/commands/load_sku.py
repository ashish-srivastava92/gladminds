import csv
import logging
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
from gladminds.core.model_fetcher import get_model
APP='bajaj'
logger = logging.getLogger("gladminds")

class Command(BaseCommand):

    def handle(self, *args, **options):
        self.upload_sku_data()
        
    def upload_sku_data(self):
        '''Upload sku data'''
        print ''' Started uploading SKU data'''
        file_list = ['brand_product_range.csv']
        vertical_list = [{'name':'Motorcycle', 'description':'Motorcycle'},
                         {'name':'Commercial Vehicle', 'description':'Commercial Vehicle'},
                         {'name':'Probiking', 'description':'Probiking'}]
        for vertical in vertical_list:
            try:
                brand_vertical=get_model('BrandVertical', APP).objects.get(name=vertical['name'])
            except Exception as ObjectDoesNotExist:   
                brand_vertical=get_model('BrandVertical', APP)(name=vertical['name'], description=vertical['description'])
                brand_vertical.save(using=APP)
        product_list=[]
        for i in range(0, 1):
            with open(settings.PROJECT_DIR + '/upload_data/' + file_list[i], 'r') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=',')
                next(spamreader)
                for row_list in spamreader:
                    temp ={}
                    temp['sku_code'] = row_list[0].strip()
                    temp['description'] = row_list[1].strip()
                    temp['vertical'] = row_list[2].strip()
                    product_list.append(temp)
        
        for product in product_list:
            try:
                app = product['vertical']
                brand_product_range = get_model('BrandProductRange', app)
                brand_product_obj = brand_product_range.objects.using(app).get(sku_code=product['sku_code'])
            except Exception as ObjectDoesNotExist:
                brand_product_obj = brand_product_range(sku_code=product['sku_code'],
                                                        description=product['description'])
                brand_product_obj.save(using=app)

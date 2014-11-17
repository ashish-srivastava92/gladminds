import csv
import time

from datetime import datetime
from django.conf import settings
from django.core.management.base import BaseCommand
from gladminds.afterbuy import models as afterbuy_models


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.upload_support_data()

    def upload_support_data(self):
        print "Started running function..."
        file_list = ['support_data.csv']
        industry_list = ['Consumers Durables', 'Automobiles', 'Telecom Service', 'DTH', 'PC', 'Mobile', 'Camera', 'Banking', 'Online Shopping', 'Courier']
        file = open("newfile.txt", "w")
        support_data = []
        brand_objs = []

        for industry_name in  industry_list:
            industry = afterbuy_models.Industry(name=industry_name);
            industry.save()

        for i in range(0, 1):
            with open(settings.PROJECT_DIR + '/' + file_list[i], 'r') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=',')
                next(spamreader)
                for row_list in spamreader:
                    temp = {}
                    temp_compnay ={}
                    temp['industry'] = i
                    temp['company_name'] = row_list[1].strip()
                    temp['brand_name'] = row_list[2].strip()
                    temp['toll_free'] = row_list[3].strip()
                    temp['email_id'] = row_list[4].strip()
                    temp['website'] = row_list[5].strip()
                    temp['feedback'] = row_list[6].strip()
                    support_data.append(temp)

        for brand in support_data:
            brand_obj = afterbuy_models.Brand(industry=brand['industry'], name=temp['brand_name'])
            brand_obj.save()
            support_obj = afterbuy_models.Support(brand=brand_obj, company_name=brand['company_name'], toll_free=brand['toll_free'], website=brand['website'], email_id=brand['email_id'] )
            support_obj.save()


           
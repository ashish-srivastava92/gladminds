import csv
import time

from datetime import datetime
from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from gladminds.aftersell.feed_log_remark import FeedLogWithRemark
from gladminds.feed import SAPFeed

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        self.upload_asc_data()

    def upload_asc_data(self):
        print "Started running function..."
        file_list = ['DEALER_ASC_MATRIX.csv']
        file = open("newfile.txt", "w")
        dealer_list = []
        
        for i in range(0, 1):
            with open(settings.PROJECT_DIR + '/' + file_list[i], 'r') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=',')
                next(spamreader)
                for row_list in spamreader:
                    temp ={}
                    temp['name'] = (row_list[1].strip())[0:29]
                    temp['email'] = row_list[4].strip()
                    temp['dealer_id'] = row_list[0].strip()                    
                    dealer_list.append(temp)
        
        for dealer in dealer_list:
            try:
                dealer_object = User.objects.get(username = dealer['dealer_id'])
            except Exception as ex:
                file.write("Failed dealer id is..." + dealer['dealer_id'])
                
            if dealer_object:
                dealer_object.first_name = dealer['name']
                dealer_object.email = dealer['email']
                dealer_object.save()
            
        file.close()
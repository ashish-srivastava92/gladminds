import csv
import time

from datetime import datetime
from django.conf import settings
from django.core.management.base import BaseCommand
from gladminds.aftersell.feed_log_remark import FeedLogWithRemark
from gladminds.feed import SAPFeed

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        self.upload_asc_data()

    def upload_asc_data(self):
        print "Started running function..."
        file_list = ['testData.csv']
        file = open("newfile.txt", "w")
        asc_list = []
        
        for i in range(0, 1):
            with open(settings.PROJECT_DIR + '/' + file_list[i], 'r') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=',')
                next(spamreader)
                for row_list in spamreader:
                    temp ={}
                    temp['asc_id'] = row_list[5].strip()
                    temp['name'] = row_list[6].strip()
                    temp['phone_number'] = ''
                    temp['address'] = str(row_list[7].strip()) + ", " +str(row_list[8].strip())
                    temp['email'] = row_list[9].strip()
                    temp['dealer_id'] = row_list[0].strip()                    
                    asc_list.append(temp)

        feed_remark = FeedLogWithRemark(len(asc_list),
                                        feed_type='ASC Feed',
                                        action='Received', status=True)
         
        feed_remark = self.save_to_db(feed_type='ASC', data_source=asc_list,
                              feed_remark=feed_remark)
        feed_remark.save_to_feed_log()
        file.write(self.get_response(feed_remark))
        file.close()
        
    def get_response(self, feed_remark):
        return "FAILED" if feed_remark.failed_feeds > 0 else "SUCCESS"

    def save_to_db(self, feed_type=None, data_source=[], feed_remark=None):
        sap_obj = SAPFeed()
        return sap_obj.import_to_db(feed_type=feed_type, data_source=data_source,
                                     feed_remark=feed_remark)

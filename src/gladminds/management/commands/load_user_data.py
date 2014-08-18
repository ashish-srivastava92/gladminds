from django.core.management.base import BaseCommand
from gladminds.feed import SAPFeed
from gladminds.aftersell.feed_log_remark import FeedLogWithRemark
from datetime import datetime
from django.conf import settings

import csv

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        self.upload_user_data()

    def upload_user_data(self):
        print "Started running function..."
        with open(settings.PROJECT_DIR + '/test_data.csv', 'r') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',')
            next(spamreader)
            failed_feed_vins = []
            for row_list in spamreader:
                data = []
                temp ={}
                temp['vin'] = row_list[0].strip()
                temp['kunnr'] = row_list[1].strip()
                temp['engine'] = row_list[2].strip()
                date_string = datetime.strptime(row_list[4].strip(), '%d/%m/%y %H:%M')
                temp['product_purchase_date'] = date_string
                temp['veh_reg_no'] = row_list[5].strip()
                temp['sap_customer_id'] = row_list[6].strip()    
                temp['customer_name'] = row_list[7].strip()
                temp['customer_phone_number'] = row_list[8].strip()
                temp['city'] = row_list[9].strip()
                temp['state'] = row_list[10].strip()
                temp['pin_no'] = row_list[11].strip()
                data.append(temp)
                feed_remark = FeedLogWithRemark(len(data),
                                        feed_type='Purchase Feed',
                                        action='Received', status=True)
                sap_obj = SAPFeed()
                feed_status = sap_obj.import_to_db(feed_type='purchase', data_source=data, feed_remark=feed_remark)
                if feed_status.failed_feeds:
                    failed_feed_vins.append(temp['vin'])
                                
        print "Failed feed vin no. ..", failed_feed_vins 
        print "Completed execution.."
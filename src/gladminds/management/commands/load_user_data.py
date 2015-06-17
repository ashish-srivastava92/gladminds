import csv
from datetime import datetime

from django.conf import settings
from django.core.management.base import BaseCommand

from gladminds.core.feed_log_remark import FeedLogWithRemark
from gladminds.feed import SAPFeed


class Command(BaseCommand):
    
    def handle(self, *args, **options):
        self.upload_user_data()

    def upload_user_data(self):
        print "Started running function..."
        file_list = ['CustomerData_Batch1.csv', 'CustomerData_Batch2.csv', 'CustomerData_Batch3.csv']
        all_failed_vin = {}
        from multiprocessing.dummy import Pool
        import time
        start_time = time.time()
        print "..........START TIME.........", time.time()
        pool = Pool(40)
        self.count = 0
        file = open("newfile.txt", "w")
        for i in range(0, 3):
            data = []
            self.failed_feed_vins = []
            with open(settings.PROJECT_DIR + '/' + file_list[i], 'r') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=',')
                next(spamreader)
                for row_list in spamreader:
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
            
            pool.map(self.process_feed, data)
             
            all_failed_vin[file_list[i]] = self.failed_feed_vins
            print "Failed feed vin no. .. ", file_list[i], self.failed_feed_vins
            file.write(','.join(self.failed_feed_vins))
            file.write('\n\n')
        file.close()
        print "Completed execution.."

    def process_feed(self, data):
        self.count = self.count  + 1
        feed_remark = FeedLogWithRemark(1,
                                    feed_type='Purchase Feed',
                                    action='Received', status=True)
        sap_obj = SAPFeed()
        feed_status = sap_obj.import_to_db(feed_type='purchase', data_source=[data], feed_remark=feed_remark)
        print "cout = ", self.count
        if feed_status.failed_feeds:
            self.failed_feed_vins.append(data['vin'])
            
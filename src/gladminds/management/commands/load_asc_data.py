import csv

from django.conf import settings
from django.core.management.base import BaseCommand
from gladminds.core.managers.feed_log_remark import FeedLogWithRemark
from gladminds.bajaj.feeds.feed import SAPFeed
from gladminds.core.managers.mail import send_asc_registration_mail

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        self.upload_asc_data()

    def upload_asc_data(self):
        print "Started running function..."
        file_list = ['new_asc_list.csv']
        file = open("newfile.txt", "w")
        asc_list = []
        
        for i in range(0, 1):
            with open(settings.PROJECT_DIR + '/' + file_list[i], 'r') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=',')
                next(spamreader)
                for row_list in spamreader:
                    temp ={}
                    temp['asc_id'] = row_list[6].strip()
                    temp['name'] = (row_list[5].strip())[0:29]
                    temp['phone_number'] = ''
                    temp['address'] = str(row_list[8].strip()) + ", " +str(row_list[9].strip())
                    temp['email'] = row_list[7].strip()
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
        for asc in asc_list:
            data = {'receiver': asc['email'], 'name': asc['name'], 'username': asc['asc_id'], 'password': asc['asc_id'] + '@123'}
            send_asc_registration_mail(data)
        
    def get_response(self, feed_remark):
        return "FAILED" if feed_remark.failed_feeds > 0 else "SUCCESS"

    def save_to_db(self, feed_type=None, data_source=[], feed_remark=None):
        sap_obj = SAPFeed()
        return sap_obj.import_to_db(feed_type=feed_type, data_source=data_source,
                                     feed_remark=feed_remark)

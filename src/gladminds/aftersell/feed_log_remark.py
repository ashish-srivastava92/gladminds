from collections import Counter
import json
from gladminds.sqs_tasks import send_report_mail_for_feed_failure
from gladminds.audit import feed_log
from django.conf import settings

class FeedLogWithRemark():

    def __init__(self, total_feeds, feed_type, action, status):
        self.total_feeds = total_feeds
        self.failed_feeds = 0
        self.feed_type = feed_type
        self.action = action
        self.status = status
        self.remarks = Counter()

    def fail_remarks(self, remark):
        self.remarks[remark] += 1
        self.failed_feeds = self.failed_feeds + 1

    def save_to_feed_log(self):
        success_data_count = self.total_feeds - self.failed_feeds
        remarks = json.dumps(self.remarks)
        if remarks and settings.FEED_FAILURE_MAIL_ENABLED:
            send_report_mail_for_feed_failure(remarks=remarks, 
                                              feed_type = self.feed_type)
        feed_log(feed_type=self.feed_type, total_data_count=self.total_feeds,
              failed_data_count=self.failed_feeds,
              success_data_count=success_data_count, status=self.status,
              action=self.action, remarks=remarks)

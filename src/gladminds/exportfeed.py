from suds.client import Client
from suds.transport.http import HttpAuthenticated
from gladminds.audit import feed_log
import logging
logger = logging.getLogger("gladminds")


class BaseExportFeed(object):

    def __init__(self, username=None, password=None, wsdl_url=None,\
                                                        feed_type=None):
        self.username = username
        self.password = password
        self.wsdl_url = wsdl_url
        self.feed_type = feed_type

    def get_http_authenticated(self):
        return HttpAuthenticated(username=self.username,\
                                 password=self.password)

    def get_client(self):
        transport = HttpAuthenticated(\
            username=self.username, password=self.password)
        return Client(url=self.wsdl_url, transport=transport)


class ExportCouponRedeemFeed(BaseExportFeed):

    def export(self, items=None, item_batch=None, total_failed_on_feed=0):
        logger.info(
            "Export {3}: Items:{0} and Item_batch: {1}"\
            .format(items, item_batch, self.feed_type))
        client = self.get_client()
        total_failed = total_failed_on_feed
        for item in items:
            result = client.service.MI_GCP_UCN_Sync(
                ITEM=[item], ITEM_BATCH=item_batch)
            if result[1]['I_STATUS'] == 'SUCCESS':
                export_status = True
            else:
                total_failed = total_failed + 1
                export_status = False

        logger.info("Response from SAP: {0}".format(result))
        feed_log(feed_type=self.feed_type, total_data_count=len(items)\
                 + total_failed_on_feed, failed_data_count=total_failed,\
                 success_data_count=len(items) - total_failed,\
                 action='Sent', status=export_status)

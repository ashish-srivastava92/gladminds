from suds.client import Client
from suds.transport.http import HttpAuthenticated
from gladminds.audit import feed_log
from gladminds.models import common
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
            "Export {2}: Items:{0} and Item_batch: {1}"\
            .format(items, item_batch, self.feed_type))
        client = self.get_client()
        total_failed = total_failed_on_feed
        for item in items:
            result = client.service.MI_GCP_UCN_Sync(
                ITEM=[item], ITEM_BATCH=item_batch)
            if result[1]['I_STATUS'] == 'SUCCESS':
                export_status = True
                logger.error("Sent the details of coupon {0} to sap".format(item['GCP_UCN_NO']))
            else:
                total_failed = total_failed + 1
                export_status = False
                logger.error("Failed to send the details of coupon {0} to sap".format(item['GCP_UCN_NO']))

        logger.info("Response from SAP: {0}".format(result))
        feed_log(feed_type=self.feed_type, total_data_count=len(items)\
                 + total_failed_on_feed, failed_data_count=total_failed,\
                 success_data_count=len(items) + total_failed_on_feed - total_failed,\
                 action='Sent', status=export_status)


class ExportASCRegistrationFeed(BaseExportFeed):

    def export(self, item=None, item_batch=None):
        logger.info(
            "Export {2}: Item:{0} and Item_batch: {1}"\
            .format(item, item_batch, self.feed_type))
        client = self.get_client()

        result = client.service.postASC(
            ITEM=[item], ITEM_BATCH=item_batch)
        if not result[1]['I_STATUS'] == 'SUCCESS':
            raise
        return

class ExportCustomerRegistrationFeed(BaseExportFeed):

    def export(self, items=None, item_batch=None, total_failed_on_feed=0):
        logger.info(
            "Export {2}: Items:{0} and Item_batch: {1}"\
            .format(items, item_batch, self.feed_type))
        client = self.get_client()
        total_failed = total_failed_on_feed
        for item in items:
            logger.info("Trying to send SAP the ID: {0}".format(item['CUSTOMER_ID']))
            try:
                result = client.service.SI_GCPCstID_sync(
                    ITEM=[item], ITEM_BATCH=item_batch)
                logger.info("Response from SAP: {0}".format(result))
                if result[1]['STATUS'] == 'SUCCESS':
                    common.CustomerTempRegistration.objects.filter(temp_customer_id=item['CUSTOMER_ID']).update(sent_to_sap=True)
                    export_status = True
                    logger.info("Sent the details of customer ID {0} to sap".format(item['CUSTOMER_ID']))
                else:
                    total_failed = total_failed + 1
                    export_status = False
                    logger.error("Failed to send the details of customer ID {0} to sap".format(item['CUSTOMER_ID']))
            except Exception as ex:
                logger.error("Failed to send the details to sap")
                logger.error(ex)
        feed_log(feed_type=self.feed_type, total_data_count=len(items)\
                 + total_failed_on_feed, failed_data_count=total_failed,\
                 success_data_count=len(items) + total_failed_on_feed - total_failed,\
                 action='Sent', status=export_status)
        

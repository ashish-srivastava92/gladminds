from suds.client import Client
from suds.transport.http import HttpAuthenticated
from gladminds.audit import feed_log
from gladminds.models import common
from django.conf import settings
import logging
logger = logging.getLogger("gladminds")


class BaseExportFeed(object):

    def __init__(self, username=None, password=None, wsdl_url=None, \
                                                        feed_type=None):
        self.username = username
        self.password = password
        self.wsdl_url = wsdl_url
        self.feed_type = feed_type

    def get_http_authenticated(self):
        return HttpAuthenticated(username=self.username, \
                                 password=self.password)

    def get_client(self):
        transport = HttpAuthenticated(\
            username=self.username, password=self.password)
        client = Client(url=self.wsdl_url, transport=transport)
        cache = client.options.cache
        cache.setduration(seconds=settings.FILE_CACHE_DURATION)
        return client


class ExportCouponRedeemFeed(BaseExportFeed):

    def export(self, items=None, item_batch=None, total_failed_on_feed=0):
        logger.info(
            "Export {0}".format(self.feed_type))
        client = self.get_client()
        total_failed = total_failed_on_feed
        for item in items:
            logger.info("Trying to send SAP the coupon: {0}"\
                        .format(item))
            try:            
                result = client.service.MI_GCP_UCN_Sync(
                    ITEM=[item], ITEM_BATCH=item_batch)
                logger.info("Response from SAP: {0}".format(result))
                if result[1]['I_STATUS'] == 'SUCCESS':
                    try:
                        export_status = True
                        coupon = common.CouponData.objects.get(unique_service_coupon=item['GCP_UCN_NO'])
                        coupon.sent_to_sap = True
                        coupon.save()
                        logger.info("Sent the details of coupon {0} to sap".format(item['GCP_UCN_NO']))
                    except Exception as ex:
                        logger.error("Coupon with id {0} does not exist".format(item['GCP_UCN_NO']))
                else:
                    total_failed = total_failed + 1
                    export_status = False
                    logger.error("Failed to send the details of coupon {0} to sap".format(item['GCP_UCN_NO']))
            except Exception as ex:
                logger.error("Failed to send the details to sap")
                logger.error(ex)
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
        export_status = False
        logger.info(
            "Export {2}: Items:{0} and Item_batch: {1}"\
            .format(items, item_batch, self.feed_type))
        client = self.get_client()
        total_failed = total_failed_on_feed
        for item in items:
            logger.info("Trying to send SAP the ID: {0}"\
                        .format(item['CUSTOMER_ID']))
            try:
                result = client.service.SI_GCPCstID_sync(
                    item_custveh=[{"item": item}], item=item_batch)
                logger.info("Response from SAP: {0}".format(result))
                if result[0]['item'][0]['STATUS'] == 'SUCCESS':
                    try:
                        temp_customer_object = common.CustomerTempRegistration.objects.get(temp_customer_id=
                                                                                           item['CUSTOMER_ID'])
                        temp_customer_object.sent_to_sap = True
                        if result[2]:
                            temp_customer_object.remarks = result[2]['item'][0]['REMARKS']
                        else: 
                            temp_customer_object.tagged_sap_id = result[1]['item'][0]['PARTNER']
                        temp_customer_object.save()
                        export_status = True
                        logger.info("Sent the details of customer ID {0} to sap".format(item['CUSTOMER_ID']))
                    except Exception as ex:
                        logger.error("Customer with id {0} does not exist".format(item['CUSTOMER_ID']))
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

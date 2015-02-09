from suds.client import Client
from suds.transport.http import HttpAuthenticated
from datetime import datetime
from gladminds.core.managers.audit_manager import feed_log, feed_failure_log
from gladminds.bajaj import models
from django.conf import settings
import logging
from gladminds.core import utils
from gladminds.core.managers.feed_log_remark import FeedLogWithRemark
from gladminds.bajaj.services.coupons.feed_models import save_to_db
from gladminds.bajaj.services.coupons.import_feed import SAPFeed
import json
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
        client = Client(url=self.wsdl_url, transport=transport)
        cache = client.options.cache
        cache.setduration(seconds=settings.FILE_CACHE_DURATION)
        return client


class ExportMemberTempFeed(BaseExportFeed):
    
    def export_data(self, start_date=None, end_date=None):
        results = models.Mechanic.objects.filter(sent_to_sap=0)
        items = []
        total_failed = 0
        item_batch = {
            'TIMESTAMP': datetime.now().strftime("%Y-%m-%dT%H:%M:%S")}
        for mechanic in results:
            try:
                item = {
                        "TEMP_ID": mechanic.mechanic_id,
                        "FIRST_NAME": mechanic.first_name,
                        "MIDDLE_NAME": mechanic.middle_name,
                        "LAST_NAME": mechanic.first_name,
                        "BIRTH_DT": mechanic.date_of_birth.date().strftime("%Y-%m-%d"),
                        "ADDR1": mechanic.adress_line_1,
                        "ADDR2": mechanic.adress_line_2,
                        "ADDR3": mechanic.adress_line_3,
                        "ADDR4": mechanic.adress_line_4,
                        "ADDR5": mechanic.adress_line_5,
                        "ADDR6": mechanic.adress_line_6,
                        "STATE": mechanic.state,
                        "PIN_CODE": mechanic.pincode,
                        "DSB_CODE": mechanic.registered_by_distributor.distributor_id,
                        "MOBILE_NO":str(mechanic.phone_number),
                    }                        
                items.append(item)
            except Exception as ex:
                logger.error("error on data mechanic data from db %s" % str(ex))
                total_failed = total_failed + 1
        return items, item_batch, total_failed

    def export(self, items=None, item_batch=None, total_failed_on_feed=0):
        logger.info(
            "Export {0}".format(self.feed_type))
        client = self.get_client()
        total_failed = total_failed_on_feed
        for item in items:
            logger.info("Trying to send SAP the member: {0}"\
                        .format(item))
            try:            
                result = client.service.OP_SI_Mech_Sync(
                    DT_Mac={'item':[item]}, DT_STAMP={'item':item_batch})
                logger.info("Response from SAP: {0}".format(result))
                if result[1][0]['STATUS'] == 'SUCCESS':
                    try:
                        export_status = True
                        member_detail = models.Mechanic.objects.get(unique_service_coupon=item['TEMP_ID'])
                        member_detail.sent_to_sap = True
                        member_detail.save()
                        logger.info("Sent the details of member {0} to sap".format(item['TEMP_ID']))
                    except Exception as ex:
                        logger.error("Error in member update:{0}::{1}".format(item['TEMP_ID'], ex))
                else:
                    total_failed = total_failed + 1
                    export_status = False
                    logger.error("Failed to send the details of member {0} to sap".format(item['TEMP_ID']))
            except Exception as ex:
                logger.error("Failed to send the member details to sap")
                logger.error(ex)
        feed_log(feed_type=self.feed_type, total_data_count=len(items)\
                 + total_failed_on_feed, failed_data_count=total_failed,\
                 success_data_count=len(items) + total_failed_on_feed - total_failed,\
                 action='Sent', status=export_status)

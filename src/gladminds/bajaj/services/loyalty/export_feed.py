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
from gladminds.bajaj.services.feed_resources import BaseExportFeed
import json
logger = logging.getLogger("gladminds")

class ExportMemberTempFeed(BaseExportFeed):
    
    def export_data(self):
        results = models.Mechanic.objects.filter(sent_to_sap=0, form_status='Complete')
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
                        "ADDR1": mechanic.address_line_1,
                        "ADDR2": mechanic.address_line_2,
                        "ADDR3": mechanic.address_line_3,
                        "ADDR4": mechanic.address_line_4,
                        "ADDR5": mechanic.address_line_5,
                        "ADDR6": mechanic.address_line_6,
                        "STATE": mechanic.state.state_code,
                        "PIN_CODE": mechanic.pincode,
                        "DSB_CODE": mechanic.registered_by_distributor.distributor_id,
                        "MOBILE_NO":str(mechanic.phone_number),
                    }                        
                items.append(item)
            except Exception as ex:
                logger.error("[ExportMemberTempFeed]: error fetching from db {0}".format(ex))
                total_failed = total_failed + 1
        return items, item_batch, total_failed

    def export(self, items=None, item_batch=None, total_failed_on_feed=0):
        logger.info(
            "[ExportMemberTempFeed]: Export {0}".format(self.feed_type))
        client = self.get_client()
        total_failed = total_failed_on_feed
        for item in items:
            logger.info("[ExportMemberTempFeed]: Trying to send SAP the member: {0}"\
                        .format(item))
            try:            
                result = client.service.SI_Mech_Sync(
                    DT_Mac={'item':[item]}, DT_STAMP={'item':item_batch})
                logger.info("[ExportMemberTempFeed]: Response from SAP: {0}".format(result))
                if result[0]['item'][0]['STATUS'] == 'SUCCESS':
                    try:
                        export_status = True
                        member_detail = models.Mechanic.objects.get(mechanic_id=item['TEMP_ID'])
                        member_detail.sent_to_sap = True
                        member_detail.save()
                        logger.info("[ExportMemberTempFeed]: Sent the details of member {0} to sap".format(item['TEMP_ID']))
                    except Exception as ex:
                        logger.error("[ExportMemberTempFeed]: Error in member update:{0}::{1}".format(item['TEMP_ID'], ex))
                else:
                    total_failed = total_failed + 1
                    export_status = False
                    logger.error("[ExportMemberTempFeed]: {0}:: Not received success from sap".format(item['TEMP_ID']))
            except Exception as ex:
                logger.error("[ExportMemberTempFeed]:  Error in member update:{0}::{1}".format(item['TEMP_ID'], ex))
        feed_log(feed_type=self.feed_type, total_data_count=len(items)\
                 + total_failed_on_feed, failed_data_count=total_failed,\
                 success_data_count=len(items) + total_failed_on_feed - total_failed,\
                 action='Sent', status=export_status)

class ExportAccumulationFeed(BaseExportFeed):
    
    def export_data(self):
        results = models.AccumulationRequest.objects.filter(sent_to_sap=0)
        items = []
        total_failed = 0
        item_batch = {
            'T_STAMP': datetime.now().strftime("%Y-%m-%dT%H:%M:%S")}
        for accumulation in results:
            try:                
                item = {
                        "CRDAT": accumulation.created_date.date().strftime("%Y-%m-%d"),
                        "TANSSID": accumulation.transaction_id,
                        "POINTS": accumulation.points,
                        "MECHID": accumulation.member.permanent_id,
                        "MOBNO": str(accumulation.member.phone_number),
                    }
                upcs = accumulation.upcs.all()
                for upc in upcs:
                    item['UPCED'] = upc.unique_part_code
                    items.append(item)
            except Exception as ex:
                logger.error("[ExportAccumulationFeed]: error fetching from db {0}".format(ex))
                total_failed = total_failed + 1
        return items, item_batch, total_failed
    
    def export(self, items=None, item_batch=None, total_failed_on_feed=0):
        logger.info(
            "[ExportAccumulationFeed]: Export {0}".format(self.feed_type))
        client = self.get_client()
        total_failed = total_failed_on_feed
        for item in items:
            logger.info("[ExportAccumulationFeed]: Trying to send SAP the member: {0}"\
                        .format(item))
            try:            
                result = client.service.SI_Acc_Sync(
                    DT_Accum={'item':[item]}, DT_STAMP={'Item_Stamp':item_batch})
                logger.info("[ExportAccumulationFeed]: Response from SAP: {0}".format(result))
                if result[0]['DT_Item']['STATUS'] == 'SUCCESS':
                    try:
                        export_status = True
                        accumulation_detail = models.AccumulationRequest.objects.get(transaction_id=item['TANSSID'])
                        accumulation_detail.sent_to_sap = True
                        accumulation_detail.save()
                        logger.info("[ExportAccumulationFeed]: Sent the details of member {0} to sap".format(item['TANSSID']))
                    except Exception as ex:
                        logger.error("[ExportAccumulationFeed]: Error in sending accumulation:{0}::{1}".format(item['TANSSID'], ex))
                else:
                    total_failed = total_failed + 1
                    export_status = False
                    logger.error("[ExportAccumulationFeed]: {0}:: Not received success from sap".format(item['TANSSID']))
            except Exception as ex:
                logger.error("[ExportAccumulationFeed]: Error in sending accumulation :{0}::{1}".format(item['TANSSID'], ex))
        feed_log(feed_type=self.feed_type, total_data_count=len(items)\
                 + total_failed_on_feed, failed_data_count=total_failed,\
                 success_data_count=len(items) + total_failed_on_feed - total_failed,\
                 action='Sent', status=export_status)

from suds.client import Client
from suds.transport.http import HttpAuthenticated
from datetime import datetime
from django.db.models import Q
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
        export_status = False
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
                        member_detail = models.Mechanic.objects.get(mechanic_id=item['TEMP_ID'])
                        member_detail.sent_to_sap = True
                        member_detail.save()
                        logger.info("[ExportMemberTempFeed]: Sent the details of member {0} to sap".format(item['TEMP_ID']))
                        export_status = True
                    except Exception as ex:
                        logger.error("[ExportMemberTempFeed]: Error in member update:{0}::{1}".format(item['TEMP_ID'], ex))
                else:
                    total_failed = total_failed + 1
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
                    item['UPCED'] = str(upc.unique_part_code)
                    items.append(item)
            except Exception as ex:
                logger.error("[ExportAccumulationFeed]: error fetching from db {0}".format(ex))
                total_failed = total_failed + 1
        return items, item_batch, total_failed, results
    
    def export(self, items=None, item_batch=None, total_failed_on_feed=0, query_set=None):
        logger.info(
            "[ExportAccumulationFeed]: Export {0}".format(self.feed_type))
        export_status = False
        client = self.get_client()
        total_failed = total_failed_on_feed
        try:
            result = client.service.SI_Acc_Sync(
                    DT_Accum={'Item':items}, DT_STAMP={'Item_Stamp':item_batch})
            logger.info("[ExportAccumulationFeed]: Response from SAP: {0}".format(result))
            if result[0]['STATUS'] == 'SUCCESS':
                query_set.update(sent_to_sap=True)
                logger.error("[ExportAccumulationFeed]: Sent details o SAP")
            else:
                total_failed = total_failed + len(items)
                logger.error("[ExportAccumulationFeed]: Not received success from sap")
        except Exception as ex:
            logger.error("[ExportAccumulationFeed]: Error in sending accumulation :{0}".format(ex))
                
#         for item in items:
#             logger.info("[ExportAccumulationFeed]: Trying to send SAP the member: {0}"\
#                         .format(item))
#             try:            
#                 result = client.service.SI_Acc_Sync(
#                     DT_Accum={'Item':[item]}, DT_STAMP={'Item_Stamp':item_batch})
#                 logger.info("[ExportAccumulationFeed]: Response from SAP: {0}".format(result))
#                 if result[0]['STATUS'] == 'SUCCESS':
#                     try:
#                         accumulation_detail = models.AccumulationRequest.objects.get(transaction_id=item['TANSSID'])
#                         accumulation_detail.sent_to_sap = True
#                         accumulation_detail.save()
#                         logger.info("[ExportAccumulationFeed]: Sent the details of member {0} to sap".format(item['TANSSID']))
#                         export_status = True
#                     except Exception as ex:
#                         logger.error("[ExportAccumulationFeed]: Error in sending accumulation:{0}::{1}".format(item['TANSSID'], ex))
#                 else:
#                     total_failed = total_failed + 1
#                     logger.error("[ExportAccumulationFeed]: {0}:: Not received success from sap".format(item['TANSSID']))
#             except Exception as ex:
#                 logger.error("[ExportAccumulationFeed]: Error in sending accumulation :{0}::{1}".format(item['TANSSID'], ex))
        feed_log(feed_type=self.feed_type, total_data_count=len(items)\
                 + total_failed_on_feed, failed_data_count=total_failed,\
                 success_data_count=len(items) + total_failed_on_feed - total_failed,\
                 action='Sent', status=export_status)

class ExportRedemptionFeed(BaseExportFeed):
    
    def export_data(self):
        args = {}
        results = models.RedemptionRequest.objects.filter(~Q(image_url=''), Q(status='Delivered'), Q(sent_to_sap=0))
        items = []
        total_failed = 0
        item_batch = {
            'TIMESTAMP': datetime.now().strftime("%Y-%m-%dT%H:%M:%S")}
        for redemption in results:
            try:
                item = {
                        "CRDAT": redemption.created_date.date().strftime("%Y-%m-%d"),
                        "MECHID": redemption.member.permanent_id,
                        "MOBNO": str(redemption.member.phone_number),
                        "PARTNID": redemption.partner.partner_id,
                        "APRDAT": redemption.approved_date.date().strftime("%Y-%m-%d"),
                        "EXPDLVDAT": redemption.expected_delivery_date.date().strftime("%Y-%m-%d"),
                        "SHPDAT": redemption.shipped_date.date().strftime("%Y-%m-%d"),
                        "SHPID": redemption.tracking_id,
                        "DELVDAT": redemption.delivery_date.date().strftime("%Y-%m-%d"),
                        "PODNO": redemption.pod_number,
                        "PODDOC": redemption.image_url,
                        "TRANSID": redemption.transaction_id,
                    }
                items.append(item)
            except Exception as ex:
                logger.error("[ExportRedemptionFeed]: error fetching from db {0}".format(ex))
                total_failed = total_failed + 1
        return items, item_batch, total_failed, results
    
    def export(self, items=None, item_batch=None, total_failed_on_feed=0, query_set=None):
        logger.info(
            "[ExportRedemptionFeed]: Export {0}".format(self.feed_type))
        export_status = False
        client = self.get_client()
        total_failed = total_failed_on_feed
        try: 
            result = client.service.SI_Redum_Sync(
                        DT_Redum={'Item':items}, DT_STAMP={'Item':item_batch})
            logger.info("[ExportRedemptionFeed]: Response from SAP: {0}".format(result))
            if result[0]['STATUS'] == 'SUCCESS':
                query_set.update(sent_to_sap=True)
                export_status = True
                logger.error("[ExportRedemptionFeed]: Sent details o SAP")
            else:
                total_failed = total_failed + len(items)
                logger.error("[ExportRedemptionFeed]: Not received success from sap")
        except Exception as ex:
                logger.error("[ExportRedemptionFeed]: Error in sending accumulation :{0}".format(ex))
#         for item in items:
#             logger.info("[ExportRedemptionFeed]: Trying to send SAP the member: {0}"\
#                         .format(item))
#             try:            
#                 result = client.service.SI_Redum_Sync(
#                     DT_Redum={'Item':[item]}, DT_STAMP={'Item':item_batch})
#                 logger.info("[ExportRedemptionFeed]: Response from SAP: {0}".format(result))
#                 if result[0]['STATUS'] == 'SUCCESS':
#                     try:
#                         redemption_detail = models.RedemptionRequest.objects.get(transaction_id=item['TRANSID'])
#                         redemption_detail.sent_to_sap = True
#                         redemption_detail.save()
#                         logger.info("[ExportRedemptionFeed]: Sent the details of member {0} to sap".format(item['TRANSID']))
#                         export_status = True
#                     except Exception as ex:
#                         logger.error("[ExportRedemptionFeed]: Error in sending accumulation:{0}::{1}".format(item['TRANSID'], ex))
#                 else:
#                     total_failed = total_failed + 1
#                     logger.error("[ExportRedemptionFeed]: {0}:: Not received success from sap".format(item['TRANSID']))
#             except Exception as ex:
#                 logger.error("[ExportRedemptionFeed]: Error in sending accumulation :{0}::{1}".format(item['TRANSID'], ex))
        feed_log(feed_type=self.feed_type, total_data_count=len(items)\
                 + total_failed_on_feed, failed_data_count=total_failed,\
                 success_data_count=len(items) + total_failed_on_feed - total_failed,\
                 action='Sent', status=export_status)
        

class ExportDistributorFeed(BaseExportFeed):

    def export_data(self):
        args = {}
        results = models.Distributor.objects.filter(sent_to_sap=0)
        items = []
        total_failed = 0
        item_batch = {
            'I_STAMP': datetime.now().strftime("%Y-%m-%dT%H:%M:%S")}
        for distributor in results:
            try:
                asm=None
                if distributor.asm:
                    asm = distributor.asm.asm_id
                
                item = {
                        "DISTID": distributor.distributor_id,
                        "NAME": distributor.name,
                        "EMAIL": distributor.email,
                        "MOBNO": str(distributor.phone_number) if distributor.phone_number else None,
                        "CITY": distributor.city,
                        "ASMID": asm,
                    }
                items.append(item)
            except Exception as ex:
                logger.error("[ExportDistributorFeed]: error fetching from db {0}".format(ex))
                total_failed = total_failed + 1
        return items, item_batch, total_failed
    
    def export(self, items=None, item_batch=None, total_failed_on_feed=0):
        logger.info(
            "[ExportDistributorFeed]: Export {0}".format(self.feed_type))
        export_status = False
        client = self.get_client()
        total_failed = total_failed_on_feed
        for item in items:
            logger.info("[ExportDistributorFeed]: Trying to send SAP the member: {0}"\
                        .format(item))
            try:
                result = client.service.SI_Dist_Sync(
                    DT_DIST={'Item':[item]}, DT_STAMP={'Item_Stamp':item_batch})
                logger.info("[ExportDistributorFeed]: Response from SAP: {0}".format(result))
                if result[0]['STATUS'] == 'SUCCESS':
                    try:
                        distributor_detail = models.Distributor.objects.get(distributor_id=item['DISTID'])
                        distributor_detail.sent_to_sap = True
                        distributor_detail.save()
                        logger.info("[ExportDistributorFeed]: Sent the details of member {0} to sap".format(item['DISTID']))
                        export_status = True
                    except Exception as ex:
                        logger.error("[ExportDistributorFeed]: Error in sending accumulation:{0}::{1}".format(item['DISTID'], ex))
                else:
                    total_failed = total_failed + 1
                    logger.error("[ExportDistributorFeed]: {0}:: Not received success from sap".format(item['DISTID']))
            except Exception as ex:
                logger.error("[ExportDistributorFeed]: Error in sending accumulation :{0}::{1}".format(item['DISTID'], ex))
        feed_log(feed_type=self.feed_type, total_data_count=len(items)\
                 + total_failed_on_feed, failed_data_count=total_failed,\
                 success_data_count=len(items) + total_failed_on_feed - total_failed,\
                 action='Sent', status=export_status)
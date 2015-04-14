import csv
import logging
import os
import time
from datetime import datetime, timedelta

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group
from django.db.models import signals

from gladminds.core.services import message_template as templates
from gladminds.core import utils
from gladminds.bajaj import models
from gladminds.core.managers.audit_manager import feed_log, sms_log
from gladminds.core.cron_jobs.queue_utils import send_job_to_queue
from gladminds.core.auth_helper import Roles
from gladminds.core.services.feed_resources import BaseFeed, BaseExportFeed
logger = logging.getLogger("gladminds")

USER_GROUP = {'dealer': Roles.DEALERS,
              'ASC': Roles.ASCS,
              'SA':Roles.SERVICEADVISOR}

def load_feed():
    FEED_TYPE = settings.FEED_TYPE
    if FEED_TYPE is 'CSV':
        CSVFeed()
    elif FEED_TYPE is 'SAP':
        SAPFeed()


class CSVFeed(object):

    def __init__(self):
        file_path = settings.DATA_CSV_PATH
        brand_path = file_path + "/brand_data.csv"
        dealer_path = file_path + "/dealer_data.csv"
        product_path = file_path + "/product_data.csv"
        product_purchase_path = file_path + "/product_purchase.csv"
        coupon_redeem_path = file_path + "/coupon_redeem.csv"

        # Import data from CSV
        if os.path.isfile(brand_path):
            brand_feed = self.get_dict(brand_path)
            brand_data = BrandProductTypeFeed(data_source=brand_feed)
            brand_data.import_data()
            self.rename(fullpath=brand_path)

        if os.path.isfile(dealer_path):
            dealer_feed = self.get_dict(dealer_path)
            dealer_data = DealerAndServiceAdvisorFeed(data_source=dealer_feed)
            dealer_data.import_data()
            self.rename(fullpath=dealer_path)

        if os.path.isfile(product_path):
            productcoupon_feed = self.get_dict(product_path)
            product_data = ProductDispatchFeed(data_source=productcoupon_feed)
            product_data.import_data()
            self.rename(fullpath=product_path)

        if os.path.isfile(product_purchase_path):
            productpurchase_feed = self.get_dict(product_purchase_path)
            product_purchase_data = ProductPurchaseFeed(
                data_source=productpurchase_feed)
            product_purchase_data.import_data()
            self.rename(fullpath=product_purchase_path)

        if os.path.isfile(coupon_redeem_path):
            coupon_redeem_feed = self.get_dict(coupon_redeem_path)
            coupon_redeem_data = ProductServiceFeed(
                data_source=coupon_redeem_feed)
            coupon_redeem_data.import_data()
            self.rename(fullpath=coupon_redeem_path)

    def get_dict(self, filepath):
        csv_dict = {}
        try:
            csv_dict = csv.DictReader(open(filepath))
        except IOError as ie:
            logger.exception("[Excpetion]: {0}".format(ie))
        return csv_dict

    def rename(self, fullpath):
        try:
            timestamp_str = str(int(time.time()))
            os.rename(fullpath, fullpath + '-' + timestamp_str)
        except OSError as oe:
            logger.exception("[Excpetion]: {0}".format(oe))


class SAPFeed(object):

    def import_to_db(self, feed_type=None, data_source=[], feed_remark=None):
        function_mapping = {
            'brand': BrandProductTypeFeed,
            'dealer': DealerAndServiceAdvisorFeed,
            'dispatch': ProductDispatchFeed,
            'purchase': ProductPurchaseFeed,
            'ASC': ASCFeed,
            'old_fsc': OldFscFeed,
            'credit_note': CreditNoteFeed,
            'asc_sa': ASCAndServiceAdvisorFeed,
            'bomheader': BOMHeaderFeed,
            'bomitem': BOMItemFeed,
            'eco_release': ECOReleaseFeed,
            'container_tracker':ContainerTrackerFeed,
            'eco_implementation':ECOImplementationFeed,
        }
        feed_obj = function_mapping[feed_type](data_source=data_source,
                                             feed_remark=feed_remark)
        return feed_obj.import_data()

class BrandProductTypeFeed(BaseFeed):

    def import_data(self):
        for product in self.data_source:
            try:
                product_type = models.ProductType(product_type=product['product_type'])
                product_type.save()
            except Exception as ex:
                logger.info(
                    "[Exception: BrandProductTypeFeed_product_type]: {0}".format(ex))
                continue


class DealerAndServiceAdvisorFeed(BaseFeed):

    def import_data(self):
        total_failed = 0
        for dealer in self.data_source:
            try:
                dealer_data = self.check_or_create_dealer(dealer_id=dealer['id'],
                                address=dealer['address'], cdms_flag=dealer['cdms_flag'])
                mobile_number_active = self.check_mobile_active(dealer, dealer_data)
                if mobile_number_active and dealer['status']=='Y':
                    raise ValueError(dealer['phone_number'] + ' is active under another dealer')
                try:
                    service_advisor = models.ServiceAdvisor.objects.select_related('user__user').get(
                                        service_advisor_id=dealer['service_advisor_id'])
                    if service_advisor.user.phone_number != dealer['phone_number']:
                        service_advisor.user.phone_number = dealer['phone_number']
                        logger.info(
                        "[Info: DealerAndServiceAdvisorFeed_sa]: Updated phone number for {0}"
                        .format(dealer['service_advisor_id']))
                except ObjectDoesNotExist as odne:
                    logger.info(
                    "[Exception:  DealerAndServiceAdvisorFeed_sa]: {0}"
                    .format(odne))
                    sa_user = self.register_user(Roles.SERVICEADVISOR, username=dealer['service_advisor_id'],
                                                 first_name=dealer['name'],
                                                 phone_number=dealer['phone_number'])
                    service_advisor = models.ServiceAdvisor(
                                            service_advisor_id=dealer['service_advisor_id'], 
                                            dealer=dealer_data, user=sa_user)
                service_advisor.status = unicode(dealer['status'])
                service_advisor.save()
            except Exception as ex:
                total_failed += 1
                ex = "{0}".format(ex)
                logger.error(ex)
                self.feed_remark.fail_remarks(ex)
                continue

        return self.feed_remark

    def check_mobile_active(self, dealer, dealer_data):
        list_mobile = models.ServiceAdvisor.objects.active(dealer['phone_number'])
        list_active_mobile = list_mobile.exclude(dealer=dealer_data,
                                                 service_advisor_id=dealer['service_advisor_id'])
        if list_active_mobile:
            return True
        return False

def compare_purchase_date(date_of_purchase):
    valid_msg_days = models.Constant.objects.get(constant_name = "welcome_msg_active_days").constant_value
    valid_msg_days_delta = timedelta(days=int(valid_msg_days))
    purchased_days = datetime.now().date()-date_of_purchase
    if purchased_days <= valid_msg_days_delta:
        return True
    else:
        return False
    

class ProductDispatchFeed(BaseFeed):

    def import_data(self):
        for product in self.data_source:
            try:
                product_data = models.ProductData.objects.get(product_id=product['vin'])
            except ObjectDoesNotExist as done:
                logger.info(
                    '[Info: ProductDispatchFeed_product_data]: {0}'.format(done))
                try:
                    dealer_data = self.check_or_create_dealer(dealer_id=product['dealer_id'])
                    product_data = models.ProductData(
                        product_id=product['vin'], invoice_date=product['invoice_date'], 
                        dealer_id=dealer_data, sku_code=product['product_type'])
                    product_data.save()
                    logger.info('[Successful: ProductDispatchFeed_product_data_save]:VIN-{0} UCN-{1}'.format(product['vin'], product['unique_service_coupon']))
                except Exception as ex:
                    ex = '''[Exception: ProductDispatchFeed_product_data_save]:{0} VIN - {1}'''.format(ex, product['vin'])
                    self.feed_remark.fail_remarks(ex)
                    logger.error(ex)
                    continue
            try:
                if not product['unique_service_coupon']:
                    continue
                valid_coupon = models.CouponData.objects.filter(unique_service_coupon=product['unique_service_coupon'])
                service_type_exists = models.CouponData.objects.filter(product__product_id=product['vin'], service_type=str(product['service_type']))
                if service_type_exists and not valid_coupon:
                    service_type_error = 'VIN already has coupon of service type {0}'.format(product['service_type'])
                    logger.error(service_type_error)
                    raise ValueError(service_type_error)
                elif not valid_coupon:
                    coupon_data = models.CouponData(unique_service_coupon=product['unique_service_coupon'],
                            product=product_data, valid_days=product['valid_days'],
                            valid_kms=product['valid_kms'], service_type=product['service_type'],
                            status=product['coupon_status'])
                    coupon_data.save()
                    logger.info('[Successful: ProductDispatchFeed_product_data_save]:VIN - {0} UCN - {1}'.format(product['vin'], product['unique_service_coupon']))
                    
                elif valid_coupon[0].product.product_id == product['vin'] and str(valid_coupon[0].service_type) == str(product['service_type']):
                    logger.info('UCN is already saved in database. VIN - {0} UCN - {1}'.format(product['vin'], product['unique_service_coupon']))
                    continue
                else:
                    coupon_exist_error = 'Coupon already registered for VIN {0}'.format(valid_coupon[0].product.product_id)
                    logger.error(coupon_exist_error)
                    raise ValueError(coupon_exist_error)
            except Exception as ex:   
                ex = '''[Error: ProductDispatchFeed_product_data_save]: VIN - {0} Coupon - {1} {2}'''.format(
                                        product['vin'], product['unique_service_coupon'], ex)
                self.feed_remark.fail_remarks(ex)
                logger.error(ex)
                continue

        return self.feed_remark

    def get_or_create_product_type(self, product_type=None):
        brand_list = [{
            'product_type': product_type,
            'product_name': product_type,
        }]
        obj_brand = BrandProductTypeFeed(data_source=brand_list)
        obj_brand.import_data()

class ProductPurchaseFeed(BaseFeed):

    def import_data(self):
        for product in self.data_source:
            try:
                product_data = models.ProductData.objects.get(product_id=product['vin'])
                if product_data.customer_phone_number and product_data.customer_id == product['sap_customer_id']:
                    post_save.disconnect(
                        update_coupon_data, sender=models.ProductData)

                if not product_data.customer_id  or product_data.customer_id.find('T') == 0:
                    product_data.customer_id = product['sap_customer_id']
                    product_data.engine = product["engine"]
                    product_data.veh_reg_no =  product['veh_reg_no']
                
                product_purchase_date = product['product_purchase_date']
                product_data.purchase_date = product_purchase_date
                product_data.customer_phone_number = product['customer_phone_number']    
                product_data.customer_name = product['customer_name']
                product_data.customer_city = product['city']
                product_data.customer_state = product['state']
                product_data.customer_pincode = product['pin_no']
                product_data.save()
                
                post_save.connect(
                    update_coupon_data, sender=models.ProductData)
            except ObjectDoesNotExist as done:
                ex='[Info: ProductPurchaseFeed_product_data]: VIN- {0} :: {1}'''.format(product['vin'], done)
                logger.error(ex)
                self.feed_remark.fail_remarks(ex)
                vin_sync_feed = models.VinSyncFeedLog.objects.filter(product_id = product['vin'],ucn_count=-1)
                if vin_sync_feed:
                    vin_sync_feed=vin_sync_feed[0]
                    vin_sync_feed.sent_to_sap=False
                else:
                    vin_sync_feed=models.VinSyncFeedLog(product_id = product['vin'],ucn_count=-1) 
                vin_sync_feed.save()
            except Exception as ex:
                ex = '''[Exception: ProductPurchaseFeed_product_data]: VIN- {0} :: {1}'''.format(product['vin'], ex)
                self.feed_remark.fail_remarks(ex)
                logger.error(ex)
                continue

        return self.feed_remark


class ProductServiceFeed(BaseFeed):

    def import_data(self):
        for redeem in self.data_source:
            try:
                closed_date = datetime.strptime(
                    redeem['closed_date'], '%d-%m-%Y %H:%M:%S')
                actual_service_date = datetime.strptime(
                    redeem['actual_service_date'], '%d-%m-%Y %H:%M:%S')
                coupon_data = models.CouponData.objects.filter(vin__vin=redeem['vin'], unique_service_coupon=redeem['unique_service_coupon']).update(
                    closed_date=closed_date, actual_service_date=actual_service_date, actual_kms=redeem['actual_kms'], status=2)
            except Exception as ex:
                continue


def update_coupon_data(sender, **kwargs):
    from gladminds.sqs_tasks import send_on_product_purchase
    instance = kwargs['instance']
    logger.info("triggered update_coupon_data")
    if instance.customer_phone_number:
        product_purchase_date = instance.purchase_date
        vin = instance.product_id
        coupon_data = models.CouponData.objects.filter(product=instance)
        for coupon in coupon_data:
            mark_expired_on = product_purchase_date + \
                timedelta(days=int(coupon.valid_days))
            coupon_object = models.CouponData.objects.get(
                product=instance, unique_service_coupon=coupon.unique_service_coupon)
            coupon_object.mark_expired_on = mark_expired_on
            coupon_object.extended_date = mark_expired_on
            coupon_object.save()
        
        try:
            customer_name=instance.customer_name
            customer_phone_number = utils.get_phone_number_format(instance.customer_phone_number)
            customer_id=instance.customer_id
            temp_customer_data = models.CustomerTempRegistration.objects.filter(product_data__product_id=vin)
            if temp_customer_data and not temp_customer_data[0].temp_customer_id == customer_id:
                message = templates.get_template('SEND_REPLACED_CUSTOMER_ID').format(
                    customer_name=customer_name, sap_customer_id=customer_id)
            elif instance.customer_id.find('T') == 0:
                message = templates.get_template('SEND_TEMPORARY_CUSTOMER_ID').format(
                    customer_name=customer_name, sap_customer_id=customer_id)
            else:
                if compare_purchase_date(product_purchase_date):
                    message = templates.get_template('SEND_CUSTOMER_ON_PRODUCT_PURCHASE').format(
                    customer_name=customer_name, sap_customer_id=customer_id)
                else:
                    message = templates.get_template('SEND_REPLACED_CUSTOMER_ID').format(
                    customer_name=customer_name, sap_customer_id=customer_id)
            
            sms_log(
                settings.BRAND, receiver=customer_phone_number, action='SEND TO QUEUE', message=message)
            send_job_to_queue(send_on_product_purchase, {"phone_number":customer_phone_number, "message":message, "sms_client":settings.SMS_CLIENT}) 
        except Exception as ex:
            logger.info("[Exception]: Signal-In Update Coupon Data %s" % ex)

post_save.connect(update_coupon_data, sender=models.ProductData)
    
class OldFscFeed(BaseFeed):
    
    def import_data(self):
        for fsc in self.data_source:
            product_data = models.ProductData.objects.filter(product_id=fsc['vin'])
            dealer_id = str(int(fsc['dealer']))
            if len(product_data)==0:
                self.save_to_old_fsc_table(dealer_id, fsc['service'], 'product_id', fsc['vin'])
            else:
                coupon_data = models.CouponData.objects.filter(product__product_id=fsc['vin'],
                                        service_type=int(fsc['service']))
                if len(coupon_data) == 0:
                    self.save_to_old_fsc_table(dealer_id, fsc['service'], 'service_type', fsc['service'], vin = product_data[0] )
                else:
                    cupon_details = coupon_data[0]
                    cupon_details.status = 6
                    cupon_details.closed_date = datetime.now()
                    cupon_details.sent_to_sap = True
                    cupon_details.servicing_dealer = dealer_id
                    cupon_details.save()
        return self.feed_remark

    def save_to_old_fsc_table(self, dealer_detail,st, missing_field,missing_value, vin=None):
        try:
            old_fsc_obj = models.OldFscData.objects.get(product=vin, service_type=int(st), missing_field=missing_field)
        except Exception as ex:
            old_coupon_data = models.OldFscData(product=vin, service_type = int(st),
                                             status=6, closed_date=datetime.now(), sent_to_sap = True,
                                             servicing_dealer = dealer_detail, missing_field=missing_field, 
                                             missing_value=missing_value)
            old_coupon_data.save()

class CreditNoteFeed(BaseFeed):
    
    def import_data(self):
        for credit_note in self.data_source:
            try:
                message=coupon_data=None
                product_data = models.ProductData.objects.filter(product_id=credit_note['vin'])
                if not product_data:
                    message='VIN: {0} does not exits'.format(credit_note['vin'])
                    raise ValueError(message)
                else:
                    coupon_data = models.CouponData.objects.filter(product__product_id=credit_note['vin'],
                                    unique_service_coupon=credit_note['unique_service_coupon'])
                    if not coupon_data:
                        message='VIN: {0} coupon:{1}:: coupon does not exists'.format(credit_note['vin'],
                                                            credit_note['unique_service_coupon'])
                        raise ValueError(message)
                    elif coupon_data[0].service_type!=int(credit_note['service_type']):
                        message='VIN: {0} coupon:{1}:: service type does not match'.format(credit_note['vin'],
                                                            credit_note['unique_service_coupon'])
                        raise ValueError(message)
                    else:
                        valid_coupon = coupon_data[0]
                        valid_coupon.status = 2
                        valid_coupon.actual_kms = credit_note['actual_kms']
                        valid_coupon.actual_service_date = credit_note['actual_service_date']
                        valid_coupon.credit_note = credit_note['credit_note']
                        valid_coupon.credit_date = credit_note['credit_date']
                        valid_coupon.servicing_dealer = credit_note['dealer']
#                         valid_coupon.closed_date = credit_note['closed_date']
                        valid_coupon.closed_date = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
                        valid_coupon.save()
                logger.info("updated credit details:: vin : {0} coupon : {1} service_type : {2}".format(
                                credit_note['vin'], credit_note['unique_service_coupon'],
                                credit_note['service_type']))
            except Exception as ex:
                ex = "[Exception: CREDIT_NOTE_FEED]:{0}".format(ex)
                logger.error(ex)
                self.feed_remark.fail_remarks(ex)
            if credit_note['cdms_doc_number']:
                self.save_cdms_data(credit_note, coupon_data, message)
        return self.feed_remark

    def save_cdms_data(self, credit_note, coupon_data, message):
        valid_coupon=None
        if coupon_data:
            valid_coupon=coupon_data[0]

        cdms_data=models.CDMSData(unique_service_coupon=valid_coupon,
                        received_date=credit_note['received_date'],
                        cdms_date=credit_note['cdms_date'],
                        cdms_doc_number=credit_note['cdms_doc_number'],
                        remarks=message)
        cdms_data.save()

class ASCFeed(BaseFeed):
    def import_data(self):
        for asc in self.data_source:
            asc_data = models.AuthorizedServiceCenter.objects.filter(asc_id=asc['asc_id'])
            if not asc_data:
                dealer_data = None
                if asc['dealer_id']:
                    dealer_data = self.check_or_create_dealer(dealer_id=asc['dealer_id'])
                try:
                    asc_obj = self.register_user(Roles.ASCS, username=asc['asc_id'],
                                                address=asc['address'])
                    asc_data = models.AuthorizedServiceCenter(user=asc_obj,asc_id=asc['asc_id'],
                                    dealer=dealer_data)
                    asc_data.save()
                except Exception as ex:
                    ex = "[Exception: ASCFeed_dealer_data]: {0}".format(ex)
                    logger.error(ex)
                    self.feed_remark.fail_remarks(ex)
            else:
                ex = "[Exception: ASCFeed_dealer_data] asc_id {0} already exists".format(asc['asc_id'])
                logger.error(ex)
        return self.feed_remark
    
class ASCAndServiceAdvisorFeed(BaseFeed):

    def import_data(self):
        total_failed = 0
        for asc in self.data_source:
            try:
                asc_data = models.AuthorizedServiceCenter.objects.get(asc_id=asc['id'])
            except ObjectDoesNotExist as ex:
                asc_obj = self.register_user(Roles.ASCS, username=asc['id'])
                asc_data = models.AuthorizedServiceCenter(user=asc_obj,asc_id=asc['id'])
            try:
                mobile_number_active = self.check_mobile_active(asc, asc_data)
                if mobile_number_active and asc['status']=='Y':
                    raise ValueError(asc['phone_number'] + ' is active under another dealer')
                try:
                    service_advisor = models.ServiceAdvisor.objects.select_related('user__user').get(
                                        service_advisor_id=asc['service_advisor_id'])
                    if service_advisor.user.phone_number != asc['phone_number']:
                        service_advisor.user.phone_number = asc['phone_number']
                        logger.info(
                        "[Info: DealerAndServiceAdvisorFeed_sa]: Updated phone number for {0}"
                        .format(asc['service_advisor_id']))
                except ObjectDoesNotExist as odne:
                    logger.info(
                    "[Exception:  DealerAndServiceAdvisorFeed_sa]: {0}"
                    .format(odne))
                    sa_user = self.register_user(Roles.SERVICEADVISOR, username=asc['service_advisor_id'],
                                                 first_name=asc['name'],
                                                 phone_number=asc['phone_number'])
                    service_advisor = models.ServiceAdvisor(
                                            service_advisor_id=asc['service_advisor_id'], 
                                            asc=asc_data, user=sa_user)
                service_advisor.status = unicode(asc['status'])
                service_advisor.save()
            except Exception as ex:
                total_failed += 1
                ex = "{0}".format(ex)
                logger.error(ex)
                self.feed_remark.fail_remarks(ex)
                continue

        return self.feed_remark

    def check_mobile_active(self, asc, asc_data):
        list_mobile = models.ServiceAdvisor.objects.active(asc['phone_number'])
        list_active_mobile = list_mobile.exclude(asc=asc_data,
                                                 service_advisor_id=asc['service_advisor_id'])
        if list_active_mobile:
            return True
        return False
    
class BOMItemFeed(BaseFeed):
  
    def import_data(self):
        for bom in self.data_source:
            try:
                bom_item_obj = models.BOMItem(bom_number=bom['bom_number'], part_number=bom['part_number'],
                                            revision_number=bom['revision_number'], quantity=bom['quantity'], 
                                            uom=bom['uom'], change_number_to=bom['change_number_to'],
                                            valid_from=bom['valid_from'], valid_to=bom['valid_to'], 
                                            plate_id=bom['plate_id'], plate_txt=bom['plate_txt'],
                                            serial_number=bom['serial_number'], change_number=bom['change_number'],
                                            item=bom['item'], item_id=bom['item_id'])                
                bom_item_obj.save()
            except Exception as ex:
                ex="[Exception: ]: BOMItemFeed {0}".format(ex)
                logger.error(ex)
                self.feed_remark.fail_remarks(ex)
                
        return self.feed_remark

class BOMHeaderFeed(BaseFeed):    

    def import_data(self):
        for bom in self.data_source:
            try:
                bom_header_obj = models.BOMHeader(sku_code=bom['sku_code'], plant=bom['plant'],
                                                  bom_type=bom['bom_type'], bom_number=bom['bom_number_header'],
                                                  created_on=bom['created_on'], valid_from=bom['valid_from_header'],
                                                  valid_to=bom['valid_to_header'])
                bom_header_obj.save() 
            except Exception as ex:
                ex="[Exception: ]: BOMHeaderFeed {0}".format(ex)
                logger.error(ex)
                self.feed_remark.fail_remarks(ex)

        return self.feed_remark
    
class ECOReleaseFeed(BaseFeed):    

    def import_data(self):
        for eco_obj in self.data_source:
            try:
                if eco_obj['eco_release_date'] == "0000-00-00" or not eco_obj['eco_release_date']:
                    eco_release_date=None
                else:
                    eco_release_date=datetime.strptime(eco_obj['eco_release_date'], "%Y-%m-%d")
                eco_release_obj = models.ECORelease(eco_number=eco_obj['eco_number'], eco_release_date=eco_release_date,
                                                    eco_description=eco_obj['eco_description'], action=eco_obj['action'], parent_part=eco_obj['parent_part'],
                                                    add_part=eco_obj['add_part'], add_part_qty=eco_obj['add_part_qty'], add_part_rev=eco_obj['add_part_rev'],
                                                    add_part_loc_code=eco_obj['add_part_loc_code'], del_part=eco_obj['del_part'], del_part_qty=eco_obj['del_part_qty'],
                                                    del_part_rev=eco_obj['del_part_rev'], del_part_loc_code=eco_obj['del_part_loc_code'], 
                                                    models_applicable=eco_obj['models_applicable'], serviceability=eco_obj['serviceability'], 
                                                    interchangebility=eco_obj['interchangebility'], reason_for_change=eco_obj['reason_for_change'])
                eco_release_obj.save() 
            except Exception as ex:
                ex="[Exception: ]: ECOReleaseFeed {0}".format(ex)
                logger.error(ex)
                self.feed_remark.fail_remarks(ex)
        return self.feed_remark

class ContainerTrackerFeed(BaseFeed):

    def import_data(self):
        for tracker_obj in self.data_source:
            try:
                try:
                    container_tracker_obj=models.ContainerTracker.objects.get(zib_indent_num=tracker_obj['zib_indent_num'],
                                                                              lr_number=tracker_obj['lr_number'])
                except ObjectDoesNotExist as odne:
                    transporter_data = self.check_or_create_transporter(transporter_id=tracker_obj['transporter_id'],
                                                                        name=tracker_obj['tranporter_name'])
                    container_tracker_obj = models.ContainerTracker(zib_indent_num=tracker_obj['zib_indent_num'], 
                                                                    consignment_id=tracker_obj['consignment_id'],
                                                                    truck_no=tracker_obj['truck_no'], 
                                                                    lr_number=tracker_obj['lr_number'],                                                                    
                                                                    do_num=tracker_obj['do_num'],
                                                                    transporter=transporter_data)

                    if tracker_obj['lr_date'] == "0000-00-00" or not tracker_obj['lr_date']:
                        lr_date=None
                    else:
                        lr_date=datetime.strptime(tracker_obj['lr_date'], "%Y-%m-%d")
                    container_tracker_obj.lr_date=lr_date
                
                if tracker_obj['gatein_date'] != "0000-00-00":
                    gatein_date=datetime.strptime(tracker_obj['gatein_date'], "%Y-%m-%d")
                    status="Closed"
                else:
                    gatein_date=None
                    status="Open"
                container_tracker_obj.gatein_date=gatein_date
                container_tracker_obj.gatein_time=tracker_obj['gatein_time']
                container_tracker_obj.status=status
                container_tracker_obj.save() 
            except Exception as ex:
                ex="[Exception: ]: ContainerTrackerFeed {0}".format(ex)
                logger.error(ex)
                self.feed_remark.fail_remarks(ex)
        
        return self.feed_remark

class ECOImplementationFeed(BaseFeed):

    def import_data(self):
        for eco_obj in self.data_source:
            try:
                if eco_obj['change_date'] == "0000-00-00" or not eco_obj['change_date']:
                    change_date=None
                else:
                    change_date=datetime.strptime(eco_obj['change_date'], "%Y-%m-%d")
                eco_implementation_obj = models.ECOImplementation(change_no=eco_obj['change_no'],change_date=change_date,
                                                           change_time=eco_obj['change_time'],plant=eco_obj['plant'],
                                                           action=eco_obj['action'],parent_part=eco_obj['parent_part'],
                                                           added_part=eco_obj['added_part'],added_part_qty=eco_obj['added_part_qty'],
                                                           deleted_part=eco_obj['deleted_part'],deleted_part_qty=eco_obj['deleted_part_qty'],
                                                           chassis_number=eco_obj['chassis_number'],engine_number=eco_obj['engine_number'],
                                                           eco_number=eco_obj['eco_number'],reason_code=eco_obj['reason_code'],
                                                           remarks=eco_obj['remarks']
                                                           )
                eco_implementation_obj.save() 
            except Exception as ex:
                ex="[Exception: ]: ECOImplementationFeed {0}".format(ex)
                logger.error(ex)
                self.feed_remark.fail_remarks(ex)
        return self.feed_remark

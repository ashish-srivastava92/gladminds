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

from gladminds.core.managers import audit_manager
from gladminds.bajaj.services import message_template as templates
from gladminds.core import utils
from gladminds.bajaj import models
from gladminds.core.managers.audit_manager import feed_log
from gladminds.core.utils import get_task_queue

logger = logging.getLogger("gladminds")
USER_GROUP = {'dealer': 'dealers', 'ASC': 'ascs', 'SA':'sas', 'customer':"customer"}

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
        if feed_type == 'brand':
            brand_obj = BrandProductTypeFeed(data_source=data_source,
                                             feed_remark=feed_remark)
            return brand_obj.import_data()
        elif feed_type == 'dealer':
            dealer_obj = DealerAndServiceAdvisorFeed(data_source=data_source,
                                                     feed_remark=feed_remark)
            return dealer_obj.import_data()
        elif feed_type == 'dispatch':
            dispatch_obj = ProductDispatchFeed(data_source=data_source,
                                               feed_remark=feed_remark)
            return dispatch_obj.import_data()
        elif feed_type == 'purchase':
            purchase_obj = ProductPurchaseFeed(data_source=data_source,
                                               feed_remark=feed_remark)
            return purchase_obj.import_data()
        elif feed_type == 'ASC':
            asc_obj = ASCFeed(data_source=data_source,
                                               feed_remark=feed_remark)
            return asc_obj.import_data()
        elif feed_type == 'old_fsc':
            fsc_obj = OldFscFeed(data_source=data_source,
                                               feed_remark=feed_remark)
            return fsc_obj.import_data()
        elif feed_type == 'credit_note':
            credit_note_obj = CreditNoteFeed(data_source=data_source,
                                               feed_remark=feed_remark)
            return credit_note_obj.import_data()


class BaseFeed(object):

    def __init__(self, data_source=None, feed_remark=None):
        self.data_source = data_source
        self.feed_remark = feed_remark

    def import_data(self):
        pass

    def register_user(self, user, group=None, username=None, first_name='', last_name='',
                          email='', address='', phone_number=None):
        logger.info('New {0} Registration with id - {1}'.format(user, username))
        if not group:
            group = USER_GROUP[user]
        try:
            user_group = Group.objects.get(name=group)
        except ObjectDoesNotExist as ex:
            logger.info(
                "[Exception: new_ registration]: {0}"
                .format(ex))
            user_group = Group.objects.create(name=group)
            user_group.save()
        if username:
            try:
                new_user = User.objects.get(username=username)
            except ObjectDoesNotExist as ex:
                logger.info(
                    "[Exception: new_ registration]: {0}"
                    .format(ex))    
                new_user = User(
                    username=username, first_name=first_name, last_name=last_name, email=email)
                password = username + settings.PASSWORD_POSTFIX
                new_user.set_password(password)
                new_user.save()
                new_user.groups.add(user_group)
                new_user.save()
                logger.info(user + ' {0} registered successfully'.format(username))
            try:
                user_details = models.UserProfile.objects.get(user=new_user)
            except ObjectDoesNotExist as ex:
                user_details = models.UserProfile(user=new_user,
                                        phone_number=phone_number, address=address)
                user_details.save()
            return user_details
        else:
            logger.info('{0} id is not provided.'.format(user))
            raise Exception('{0} id is not provided.'.format(user))   

    def check_or_create_dealer(self, dealer_id, address=None):
        try:
            dealer_data = models.Dealer.objects.get(
                dealer_id=dealer_id)
        except ObjectDoesNotExist as odne:
            logger.debug(
                "[Exception: new_dealer_data]: {0}"
                .format(odne))
            user = self.register_user('dealer', username=dealer_id)
            dealer_data = models.Dealer(user=user,
                dealer_id=dealer_id)
            dealer_data.save()            
        return dealer_data


class BrandProductTypeFeed(BaseFeed):

    def import_data(self):
        for product in self.data_source:
            try:
                product_type = models.ProductType(product_name=product[
                                                      'product_name'], product_type=product['product_type'])
                product_type.save()
            except Exception as ex:
                logger.info(
                    "[Exception: BrandProductTypeFeed_product_type]: {0}".format(ex))
                continue


class DealerAndServiceAdvisorFeed(BaseFeed):

    def import_data(self):
        total_failed = 0
        for dealer in self.data_source:
            dealer_data = self.check_or_create_dealer(dealer_id=dealer['dealer_id'],
                                address=dealer['address'])
            try:
                mobile_number_active = self.check_mobile_active(dealer, dealer_data)
                if mobile_number_active and dealer['status']=='Y':
                    raise ValueError(dealer['phone_number'] + ' is active under another dealer')
                try:
                    service_advisor = models.ServiceAdvisor.objects.get(
                                        service_advisor_id=dealer['service_advisor_id'])
                    if service_advisor.phone_number != dealer['phone_number']:
                        service_advisor.phone_number = dealer['phone_number']
                        logger.info(
                        "[Info: DealerAndServiceAdvisorFeed_sa]: Updated phone number for {0}"
                        .format(dealer['service_advisor_id']))
                except ObjectDoesNotExist as odne:
                    logger.info(
                    "[Exception:  DealerAndServiceAdvisorFeed_sa]: {0}"
                    .format(odne))
                    service_advisor = models.ServiceAdvisor(
                                            service_advisor_id=dealer['service_advisor_id'], 
                                            name=dealer['name'], phone_number=dealer['phone_number'])
                    self.register_user('SA', username=dealer['service_advisor_id'])
                service_advisor.save()
                
                try:
                    service_advisor_dealer = models.ServiceAdvisorDealerRelationship.objects.get(
                                               service_advisor_id=service_advisor, dealer_id=dealer_data)
                    service_advisor_dealer.status = unicode(dealer['status'])
                except ObjectDoesNotExist as odne:
                    service_advisor_dealer = models.ServiceAdvisorDealerRelationship(
                                                dealer_id=dealer_data,
                                                service_advisor_id=service_advisor,
                                                status=dealer['status'])
                    
                service_advisor_dealer.save()
                    
            except Exception as ex:
                total_failed += 1
                ex = "{0}".format(ex)
                logger.error(ex)
                self.feed_remark.fail_remarks(ex)
                continue

        return self.feed_remark

    def check_mobile_active(self, dealer, dealer_data):
        list_mobile = models.ServiceAdvisorDealerRelationship.objects.filter(
                                service_advisor_id__phone_number=dealer['phone_number'], status='Y')
        list_active_mobile = list_mobile.exclude(dealer_id=dealer_data,
                                service_advisor_id__service_advisor_id=dealer['service_advisor_id'])
        if list_active_mobile:
            return True
        return False


class ProductDispatchFeed(BaseFeed):

    def import_data(self):
        for product in self.data_source:
            try:
                product_data = models.ProductData.objects.get(
                    product_id=product['vin'])
            except ObjectDoesNotExist as done:
                logger.info(
                    '[Info: ProductDispatchFeed_product_data]: {0}'.format(done))
                try:
                    dealer_data = self.check_or_create_dealer(dealer_id=product['dealer_id'])
                    self.get_or_create_product_type(
                        product_type=product['product_type'])
                    producttype_data = models.ProductType.objects.get(
                        product_type=product['product_type'])
                    invoice_date = product['invoice_date']
                    product_data = models.ProductData(
                        product_id=product['vin'], product_type=producttype_data, invoice_date=invoice_date, dealer_id=dealer_data)
                    product_data.save()
                    logger.info('[Successful: ProductDispatchFeed_product_data_save]:VIN - {0}'.format(product['vin'], product['unique_service_coupon']))
                except Exception as ex:

                    ex = '''[Exception: ProductDispatchFeed_product_data_save]:
                         {0} VIN - {1}'''.format(ex, product['vin'])
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
                product_data = models.ProductData.objects.get(
                    vin=product['vin'])
                if product_data.customer_phone_number and product_data.sap_customer_id == product['sap_customer_id']:
                    post_save.disconnect(
                        update_coupon_data, sender=models.ProductData)
                try:
                    customer_data = models.GladMindUsers.objects.get(
                        phone_number=product['customer_phone_number'])
                except ObjectDoesNotExist as odne:
                    logger.info(
                        '[Exception: ProductPurchaseFeed_customer_data]: {0}'.format(odne))
                    # Register this customer
                    gladmind_customer_id = utils.generate_unique_customer_id()
                    user=self.register_user('customer', username=gladmind_customer_id)
                    customer_data = models.GladMindUsers(user=user, gladmind_customer_id=gladmind_customer_id, phone_number=product[
                                                         'customer_phone_number'], registration_date=datetime.now(),
                                                         customer_name=product['customer_name'], pincode=product['pin_no'],
                                                         state=product['state'], address=product['city'])
                    customer_data.save()

                if not product_data.sap_customer_id  or product_data.sap_customer_id.find('T') == 0:
                    product_purchase_date = product['product_purchase_date']
                    product_data.sap_customer_id = product['sap_customer_id']
                    product_data.product_purchase_date = product_purchase_date
                    product_data.engine = product["engine"]
                    product_data.veh_reg_no =  product['veh_reg_no']
                
                product_data.customer_phone_number = customer_data    
                product_data.save()
                
                post_save.connect(
                    update_coupon_data, sender=models.ProductData)
            except Exception as ex:

                ex = '''[Exception: ProductPurchaseFeed_product_data]:
                         {0} VIN - {1}'''.format(ex, product['vin'])
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
    from gladminds.core.cron_jobs.sqs_tasks import send_on_product_purchase
    instance = kwargs['instance']
    logger.info("triggered update_coupon_data")
    if instance.customer_phone_number:
        product_purchase_date = instance.product_purchase_date
        vin = instance.vin
        coupon_data = models.CouponData.objects.filter(vin=instance)
        for coupon in coupon_data:
            mark_expired_on = product_purchase_date + \
                timedelta(days=int(coupon.valid_days))
            coupon_object = models.CouponData.objects.get(
                vin=instance, unique_service_coupon=coupon.unique_service_coupon)
            coupon_object.mark_expired_on = mark_expired_on
            coupon_object.extended_date = mark_expired_on
            coupon_object.save()
        
        try:
            customer_data = models.GladMindUsers.objects.get(
                phone_number=instance.customer_phone_number)
            temp_customer_data = models.CustomerTempRegistration.objects.filter(product_data__vin=vin)
            if temp_customer_data and not temp_customer_data[0].temp_customer_id == instance.sap_customer_id:
                message = templates.get_template('SEND_REPLACED_CUSTOMER_ID').format(
                    customer_name=customer_data.customer_name, sap_customer_id=instance.sap_customer_id)
            elif instance.sap_customer_id.find('T') == 0:
                message = templates.get_template('SEND_TEMPORARY_CUSTOMER_ID').format(
                    customer_name=customer_data.customer_name, sap_customer_id=instance.sap_customer_id)
            else:
                message = templates.get_template('SEND_CUSTOMER_ON_PRODUCT_PURCHASE').format(
                    customer_name=customer_data.customer_name, sap_customer_id=instance.sap_customer_id)
            customer_phone_number = utils.get_phone_number_format(instance.customer_phone_number.phone_number)
            if settings.ENABLE_AMAZON_SQS:
                task_queue = get_task_queue()
                task_queue.add("send_on_product_purchase", {"phone_number": 
                                customer_phone_number, "message":message,
                                "sms_client":settings.SMS_CLIENT})
            else:
                send_on_product_purchase.delay(
                phone_number=customer_phone_number, message=message, sms_client=settings.SMS_CLIENT)
 
            audit.audit_log(
                reciever=customer_phone_number, action='SEND TO QUEUE', message=message)
        except Exception as ex:
            logger.info("[Exception]: Signal-In Update Coupon Data %s" % ex)

post_save.connect(update_coupon_data, sender=models.ProductData)
    
class OldFscFeed(BaseFeed):
    
    def import_data(self):
        for fsc in self.data_source:
            try:
                dealer_data = self.check_or_create_dealer(dealer_id=fsc['dealer'])
                product_data = models.ProductData.objects.get(vin=fsc['vin'])
                coupon_data = models.CouponData.objects.filter(vin__vin=fsc['vin'],
                                            service_type=int(fsc['service']))
                if len(coupon_data) == 0:
                    try:
                        old_fsc_obj = models.OldFscData.objects.get(vin=product_data, service_type=int(fsc['service']) )
                    except Exception as ex:
                        ex = "[Exception: OLD_FSC_FEED]: For VIN {0} service type {1} does not exist in old fsc database::{2}".format(
                            fsc['vin'], fsc['service'], ex)
                        logger.info(ex)
                        old_coupon_data = models.OldFscData(vin=product_data, service_type = int(fsc['service']),
                                                         status=6, closed_date=datetime.now(), sent_to_sap = True, servicing_dealer = dealer_data)
                        old_coupon_data.save()
                else:
                    cupon_details = coupon_data[0]
                    cupon_details.status = 6
                    cupon_details.closed_date = datetime.now()
                    cupon_details.sent_to_sap = True
                    cupon_details.servicing_dealer = dealer_data
                    cupon_details.save()
            except Exception as ex:
                ex = "[Exception: OLD_FSC_FEED]: VIN {0} does not exist::{1}".format(
                            fsc['vin'], ex)
                logger.error(ex)
                self.feed_remark.fail_remarks(ex)
        return self.feed_remark

class CreditNoteFeed(BaseFeed):
    
    def import_data(self):
        for credit_note in self.data_source:
            try:
                coupon_data = models.CouponData.objects.get(vin__vin=credit_note['vin'],
                                    unique_service_coupon=credit_note['unique_service_coupon'],
                                    service_type=int(credit_note['service_type']))
                coupon_data.credit_note = credit_note['credit_note']
                coupon_data.credit_date = credit_note['credit_date']
                coupon_data.save()
                logger.info("updated credit details:: vin : {0} coupon : {1} service_type : {2}".format(
                            credit_note['vin'], credit_note['unique_service_coupon'],
                            credit_note['service_type']))
            except Exception as ex:
                ex = "[Exception: CREDIT_NOTE_FEED]: For VIN {0} with coupon {1} of service type {2}:: {3}".format(
                            credit_note['vin'], credit_note['unique_service_coupon'],
                            credit_note['service_type'], ex)
                logger.error(ex)
                self.feed_remark.fail_remarks(ex)
        return self.feed_remark

class ASCFeed(BaseFeed):
    def import_data(self):
        for asc in self.data_source:
            asc_data = models.AuthorizedServiceCenter.objects.filter(asc_id=asc['asc_id'])
            if not asc_data:
                dealer_data = None
                if asc['dealer_id']:
                    dealer_data = self.check_or_create_dealer(dealer_id=asc['dealer_id'])
                try:
                    asc_obj = self.register_user('ASC', username=asc['asc_id'],
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
    

class CouponRedeemFeedToSAP(BaseFeed):

    def export_data(self, start_date=None, end_date=None):
        results = models.CouponData.objects.filter(sent_to_sap=0,
                            status=2).select_related('vin', 'customer_phone_number__phone_number')
        items = []
        total_failed = 0
        item_batch = {
            'TIMESTAMP': datetime.now().strftime("%Y-%m-%dT%H:%M:%S")}
        for redeem in results:
            try:
                #added the condition only for the previous coupons with no servicing dealer details
                if redeem.servicing_dealer:
                    servicing_dealer = redeem.servicing_dealer.dealer_id
                else:
                    servicing_dealer = redeem.vin.dealer_id.dealer_id
                item = {
                        "CHASSIS": redeem.vin.vin,
                        "GCP_KMS": redeem.actual_kms,
                        "GCP_KUNNR": servicing_dealer,
                        "GCP_UCN_NO": redeem.unique_service_coupon,
                        "PRODUCT_TYPE": redeem.vin.product_type.product_type,
                        "SERVICE_TYPE": str(redeem.service_type),
                        "SER_AVL_DT": redeem.actual_service_date.date().strftime("%Y-%m-%d"),
                    }                        
                items.append(item)
            except Exception as ex:
                logger.error("error on data coupon data from db %s" % str(ex))
                total_failed = total_failed + 1
        return items, item_batch, total_failed


class ASCRegistrationToSAP(BaseFeed):

    def export_data(self, asc_phone_number=None):
        asc_form_obj = aftersell_models.ASCSaveForm.objects\
            .get(phone_number=asc_phone_number, status=1)

        item_batch = {
            'TIMESTAMP': asc_form_obj.timestamp.strftime("%Y-%m-%dT%H:%M:%S")}

        item = {
            "ASC_NAME": asc_form_obj.name,
            "ASC_MOBILE": asc_form_obj.phone_number,
            "ASC_EMAIL": asc_form_obj.email,
            "ASC_ADDRESS": asc_form_obj.address,
            "ASC_ADDRESS_PINCODE": asc_form_obj.pincode,
            "KUNNAR": "hardcoded",
        }
        return {"item": item, "item_batch": item_batch}

class CustomerRegistationFeedToSAP(BaseFeed):

    def export_data(self, start_date=None, end_date=None):
        results = models.CustomerTempRegistration.objects.filter(sent_to_sap=False).select_related('product_data')
        items = []
        total_failed = 0
        item_batch = {
            'TIME_STAMP': datetime.now().strftime("%Y%m%d%H%M%S")}
        for redeem in results:
            try:
                item = {
                    "CHASSIS": redeem.product_data.vin,
                    "KUNNR": redeem.product_data.dealer_id.dealer_id,
                    "CUSTOMER_ID" : redeem.temp_customer_id,
                    "ENGINE" : redeem.product_data.engine,
                    "VEH_SL_DT": redeem.product_purchase_date.date().strftime("%Y-%m-%d"),
                    "CUSTOMER_NAME": redeem.new_customer_name,
                    "CUST_MOBILE": redeem.new_number,
                    
                }
                items.append(item)
            except Exception as ex:
                logger.error("error on customer info from db %s" % str(ex))
                total_failed = total_failed + 1
        return items, item_batch, total_failed

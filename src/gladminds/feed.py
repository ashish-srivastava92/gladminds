import csv
from datetime import datetime, timedelta
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group
import logging
import os
import time

from gladminds import audit, message_template as templates
from gladminds import utils
from gladminds.models import common
from gladminds.aftersell.models import common as aftersell_common
from gladminds.audit import feed_log
from django.db.models import signals
from gladminds.utils import get_task_queue

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


class BaseFeed(object):

    def __init__(self, data_source=None, feed_remark=None):
        self.data_source = data_source
        self.feed_remark = feed_remark

    def import_data(self):
        pass

    def registerNewUser(self, user, group=None, username=None, first_name='', last_name='',
                          email=''):
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
            return new_user
        else:
            logger.info('{0} id is not provided.'.format(user))
            raise Exception('{0} id is not provided.'.format(user))    


class BrandProductTypeFeed(BaseFeed):

    def import_data(self):
        for brand in self.data_source:
            try:
                brand_data = common.BrandData.objects.get(
                    brand_id=brand['brand_id'])
            except ObjectDoesNotExist as odne:
                logger.info(
                    "[Exception: BrandProductTypeFeed_brand_data]: {0}"
                    .format(odne))
                brand_data = common.BrandData(
                    brand_id=brand['brand_id'], brand_name=brand['brand_name'])
                brand_data.save()

            try:
                product_type = common.ProductTypeData(brand_id=brand_data, product_name=brand[
                                                      'product_name'], product_type=brand['product_type'])
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
                dealer_data = aftersell_common.RegisteredDealer.objects.get(
                    dealer_id=dealer['dealer_id'])
            except ObjectDoesNotExist as odne:
                logger.debug(
                    "[Exception: DealerAndServiceAdvisorFeed_dealer_data]: {0}"
                    .format(odne))
                dealer_data = aftersell_common.RegisteredDealer(
                    dealer_id=dealer['dealer_id'], address=dealer['address'])
                dealer_data.save()
                self.registerNewUser('dealer', username=dealer['dealer_id'])

            try:
                mobile_number_active = self.check_mobile_active(dealer, dealer_data)
                service_advisor = aftersell_common.ServiceAdvisor.objects.filter(service_advisor_id=dealer['service_advisor_id'])
                if not mobile_number_active:
                    if len(service_advisor) > 0:
                        if dealer['phone_number'] != service_advisor[0].phone_number:
                            service_advisor[0].phone_number = dealer['phone_number']
                            service_advisor[0].save()
                            logger.info("[Info: DealerAndServiceAdvisorFeed_sa]: Updated phone number for {0}".format(dealer['service_advisor_id']))
                        service_advisor = service_advisor[0]
                    else:
                        service_advisor = aftersell_common.ServiceAdvisor(service_advisor_id=dealer['service_advisor_id'], 
                                                            name=dealer['name'], phone_number=dealer['phone_number'])
                        service_advisor.save()
                        self.registerNewUser('SA', username=dealer['service_advisor_id'])
                elif dealer['status']=='N':
                    service_advisor = service_advisor[0]
                else:
                    raise
            except Exception as ex:
                total_failed += 1
                logger.error(
                        "[Exception: DealerAndServiceAdvisorFeed_sa]: {0}".format(ex))
                continue

            try:
                mobile_number_active = self.check_mobile_active(dealer, dealer_data)
                service_advisor_dealer = aftersell_common.ServiceAdvisorDealerRelationship.objects.filter(service_advisor_id=service_advisor, dealer_id=dealer_data)
                if dealer['status']=='Y' and mobile_number_active:
                    raise
                elif len(service_advisor_dealer) == 0:
                    sa_dealer_rel = aftersell_common.ServiceAdvisorDealerRelationship(dealer_id=dealer_data, service_advisor_id=service_advisor, status=dealer['status'])
                    sa_dealer_rel.save()
                else:
                    service_advisor_dealer[
                        0].status = unicode(dealer['status'])
                    service_advisor_dealer[0].save()
            except Exception as ex:
                ex = "[Exception: Service Advisor and dealer relation is not created]: {0}"\
                    .format(ex)
                self.feed_remark.fail_remarks(ex)
                logger.error(ex)
                continue

        return self.feed_remark

    def update_other_dealer_sa_relationship(self, service_advisor, status):
        if status == 'Y':
            aftersell_common.ServiceAdvisorDealerRelationship.objects\
                .filter(service_advisor_id=service_advisor).update(status='N')

    def check_mobile_active(self, dealer, dealer_data):
        list_mobile = aftersell_common.ServiceAdvisorDealerRelationship.objects.filter(service_advisor_id__phone_number=dealer['phone_number'], status='Y')
        list_active_mobile = list_mobile.exclude(dealer_id=dealer_data, service_advisor_id__service_advisor_id=dealer['service_advisor_id'], )
        if list_active_mobile:
            return True
        return False

class ProductDispatchFeed(BaseFeed):

    def import_data(self):
        for product in self.data_source:
            try:
                product_data = common.ProductData.objects.get(
                    vin=product['vin'])
            except ObjectDoesNotExist as odne:
                logger.info(
                    '[Info: ProductDispatchFeed_product_data]: {0}'.format(odne))
                try:
                    try:
                        dealer_data = aftersell_common.RegisteredDealer.objects.get(
                            dealer_id=product['dealer_id'])
                    except Exception as ex:
                        dealer_data = aftersell_common.RegisteredDealer(
                            dealer_id=product['dealer_id'])
                        dealer_data.save()
                        self.registerNewUser('dealer', username=product['dealer_id'])
                    self.get_or_create_product_type(
                        product_type=product['product_type'])
                    producttype_data = common.ProductTypeData.objects.get(
                        product_type=product['product_type'])
                    invoice_date = product['invoice_date']
                    product_data = common.ProductData(
                        vin=product['vin'], product_type=producttype_data, invoice_date=invoice_date, dealer_id=dealer_data)
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
                valid_coupon = common.CouponData.objects.filter(unique_service_coupon=product['unique_service_coupon'])
                service_type_exists = common.CouponData.objects.filter(vin__vin=product['vin'], service_type=str(product['service_type']))
                if service_type_exists and not valid_coupon:
                    logger.error('VIN already has coupon of this service type {0} VIN - {1}'.format(product['vin'], product['unique_service_coupon']))
                    raise ValueError()
                elif not valid_coupon:
                    coupon_data = common.CouponData(unique_service_coupon=product['unique_service_coupon'],
                            vin=product_data, valid_days=product['valid_days'],
                            valid_kms=product['valid_kms'], service_type=product['service_type'],
                            status=product['coupon_status'])
                    coupon_data.save()
                    logger.info('[Successful: ProductDispatchFeed_product_data_save]:VIN - {0} UCN - {1}'.format(product['vin'], product['unique_service_coupon']))
                    
                elif valid_coupon[0].vin.vin == product['vin'] and str(valid_coupon[0].service_type) == str(product['service_type']):
                    logger.info('UCN is already saved in database. VIN - {0} UCN - {1}'.format(product['vin'], product['unique_service_coupon']))
                    continue
                else:
                    logger.error('Coupon Already registered for a VIN! VIN {0}  - UCN {1}'.format(product['vin'], product['unique_service_coupon']))
                    raise ValueError()
            except Exception as ex:   
                ex = '''Coupon: {2} Save error! {0}
                         VIN - {1}'''.format(ex, product['vin'], product['unique_service_coupon'])
                self.feed_remark.fail_remarks(ex)
                logger.error(ex)
                continue

        return self.feed_remark

    def get_or_create_product_type(self, product_type=None):
        brand_list = [{
            'brand_id': 'bajaj',
            'brand_name': 'bajaj',
            'product_type': product_type,
            'product_name': product_type,
        }]
        obj_brand = BrandProductTypeFeed(data_source=brand_list)
        obj_brand.import_data()


class ProductPurchaseFeed(BaseFeed):

    def update_customer_number(self, product_data, phone_number):
        try:
            if not product_data.customer_phone_number:
                return False
            else:
                customer_ph_num = product_data.customer_phone_number.phone_number
            if product_data.sap_customer_id and not customer_ph_num == phone_number:
                try:
                    customer_data = common.GladMindUsers.objects.get(
                        phone_number=customer_ph_num)
                    customer_data.phone_number = phone_number
                    customer_data.save()
                    product_data.customer_phone_number = customer_data
                    post_save.disconnect(
                        update_coupon_data, sender=common.ProductData)
                    product_data.save()
                    post_save.connect(
                        update_coupon_data, sender=common.ProductData)
                except Exception as ex:
                    logger.info(
                        "Expection: New Number of customer is not updated %s" % ex)
                return True
        except Exception as ex:
            logger.info('''[Exception: New Customer Added]: {0} Phone {1}'''
                        .format(ex, phone_number))

            return False

    def import_data(self):

        for product in self.data_source:
            try:
                product_data = common.ProductData.objects.get(
                    vin=product['vin'])

                if self.update_customer_number(product_data, product['customer_phone_number']):
                    logger.info("Update Customer Number")
                    continue
                try:
                    customer_data = common.GladMindUsers.objects.get(
                        phone_number=product['customer_phone_number'])
                except ObjectDoesNotExist as odne:
                    logger.info(
                        '[Exception: ProductPurchaseFeed_customer_data]: {0}'.format(odne))
                    # Register this customer
                    gladmind_customer_id = utils.generate_unique_customer_id()
                    user=self.registerNewUser('customer', username=gladmind_customer_id)
                    customer_data = common.GladMindUsers(user=user, gladmind_customer_id=gladmind_customer_id, phone_number=product[
                                                         'customer_phone_number'], registration_date=datetime.now(), customer_name=product['customer_name'])
                    customer_data.save()

                if not product_data.sap_customer_id  or product_data.sap_customer_id.find('T') == 0:
                    product_purchase_date = product['product_purchase_date']
                    product_data.sap_customer_id = product['sap_customer_id']
                    product_data.customer_phone_number = customer_data
                    product_data.product_purchase_date = product_purchase_date
                    product_data.engine = product["engine"]
                    product_data.save()
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
                coupon_data = common.CouponData.objects.filter(vin__vin=redeem['vin'], unique_service_coupon=redeem['unique_service_coupon']).update(
                    closed_date=closed_date, actual_service_date=actual_service_date, actual_kms=redeem['actual_kms'], status=2)
            except Exception as ex:
                continue


class CouponRedeemFeedToSAP(BaseFeed):

    def export_data(self, start_date=None, end_date=None):
        results = common.CouponData.objects.filter(closed_date__range=(
            start_date, end_date), status=2).select_related('vin', 'customer_phone_number__phone_number')
        items = []
        total_failed = 0
        item_batch = {
            'TIMESTAMP': datetime.now().strftime("%Y-%m-%dT%H:%M:%S")}
        for redeem in results:
            try:
                item = {
                        "CHASSIS": redeem.vin.vin,
                        "GCP_KMS": redeem.actual_kms,
                        "GCP_KUNNR": redeem.vin.dealer_id.dealer_id,
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
        asc_form_obj = aftersell_common.ASCSaveForm.objects\
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


def update_coupon_data(sender, **kwargs):
    from gladminds.sqs_tasks import send_on_product_purchase
    instance = kwargs['instance']
    logger.info("triggered update_coupon_data")
    if instance.customer_phone_number:
        product_purchase_date = instance.product_purchase_date
        vin = instance.vin
        coupon_data = common.CouponData.objects.filter(vin=instance)
        for coupon in coupon_data:
            mark_expired_on = product_purchase_date + \
                timedelta(days=int(coupon.valid_days))
            coupon_object = common.CouponData.objects.get(
                vin=instance, unique_service_coupon=coupon.unique_service_coupon)
            coupon_object.mark_expired_on = mark_expired_on
            coupon_object.extended_date = mark_expired_on
            coupon_object.save()

        try:
            customer_data = common.GladMindUsers.objects.get(
                phone_number=instance.customer_phone_number)
            if instance.sap_customer_id.find('T') == 0:
                message = templates.get_template('SEND_TEMPORARY_CUSTOMER_ID').format(
                    customer_name=customer_data.customer_name, sap_customer_id=instance.sap_customer_id)
            else:
                message = templates.get_template('SEND_CUSTOMER_ON_PRODUCT_PURCHASE').format(
                    customer_name=customer_data.customer_name, sap_customer_id=instance.sap_customer_id)
            if settings.ENABLE_AMAZON_SQS:
                task_queue = get_task_queue()
                task_queue.add("send_on_product_purchase", {"phone_number": 
                                instance.customer_phone_number.phone_number, "message":message})
            else:
                send_on_product_purchase.delay(
                phone_number=instance.customer_phone_number.phone_number, message=message)

            audit.audit_log(
                reciever=instance.customer_phone_number, action='SEND TO QUEUE', message=message)
        except Exception as ex:
            logger.info("[Exception]: Signal-In Update Coupon Data %s" % ex)

post_save.connect(update_coupon_data, sender=common.ProductData)

class ASCFeed(BaseFeed):
    def import_data(self):
        for dealer in self.data_source:
            try:
                dealer_data = aftersell_common.RegisteredDealer.objects.get(
                    dealer_id=dealer['dealer_id'])
            except ObjectDoesNotExist as ex:
                logger.debug(
                    "[Exception: ASCFeed_dealer_data]: {0}"
                    .format(ex))
                dealer_data = aftersell_common.RegisteredDealer(
                    dealer_id=dealer['dealer_id'], address=dealer['address'])
                dealer_data.save()
                self.registerNewUser('dealer', username=dealer['dealer_id'])
            try:
                asc_data = aftersell_common.RegisteredASC(
                    asc_id=dealer['asc_id'], dealer_id=dealer_data, asc_name=dealer['name'],
                    phone_number=dealer['phone_number'],address=dealer['address'],
                    email_id=dealer['email'], registration_date=datetime.now())
                user_obj = self.registerNewUser('ASC', username=dealer['asc_id'])
                asc_data.user = user_obj
                asc_data.save()
            except Exception as ex:
                ex = "[Exception: ASCFeed_dealer_data]: {0}".format(ex)
                logger.error(ex)
                self.feed_remark.fail_remarks(ex)
        return self.feed_remark

class CustomerRegistationFeedToSAP(BaseFeed):

    def export_data(self, start_date=None, end_date=None):
#        results = common.CustomerTempRegistration.objects.filter(sent_to_sap=False).select_related('product_data')
        results = [{
                    "CHASSIS": "MD2A11CZ0ECK08915",
                    "KUNNR": "10222",
                    "CUSTOMER_ID" : "T432474",
                    "ENGINE" : "DHZCEK89665",
                    "VEH_SL_DT": "2014-07-20",
                    "CUSTOMER_NAME": "BHARAT LALWANI",
                    "CUST_MOBILE": "+919999999999",
                    
                },
                {
                    "CHASSIS": "MD2A11CZ0ECK10017",
                    "KUNNR": "10491",
                    "CUSTOMER_ID" : "T432475",
                    "ENGINE" : "DHZCEK90632",
                    "VEH_SL_DT": "2014-07-20",
                    "CUSTOMER_NAME": "RAHUL KUMAR",
                    "CUST_MOBILE": "+919886032650",
                    
                },
                {
                    "CHASSIS": "MD2A11CZ0ECK10020",
                    "KUNNR": "10745",
                    "CUSTOMER_ID" : "T432476",
                    "ENGINE" : "DHZCEK91061",
                    "VEH_SL_DT": "2014-07-20",
                    "CUSTOMER_NAME": "BHARAT KUMAR",
                    "CUST_MOBILE": "+910000000000",
                    
                },
                {
                    "CHASSIS": "MD2A11CZ0ECK10129",
                    "KUNNR": "10222",
                    "CUSTOMER_ID" : "T432477",
                    "ENGINE" : "DHZCEK91165",
                    "VEH_SL_DT": "2014-07-20",
                    "CUSTOMER_NAME": "BHARAT LALWANI",
                    "CUST_MOBILE": "+919999999990",
                    
                },
                {
                    "CHASSIS": "MD2A11CZ0ECK10230",
                    "KUNNR": "10222",
                    "CUSTOMER_ID" : "T432478",
                    "ENGINE" : "DHZCEK91251",
                    "VEH_SL_DT": "2014-07-20",
                    "CUSTOMER_NAME": "BHARAT LALWANI",
                    "CUST_MOBILE": "+919999999991",
                    
                },
                {
                    "CHASSIS": "MD2A11CZ0ECK10308",
                    "KUNNR": "10222",
                    "CUSTOMER_ID" : "T432479",
                    "ENGINE" : "DHZCEK91327",
                    "VEH_SL_DT": "2014-07-20",
                    "CUSTOMER_NAME": "BHARAT LALWANI",
                    "CUST_MOBILE": "+919999999992",
                    
                },
                {
                    "CHASSIS": "MD2A11CZ0ECK10387",
                    "KUNNR": "10222",
                    "CUSTOMER_ID" : "T432480",
                    "ENGINE" : "DHZCEK91440",
                    "VEH_SL_DT": "2014-07-20",
                    "CUSTOMER_NAME": "BHARAT LALWANI",
                    "CUST_MOBILE": "+919999999993",
                    
                },
                {
                    "CHASSIS": "MD2A11CZ0ECK10423",
                    "KUNNR": "10222",
                    "CUSTOMER_ID" : "T432481",
                    "ENGINE" : "DHZCEK91477",
                    "VEH_SL_DT": "2014-07-20",
                    "CUSTOMER_NAME": "BHARAT LALWANI",
                    "CUST_MOBILE": "+919999999994",
                    
                },
                {
                    "CHASSIS": "MD2A11CZ0ECK10664",
                    "KUNNR": "10222",
                    "CUSTOMER_ID" : "T432482",
                    "ENGINE" : "DHZCEK91575",
                    "VEH_SL_DT": "2014-07-20",
                    "CUSTOMER_NAME": "BHARAT LALWANI",
                    "CUST_MOBILE": "+919999999995",
                    
                },
                {
                    "CHASSIS": "MD2A11CZ0ECK10731",
                    "KUNNR": "10222",
                    "CUSTOMER_ID" : "T432483",
                    "ENGINE" : "DHZCEK91715",
                    "VEH_SL_DT": "2014-07-20",
                    "CUSTOMER_NAME": "BHARAT LALWANI",
                    "CUST_MOBILE": "+919999999996",
                    
                },
                {
                    "CHASSIS": "MD2A11CZ0ECK10888",
                    "KUNNR": "10222",
                    "CUSTOMER_ID" : "T432484",
                    "ENGINE" : "DHZCEK91847",
                    "VEH_SL_DT": "2014-07-20",
                    "CUSTOMER_NAME": "BHARAT LALWANI",
                    "CUST_MOBILE": "+919999999997",
                    
                },
                {
                    "CHASSIS": "MD2A11CZ0ECK10891",
                    "KUNNR": "10222",
                    "CUSTOMER_ID" : "T432485",
                    "ENGINE" : "DHZCEK91852",
                    "VEH_SL_DT": "2014-07-20",
                    "CUSTOMER_NAME": "BHARAT LALWANI",
                    "CUST_MOBILE": "+919999999998",
                    
                },
                {
                    "CHASSIS": "MD2A11CZ0ECK10938",
                    "KUNNR": "10222",
                    "CUSTOMER_ID" : "T432486",
                    "ENGINE" : "DHZCEK91909",
                    "VEH_SL_DT": "2014-07-20",
                    "CUSTOMER_NAME": "BHARAT LALWANI",
                    "CUST_MOBILE": "+919999999909",
                    
                },
                {
                    "CHASSIS": "MD2A11CZ0ECK10955",
                    "KUNNR": "10222",
                    "CUSTOMER_ID" : "T432487",
                    "ENGINE" : "DHZCEK91930",
                    "VEH_SL_DT": "2014-07-20",
                    "CUSTOMER_NAME": "BHARAT LALWANI",
                    "CUST_MOBILE": "+919999999919",
                    
                },
                {
                    "CHASSIS": "MD2A11CZ0ECK10969",
                    "KUNNR": "10222",
                    "CUSTOMER_ID" : "T432488",
                    "ENGINE" : "DHZCEK91943",
                    "VEH_SL_DT": "2014-07-20",
                    "CUSTOMER_NAME": "BHARAT LALWANI",
                    "CUST_MOBILE": "+919999999929",
                    
                },
                {
                    "CHASSIS": "MD2A11CZ0ECK10972",
                    "KUNNR": "10222",
                    "CUSTOMER_ID" : "T432489",
                    "ENGINE" : "DHZCEK91944",
                    "VEH_SL_DT": "2014-07-20",
                    "CUSTOMER_NAME": "BHARAT LALWANI",
                    "CUST_MOBILE": "+919999999939",
                    
                },
                {
                    "CHASSIS": "MD2A11CZ0ECK10986",
                    "KUNNR": "10222",
                    "CUSTOMER_ID" : "T432490",
                    "ENGINE" : "DHZCEK91958",
                    "VEH_SL_DT": "2014-07-20",
                    "CUSTOMER_NAME": "BHARAT LALWANI",
                    "CUST_MOBILE": "+919999999949",
                    
                },
                {
                    "CHASSIS": "MD2A11CZ0ECK11006",
                    "KUNNR": "10222",
                    "CUSTOMER_ID" : "T432491",
                    "ENGINE" : "DHZCEK91982",
                    "VEH_SL_DT": "2014-07-20",
                    "CUSTOMER_NAME": "BHARAT LALWANI",
                    "CUST_MOBILE": "+919999999959",
                    
                },
                {
                    "CHASSIS": "MD2A11CZ0ECK11023",
                    "KUNNR": "10222",
                    "CUSTOMER_ID" : "T432492",
                    "ENGINE" : "DHZCEK92073",
                    "VEH_SL_DT": "2014-07-20",
                    "CUSTOMER_NAME": "BHARAT LALWANI",
                    "CUST_MOBILE": "+919999999969",
                    
                }]
        items = []
        total_failed = 0
        item_batch = {
            'TIME_STAMP': datetime.now().strftime("%Y%m%d%H%M%S")}
        for redeem in results:
            try:
                item = redeem
                items.append(item)
            except Exception as ex:
                logger.error("error on customer info from db %s" % str(ex))
                total_failed = total_failed + 1
        return items, item_batch, total_failed

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

    def registerNewDealer(self, username=None, first_name='', last_name='',
                          email=''):
        logger.info('New Dealer Registration with id - ' + username)
        if username:
            dealer = User(
                username=username, first_name=first_name, last_name=last_name, email=email)
            password = username + settings.PASSWORD_POSTFIX
            dealer.set_password(password)
            dealer.save()
            if not Group.objects.all():
                gr_obj = Group.objects.create(name='dealers')
                gr_obj.save()

            dealer_group = Group.objects.get(name='dealers')
            dealer.groups.add(dealer_group)
            logger.info('Dealer {0} registered successfully'.format(username))
        else:
            logger.info('Dealer id is not provided.')
            raise Exception('Dealer id is not provided.')


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
                self.registerNewDealer(username=dealer['dealer_id'])

            try:
                service_advisor = aftersell_common.ServiceAdvisor.objects.filter(
                    service_advisor_id=dealer['service_advisor_id'])
                if len(service_advisor) > 0:
                    service_advisor = service_advisor[0]
                else:
                    service_advisor = aftersell_common.ServiceAdvisor(
                        service_advisor_id=dealer['service_advisor_id'],
                        name=dealer['name'],
                        phone_number=dealer['phone_number'])
                    service_advisor.save()
            except Exception as ex:
                ex = "[Exception: DealerAndServiceAdvisorFeed_sa]: {0}"\
                    .format(ex)
                self.feed_remark.fail_remarks(ex)
                logger.error(ex)
                continue

            try:
                service_advisor_dealer = aftersell_common\
                    .ServiceAdvisorDealerRelationship.objects.filter(
                        service_advisor_id=service_advisor,
                        dealer_id=dealer_data)
                self.update_other_dealer_sa_relationship(service_advisor,
                                                         dealer['status'])
                if len(service_advisor_dealer) == 0:
                    sa_dealer_rel = aftersell_common.ServiceAdvisorDealerRelationship(
                        dealer_id=dealer_data,
                        service_advisor_id=service_advisor,
                        status=dealer['status'])
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
                        self.registerNewDealer(username=product['dealer_id'])
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
                if not valid_coupon:
                    coupon_data = common.CouponData(unique_service_coupon=product['unique_service_coupon'],
                            vin=product_data, valid_days=product['valid_days'],
                            valid_kms=product['valid_kms'], service_type=product['service_type'],
                            status=product['coupon_status'])
                    coupon_data.save()
                    logger.info('[Successful: ProductDispatchFeed_product_data_save]:VIN - {0} UCN - {1}'.format(product['vin'], product['unique_service_coupon']))
                    
                elif valid_coupon[0].vin.vin == product['vin'] and str(valid_coupon[0].service_type) == str(product['service_type']):
                    logger.info('[Successful: ProductDispatchFeed_product_data_save]:VIN - {0} UCN - {1}'.format(product['vin'], product['unique_service_coupon']))
                    continue
                else:
                    logger.error('Coupon {2} Already registered for another VIN! {0} VIN - {1}'.format(ex, product['vin'], product['unique_service_coupon']))
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
                    customer_data = common.GladMindUsers(gladmind_customer_id=gladmind_customer_id, phone_number=product[
                                                         'customer_phone_number'], registration_date=datetime.now(), customer_name=product['customer_name'])
                    customer_data.save()

                if not product_data.sap_customer_id:
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
                self.registerNewDealer(username=dealer['dealer_id'])
            try:
                asc_data = aftersell_common.RegisteredASC.objects.get(
                    asc_id=dealer['asc_id'])
            except ObjectDoesNotExist as ex:
                logger.debug(
                    "[Exception: ASCFeed_dealer_data]: {0}"
                    .format(ex))
                asc_data = aftersell_common.RegisteredASC(
                    asc_id=dealer['asc_id'], dealer_id=dealer_data, asc_name=dealer['name'],
                    phone_number=dealer['phone_number'],address=dealer['address'],
                    email_id=dealer['email'], registration_date=datetime.now())
                asc_data.save()
        return self.feed_remark

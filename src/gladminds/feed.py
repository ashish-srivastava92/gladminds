import csv
from datetime import datetime, timedelta
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import post_save
import logging
import os
import time

from gladminds import audit, message_template as templates
from gladminds import utils
from gladminds.models import common
from gladminds import exportfeed
from gladminds.audit import feed_log


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

    def import_to_db(self, feed_type=None, data_source=[]):
        if feed_type == 'brand':
            brand_obj = BrandProductTypeFeed(data_source=data_source)
            return brand_obj.import_data()
        elif feed_type == 'dealer':
            dealer_obj = DealerAndServiceAdvisorFeed(data_source=data_source)
            return dealer_obj.import_data()
        elif feed_type == 'dispatch':
            dispatch_obj = ProductDispatchFeed(data_source=data_source)
            return dispatch_obj.import_data()
        elif feed_type == 'purchase':
            purchase_obj = ProductPurchaseFeed(data_source=data_source)
            return purchase_obj.import_data()


class BaseFeed(object):

    def __init__(self, data_source=None):
        self.data_source = data_source

    def import_data(self):
        pass


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
                dealer_data = common.RegisteredDealer.objects.get(
                    dealer_id=dealer['dealer_id'])
            except ObjectDoesNotExist as odne:
                logger.info(
                    "[Exception: DealerAndServiceAdvisorFeed_dealer_data]: {0}".format(odne))
                dealer_data = common.RegisteredDealer(
                    dealer_id=dealer['dealer_id'], address=dealer['address'])
                dealer_data.save()

            try:
                service_advisor = common.ServiceAdvisor(dealer_id=dealer_data, service_advisor_id=dealer[
                                                        'service_advisor_id'], name=dealer['name'], phone_number=dealer['phone_number'], status=dealer['status'])
                service_advisor.save()
            except Exception as ex:
                total_failed += 1
                logger.info(
                    "[Exception: DealerAndServiceAdvisorFeed_sa]: {0}".format(ex))
                continue
        feed_log(feed_type='Dealer Feed', total_data_count=len(self.data_source),
                 failed_data_count=total_failed, success_data_count=len(
                     self.data_source) - total_failed,
                 action='Recieved', status=True)
        return get_feed_status(len(self.data_source), total_failed)


class ProductDispatchFeed(BaseFeed):

    def import_data(self):
        total_failed = 0
        for product in self.data_source:
            try:
                product_data = common.ProductData.objects.get(
                    vin=product['vin'])
            except ObjectDoesNotExist as odne:
                logger.info(
                    '[Exception: ProductDispatchFeed_product_data]: {0}'.format(odne))
                try:
                    try:
                        dealer_data = common.RegisteredDealer.objects.get(
                            dealer_id=product['dealer_id'])
                    except Exception as ex:
                        dealer_data = common.RegisteredDealer(dealer_id=product['dealer_id'])
                        dealer_data.save()
                    self.get_or_create_product_type(
                        product_type=product['product_type'])
                    producttype_data = common.ProductTypeData.objects.get(
                        product_type=product['product_type'])
                    invoice_date = product['invoice_date']
                    product_data = common.ProductData(
                        vin=product['vin'], product_type=producttype_data, invoice_date=invoice_date, dealer_id=dealer_data)
                    product_data.save()
                except Exception as ex:
                    total_failed += 1
                    logger.info(
                        '[Exception: ProductDispatchFeed_product_data_save]: {0}'.format(ex))
                    continue

            try:
                status = 1
                coupon_data = common.CouponData(unique_service_coupon=product['unique_service_coupon'],
                                                vin=product_data, valid_days=product['valid_days'], valid_kms=product['valid_kms'], service_type=product['service_type'], status=status)
                coupon_data.save()
            except Exception as ex:
                total_failed += 1
                continue

        feed_log(feed_type='Dispatch Feed', total_data_count=len(self.data_source),
                 failed_data_count=total_failed, success_data_count=len(
                     self.data_source) - total_failed,
                 action='Recieved', status=True)
        return get_feed_status(len(self.data_source), total_failed)

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

    def import_data(self):
        total_failed = 0
        for product in self.data_source:
            try:
                product_data = common.ProductData.objects.get(
                    vin=product['vin'])
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
                    product_data.save()
                self.update_engine_number(product)
            except Exception as ex:
                total_failed += 1
                logger.info(
                    '[Exception: ProductPurchaseFeed_product_data]: {0}'.format(ex))
                continue

        feed_log(feed_type='Purchase Feed', total_data_count=len(self.data_source),
                 failed_data_count=total_failed, success_data_count=len(
                     self.data_source) - total_failed,
                 action='Recieved', status=True)
        return get_feed_status(len(self.data_source), total_failed)

    def update_engine_number(self, product):
        try:
            product_data_obj = common.ProductData.objects.filter(vin=product["vin"])[0]
            product_data_obj.engine = product["engine"]
            product_data_obj.save()
        except ObjectDoesNotExist as odne:
                    print "on product purchase", odne
                    logger.info(
                        '[Exception: ProductPurchaseFeed_customer_data]: {0} Engine is not updated'.format(odne))


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
        item_batch = {
            'TIMESTAMP': datetime.now().strftime("%Y-%m-%dT%H:%M:%S")}
        for redeem in results:
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
        return items, item_batch


def get_feed_status(total_feeds, failed_feeds):
    return [{
            "Passed": total_feeds - failed_feeds},
            {"Failed": failed_feeds}
           ]


def update_coupon_data(sender, **kwargs):
    from gladminds.tasks import send_on_product_purchase
    instance = kwargs['instance']
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
            coupon_object.save()

        try:
            customer_data = common.GladMindUsers.objects.get(
                phone_number=instance.customer_phone_number)
            message = templates.get_template('SEND_CUSTOMER_ON_PRODUCT_PURCHASE').format(
                customer_name=customer_data.customer_name, sap_customer_id=instance.sap_customer_id)
            send_on_product_purchase.delay(
                phone_number=instance.customer_phone_number, message=message)
            audit.audit_log(
                reciever=instance.customer_phone_number, action='SEND TO QUEUE', message=message)
        except Exception as ex:
            logger.info("[Exception]: Signal-In Update Coupon Data")

post_save.connect(update_coupon_data, sender=common.ProductData)
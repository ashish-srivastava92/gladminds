from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import post_save
from django.conf import settings
from gladminds.models import common
from gladminds import utils
from datetime import datetime, timedelta
from gladminds import audit, message_template as templates
import os
import time
import csv
import logging
logger = logging.getLogger(__name__)


def load_feed():
    FEED_TYPE = settings.FEED_TYPE
    if FEED_TYPE is 'CSV':
        CSVFeed()
    elif FEED_TYPE is 'SAP':
        SAPFeed()

class CSVFeed(object):
    def __init__(self):
        file_path = settings.DATA_CSV_PATH
        brand_path = file_path+"/brand_data.csv"
        dealer_path = file_path+"/dealer_data.csv"
        product_path = file_path+"/product_data.csv"
        product_purchase_path = file_path+"/product_purchase.csv"
        coupon_redeem_path = file_path+"/coupon_redeem.csv"
        
        #Import data from CSV
        if os.path.isfile(brand_path):
            brand_feed = self.get_dict(brand_path)
            brand_data  = BrandProductTypeFeed(data_source = brand_feed)
            brand_data.import_data()
            self.rename(fullpath = brand_path)   
        
        if os.path.isfile(dealer_path):
            dealer_feed = self.get_dict(dealer_path)
            dealer_data = DealerAndServiceAdvisorFeed(data_source = dealer_feed)
            dealer_data.import_data()
            self.rename(fullpath = dealer_path)
        
        if os.path.isfile(product_path): 
            productcoupon_feed = self.get_dict(product_path)
            product_data = ProductDispatchFeed(data_source = productcoupon_feed)
            product_data.import_data()
            self.rename(fullpath = product_path)
        
        if os.path.isfile(product_purchase_path):
            productpurchase_feed = self.get_dict(product_purchase_path)
            product_purchase_data = ProductPurchaseFeed(data_source = productpurchase_feed)
            product_purchase_data.import_data()
            self.rename(fullpath = product_purchase_path)
        
        if os.path.isfile(coupon_redeem_path):
            coupon_redeem_feed = self.get_dict(coupon_redeem_path)
            coupon_redeem_data = ProductServiceFeed(data_source = coupon_redeem_feed)
            coupon_redeem_data.import_data()
            self.rename(fullpath = coupon_redeem_path)
    
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
            os.rename(fullpath, fullpath+'-'+timestamp_str)
        except OSError as oe:
            logger.exception("[Excpetion]: {0}".format(oe))
            
class SAPFeed(object):
    pass

class BaseFeed(object):
    def __init__(self, data_source = None):
        self.data_source = data_source
    
    def import_data(self):
        pass
    
class BrandProductTypeFeed(BaseFeed):
    def import_data(self):
        for brand in self.data_source:
            try:
                brand_data  =common.BrandData.objects.get(brand_id = brand['brand_id'])
            except ObjectDoesNotExist as odne:
                brand_data = common.BrandData(brand_id=brand['brand_id'], brand_name = brand['brand_name'])
                brand_data.save()
            
            try:
                product_type = common.ProductTypeData(brand_id = brand_data, product_name = brand['product_name'], product_type = brand['product_type'])
                product_type.save()
            except Exception as ex:
                continue

class DealerAndServiceAdvisorFeed(BaseFeed):
    def import_data(self):
        for dealer in self.data_source:
            try:
                dealer_data = common.RegisteredDealer.objects.get(dealer_id = dealer['dealer_id'])
            except ObjectDoesNotExist as odne:
                dealer_data = common.RegisteredDealer(dealer_id = dealer['dealer_id'], address = dealer['address'])
                dealer_data.save()
            
            try:
                service_advisor = common.ServiceAdvisor(dealer_id = dealer_data, service_advisor_id = dealer['service_advisor_id'], name = dealer['name'], phone_number = dealer['phone_number'])
                service_advisor.save()
            except Exception as ex:
                continue

class ProductDispatchFeed(BaseFeed):
    def import_data(self):
        for product in self.data_source:
            try:
                product_data = common.ProductData.objects.get(vin=product['vin'])
            except ObjectDoesNotExist as odne:
                try:
                    dealer_data = common.RegisteredDealer.objects.get(dealer_id = product['dealer_id'])
                    producttype_data = common.ProductTypeData.objects.get(product_type = product['product_type'])
                    invoice_date = datetime.strptime(product['invoice_date'],'%d-%m-%Y %H:%M:%S')
                    product_data = common.ProductData(vin = product['vin'], product_type = producttype_data, invoice_date = invoice_date, dealer_id = dealer_data)
                    product_data.save()
                except Exception as ex:
                    continue
        
            try:
                status = 1
                coupon_data = common.CouponData(unique_service_coupon = product['unique_service_coupon'], vin = product_data, valid_days = product['valid_days'], valid_kms = product['valid_kms'], service_type = product['service_type'], status = status)
                coupon_data.save()
            except Exception as ex:
                continue
            
class ProductPurchaseFeed(BaseFeed):
    def import_data(self):
        for product in self.data_source:
            try:
                product_data = common.ProductData.objects.get(vin=product['vin'])
                try:
                    customer_data = common.GladMindUsers.objects.get(phone_number = product['customer_phone_number'])
                except ObjectDoesNotExist as odne:
                    #Register this customer
                    gladmind_customer_id = utils.generate_unique_customer_id()
                    customer_data = common.GladMindUsers(gladmind_customer_id = gladmind_customer_id, phone_number = product['customer_phone_number'], registration_date = datetime.now(), customer_name = product['customer_name'])
                    customer_data.save()
                
                if not product_data.sap_customer_id:
                    product_purchase_date = datetime.strptime(product['product_purchase_date'],'%d-%m-%Y %H:%M:%S')
                    product_data.sap_customer_id = product['sap_customer_id']
                    product_data.customer_phone_number = customer_data
                    product_data.product_purchase_date = product_purchase_date
                    product_data.save()
            except Exception as ex:
                continue
            
class ProductServiceFeed(BaseFeed):
    def import_data(self):
        for redeem in self.data_source:
            try:
                coupon_data = common.CouponData.objects.filter(vin__vin = redeem['vin'], unique_service_coupon = redeem['unique_service_coupon']).update(closed_date = redeem['closed_date'], actual_service_date = redeem['actual_service_date'], actual_kms = redeem['actual_kms'], status = 2)
            except Exception as ex:
                continue

def update_coupon_data(sender, **kwargs):
    from gladminds.tasks import send_on_product_purchase
    instance = kwargs['instance']
    if instance.customer_phone_number:
        product_purchase_date = instance.product_purchase_date
        vin = instance.vin
        coupon_data = common.CouponData.objects.filter(vin = instance)
        for coupon in coupon_data:
            mark_expired_on = product_purchase_date + timedelta(days=int(coupon.valid_days))
            coupon_object = common.CouponData.objects.get(vin = instance, unique_service_coupon = coupon.unique_service_coupon)
            coupon_object.mark_expired_on=mark_expired_on
            coupon_object.save()
        
        try:
            customer_data = common.GladMindUsers.objects.get(phone_number = instance.customer_phone_number) 
            message = templates.get_template('SEND_CUSTOMER_ON_PRODUCT_PURCHASE').format(customer_name = customer_data.customer_name, sap_customer_id = instance.sap_customer_id)
            send_on_product_purchase.delay(phone_number=instance.customer_phone_number, message=message)
            audit.audit_log(reciever=instance.customer_phone_number, action='SEND TO QUEUE', message=message)
        except Exception as ex:
            print "[Exception]: Signal-In Update Coupon Data"  

post_save.connect(update_coupon_data, sender=common.ProductData)

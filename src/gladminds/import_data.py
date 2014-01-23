import csv
from django.conf import settings
from gladminds.models import common
from datetime import datetime

def import_data(*args, **kwargs):
    file_path = settings.DATA_CSV_PATH
    
    #Import data from CSV
    brand_product = csv.DictReader(open(file_path+"/brand_data.csv"))
    import_branddata(brand_source = brand_product)
    brand_product = csv.DictReader(open(file_path+"/brand_data.csv"))
    import_product_typedata(product_source = brand_product)
    
    dealer_sa = csv.DictReader(open(file_path+"/dealer_data.csv"))
    import_dealerdata(dealer_source = dealer_sa)
    dealer_sa = csv.DictReader(open(file_path+"/dealer_data.csv"))
    import_serviceadvisor_data(sa_source = dealer_sa)
    
    product_coupon = csv.DictReader(open(file_path+"/product_data.csv"))
    import_productdata(product_source = product_coupon)
    product_coupon = csv.DictReader(open(file_path+"/product_data.csv"))
    import_coupondata(coupon_source = product_coupon)

def import_branddata(brand_source):
    for brand in brand_source:
        try:
            brand = common.BrandData(brand_id=brand['brand_id'], brand_name = brand['brand_name'])
            brand.save()
        except Exception as ex:
            continue

def import_product_typedata(product_source):
    for product in product_source:
        try:
            brand_data  =common.BrandData.objects.get(brand_id = product['brand_id'])
            product_type = common.ProductTypeData(brand_id = brand_data, product_name = product['product_name'], product_type = product['product_type'])
            product_type.save()
        except Exception as ex:
            continue

def import_dealerdata(dealer_source):
    for dealer in dealer_source:
        try:
            dealer_data = common.RegisteredDealer(dealer_id = dealer['dealer_id'], address = dealer['address'])
            dealer_data.save()
        except Exception as ex:
            continue

def import_serviceadvisor_data(sa_source):
    for sa in sa_source:
        try:
            dealer_data = common.RegisteredDealer.objects.get(dealer_id = sa['dealer_id'])
            service_advisor = common.ServiceAdvisor(dealer_id = dealer_data, service_advisor_id = sa['service_advisor_id'], name = sa['name'], phone_number = sa['phone_number'])
            service_advisor.save()
        except Exception as ex:
            continue

def import_productdata(product_source):
    for product in product_source:
        try:
            dealer_data = common.RegisteredDealer.objects.get(dealer_id = product['dealer_id'])
            producttype_data = common.ProductTypeData.objects.get(product_type = product['product_type'])
            customer_phone_number = None if product['customer_phone_number'] is '' else common.GladMindUsers.objects.get(phone_number = product['customer_phone_number'])
            product_purchase_date = None if product['product_purchase_date'] is '' else datetime.strptime(product['product_purchase_date'],'%d-%m-%Y %H:%M:%S')
            invoice_date = datetime.strptime(product['invoice_date'],'%d-%m-%Y %H:%M:%S')
            product_data = common.ProductData(vin = product['vin'], customer_phone_number = customer_phone_number, product_type = producttype_data, sap_customer_id = product['sap_customer_id'], product_purchase_date = product_purchase_date, invoice_date = invoice_date, dealer_id = dealer_data)
            product_data.save()
        except Exception as ex:
            continue

def import_coupondata(coupon_source):
    for coupon in coupon_source:
        try:
            vin = common.ProductData.objects.get(vin=coupon['vin'])
            status = 1
            closed_date = None if coupon['closed_date'] is '' else datetime.strptime(coupon['closed_date'],'%d-%m-%Y %H:%M:%S')
            actual_service_date = None if coupon['actual_service_date'] is '' else coupon['actual_service_date']
            actual_kms = None if coupon['actual_kms'] is '' else coupon['actual_kms']
            actual_service_date = None if coupon['actual_service_date'] is '' else datetime.strptime(coupon['actual_service_date'],'%d-%m-%Y %H:%M:%S')
            mark_expired_on = None if vin.customer_phone_number is None else datetime.strptime(vin.product_purchase_date) + datetime.timedelta(days=int(coupon['valid_days']))
            sa_phone_number = None if coupon['sa_phone_number'] is '' else common.ServiceAdvisor.objects.get(phone_number = coupon['sa_phone_number'])
            coupon_data = common.CouponData(unique_service_coupon = coupon['unique_service_coupon'], vin = vin, valid_days = coupon['valid_days'], valid_kms = coupon['valid_kms'], service_type = coupon['service_type'], sa_phone_number = sa_phone_number, status = status, closed_date = closed_date, mark_expired_on = mark_expired_on, actual_service_date = actual_service_date, actual_kms = coupon['actual_kms'])
            coupon_data.save()
        except Exception as ex:
            continue
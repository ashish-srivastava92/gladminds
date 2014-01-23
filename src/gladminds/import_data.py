import csv
from gladminds import common

def import_data(*args, **kwargs):
    #Import data from CSV
    import_branddata()
    import_product_typedata()
    import_dealerdata()
    import_serviceadvisor_data()
    import_productdata()
    import_coupondata()

def import_branddata(*args, **kwargs):
    try:
        brand = common.BrandData(brand_id=brand_id, brand_name = brand_name)
        brand.save()
    except Exception as ex:
        pass

def import_product_typedata(*args, **kwargs):
    try:
        product_type = common.ProductTypeData(brand_id = brand_id, product_name = product_name, product_type = product_type)
        product_type.save()
    except Exception as ex:
        pass

def import_dealerdata(*args, **kwargs):
    try:
        dealer_data = common.DealerData(dealer_id = dealer_id, address = address)
        dealer_data.save()
    except Exception as ex:
        pass

def import_serviceadvisor_data(*args, **kwargs):
    try:
        service_advisor = common.ServiceAdvisor(dealer_id = dealer_id, service_advisor_id = service_advisor_id, name = name, phone_number = phone_number)
        service_advisor.save()
    except Exception as ex:
        pass

def import_productdata(*args, **kwargs):
    try:
        product_data = common.ProductData(vin = vin, customer_phone_number = customer_phone_number, product_type = product_type, sap_customer_id = sap_customer_id, product_purchase_date = product_purchase_date, invoice_date = invoice_date, dealer_id = dealer_id)
        product_data.save()
    except Exception as ex:
        pass

def import_coupondata(*args, **kwargs):
    try:
        coupon_data = common.CouponData(unique_service_coupon = unique_service_coupon, vin = vin, valid_days = valid_days, valid_kms = valid_kms, service_type = service_type, sa_phone_number = sa_phone_number, status = status, closed_date = closed_date, mark_expired_on = mark_expired_on, actual_service_date = actual_service_date, actual_kms = actual_kms)
        coupon_data.save()
    except Exception as ex:
        pass
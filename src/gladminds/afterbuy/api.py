from gladminds.models import common
from gladminds import utils
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse
from tastypie.http import HttpBadRequest

import json
import logging

logger = logging.getLogger("gladminds")

@csrf_exempt
def fnc_get_product_coupons(request):
    resp = {}
    vin = request.GET.get('vin')
    if not vin:
        return HttpBadRequest("Vin is required.")
    try:
        product_object = common.ProductData.objects.filter(vin = vin)[0]
        product_id = product_object.id
        product_coupons = common.CouponData.objects.filter(id=product_id).values()[0]
        resp = utils.get_dict_from_object(product_coupons)
    except Exception as ex:
        logger.info("[Exception fnc_get_product_coupons]:{0}".format(ex))
    return HttpResponse(json.dumps(resp))

@csrf_exempt
def fnc_get_product_purchase_information(request):
    resp = {}
    product_type_id = request.GET.get("product_type_id")
    if not product_type_id:
        return HttpBadRequest("product_type_id is required.")
    try:
        product_info = common.ProductTypeData.objects.filter(product_type_id = product_type_id).values()[0]
        if not product_info:
            return HttpBadRequest("This product does not exist.")
        else:
            resp = utils.get_dict_from_object(product_info)
    except Exception as ex:
        logger.info("[Exception fnc_get_product_purchase_information]:{0}".format(ex))
    return HttpResponse(json.dumps(resp))


@csrf_exempt
def fnc_get_product_information(request):
    resp = {}
    vin = request.GET.get('vin')
    if not vin:
        return HttpBadRequest("Vin is required.")
    try:
        product_info = common.ProductData.objects.filter(vin=vin).values()[0]
        if not product_info:
            return HttpBadRequest("This product does not exist.")
        else:
            resp = utils.get_dict_from_object(product_info)
    except Exception as ex:
        logger.info("[Exception fnc_get_product_information]:{0}".format(ex))
    return HttpResponse(json.dumps(resp))
    
    
@csrf_exempt
def fnc_get_product_warranty(request):
    resp = {}
    vin = request.GET.get('vin')
    if not vin:
        return HttpBadRequest("vin is required.")
    try:
        product_info = common.ProductData.objects.get(vin=vin)
        if not product_info:
            return HttpBadRequest("This product does not exist.")
        warranty_info = common.ProductWarrantyInfo.objects.get(product=product_info)
        resp['image_url'] = ''
        resp['issue_date'] = warranty_info.issue_date
        resp['expiry_date'] = warranty_info.expiry_date
        resp['warranty_brand_id'] = warranty_info.warranty_brand_id
        resp['warranty_brand_name'] = warranty_info.warranty_brand_name
        resp['policy_number'] = warranty_info.policy_number
        resp['premium'] = warranty_info.premium
        resp['contact_email'] = warranty_info.product.customer_phone_number.email_id
        resp['contact_phone'] = warranty_info.product.customer_phone_number.phone_number
    except Exception as ex:
        logger.info("[Exception fnc_get_product_warranty]:{0}".format(ex))
    return HttpResponse(json.dumps(resp))


@csrf_exempt
def fnc_get_product_insurance(request):
    resp = {}
    vin = request.GET.get('vin')
    if not vin:
        return HttpBadRequest("vin is required.")
    try:
        product_info = common.ProductData.objects.get(vin=vin)
        if not product_info:
            return HttpBadRequest("This product does not exist.")
        insurance_info = common.ProductInsuranceInfo.objects.get(product=product_info)
        resp['image_url'] = ''
        resp['issue_date'] = insurance_info.issue_date
        resp['expiry_date'] = insurance_info.expiry_date
        resp['insurance_brand_id'] = insurance_info.insurance_brand_id
        resp['insurance_brand_name'] = insurance_info.insurance_brand_name
        resp['policy_number'] = insurance_info.policy_number
        resp['premium'] = insurance_info.premium
        resp['contact_email'] = insurance_info.product.customer_phone_number.email_id
        resp['contact_phone'] = insurance_info.product.customer_phone_number.phone_number
    except Exception as ex:
        logger.info("[Exception fnc_get_product_insurance]:{0}".format(ex))
    return HttpResponse(json.dumps(resp))
        
    
    
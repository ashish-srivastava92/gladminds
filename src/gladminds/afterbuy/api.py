from gladminds.models import common
from gladminds import utils
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse
from tastypie.http import HttpBadRequest
from gladminds.utils import mobile_format

import json
import logging
from django.forms.models import model_to_dict

logger = logging.getLogger("gladminds")

@csrf_exempt
def get_product_coupons(request):
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
        logger.info("[Exception get_product_coupons]:{0}".format(ex))
    return HttpResponse(json.dumps(resp))

@csrf_exempt
def get_product_purchase_information(request):
    resp = {}
    vin = request.GET.get("vin")
    if not vin:
        return HttpBadRequest("vin is required.")
    try:
        product_info = common.ProductData.objects.filter(vin = vin).values()[0]
        if not product_info:
            return HttpBadRequest("This product does not exist.")
        else:
            resp = utils.get_dict_from_object(product_info)
    except Exception as ex:
        logger.info("[Exception get_product_purchase_information]:{0}".format(ex))
    return HttpResponse(json.dumps(resp))


@csrf_exempt
def get_user_product_information(request):
    resp = []
    mobile = request.GET.get('mobile')
    if not mobile:
        return HttpBadRequest("mobile is required.")
    try:
        phone_number= mobile_format(mobile)
        
        user_info = common.GladMindUsers.objects.get(phone_number=phone_number)
        product_info = common.ProductData.objects.filter(customer_phone_number=user_info)
        if not product_info:
            return HttpResponse("No product exist.")
        else:
            for i in map(model_to_dict, product_info):
                resp.append(utils.get_dict_from_object(i))
    except Exception as ex:
        logger.info("[Exception get_user_product_information]:{0}".format(ex))
    return HttpResponse(json.dumps(resp))
    
    
@csrf_exempt
def get_product_warranty(request):
    resp = {}
    vin = request.GET.get('vin')
    if not vin:
        return HttpBadRequest("vin is required.")
    try:
        product_info = common.ProductData.objects.get(vin=vin)
        warranty_info = common.ProductWarrantyInfo.objects.get(product=product_info)
        for field in ['image_url', 'issue_date', 'expiry_date', 'warranty_brand_id', 
                  'warranty_brand_name', 'policy_number', 'premium']:
            resp[field] = getattr(warranty_info, field)
        resp['warranty_email'] = warranty_info.product.product_type.warranty_email
        resp['warranty_phone'] = warranty_info.product.product_type.warranty_phone
    except Exception as ex:
        logger.info("[Exception get_product_warranty]:{0}".format(ex))
    return HttpResponse(json.dumps(resp))


@csrf_exempt
def get_product_insurance(request):
    resp = {}
    vin = request.GET.get('vin')
    if not vin:
        return HttpBadRequest("vin is required.")
    try:
        product_info = common.ProductData.objects.get(vin=vin)
        insurance_info = common.ProductInsuranceInfo.objects.get(product=product_info)
        for field in ['image_url', 'issue_date', 'expiry_date', 'insurance_brand_id', 
                  'insurance_brand_name', 'policy_number', 'premium', 'insurance_phone', 'insurance_email']:
            resp[field] = getattr(insurance_info, field)
    except Exception as ex:
        logger.info("[Exception get_product_insurance]:{0}".format(ex))
    return HttpResponse(json.dumps(resp))
        
    
    
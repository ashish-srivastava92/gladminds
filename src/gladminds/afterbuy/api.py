from gladminds.models import common
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse
from gladminds import utils

import json
import logging
from tastypie.http import HttpBadRequest

logger = logging.getLogger("gladminds")


@csrf_exempt
def fnc_get_product_coupons(request):
    resp = {}
    vin = request.POST.get('vin', None)
    if not vin:
        vin = "TestChasis_23_3";
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
    product_type_id = request.POST.get("product_type_id", None)
    if not product_type_id:
        product_type_id = "991735";
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
    vin = request.POST.get('vin', None)
    if not vin:
        vin = "TestChasis_23_3";
    try:
        product_info = common.ProductData.objects.filter(vin=vin).values()[0]
        if not product_info:
            return HttpBadRequest("This product does not exist.")
        else:
            resp = utils.get_dict_from_object(product_info)
    except Exception as ex:
        logger.info("[Exception fnc_get_product_information]:{0}".format(ex))
    return HttpResponse(json.dumps(resp))
    
    
    
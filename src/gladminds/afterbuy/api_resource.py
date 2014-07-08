import json
import logging
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse
from django.conf.urls import url
from tastypie.http import HttpBadRequest
from tastypie.resources import ModelResource
from tastypie.utils.urls import trailing_slash

from gladminds.models import common
from gladminds import utils
from gladminds.resource.authentication import AccessTokenAuthentication
from gladminds.afterbuy.models import common as afterbuy_common
from gladminds.utils import mobile_format


logger = logging.getLogger("gladminds")

class AfterBuyBaseResource(ModelResource):
    def determine_format(self, request):
        return 'application/json'

'''Contains all the apis for AfterBuy App'''
class AfterBuyResources(AfterBuyBaseResource):
    class Meta:
#         queryset = common.ProductData.objects.all()
        resource_name = 'afterbuy'
        authentication = AccessTokenAuthentication()
        
    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/user/save%s" % (self._meta.resource_name, trailing_slash()), self.wrap_view('save_user_details'), name="save_user_details"),
            url(r"^(?P<resource_name>%s)/product/coupons%s" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_product_coupons'), name="get_product_coupons"),
            url(r"^(?P<resource_name>%s)/product/purchase-info%s" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_product_purchase_information'), name="get_product_purchase_information"),
            url(r"^(?P<resource_name>%s)/product/warranty%s" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_product_warranty'), name="get_product_warranty"),
            url(r"^(?P<resource_name>%s)/product/insurance%s" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_product_insurance'), name="get_product_insurance"),
            url(r"^(?P<resource_name>%s)/product/info%s" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_user_product_information'), name="get_user_product_information"),
            url(r"^(?P<resource_name>%s)/notification/count%s" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_notification_count'), name="get_notification_count"),
            url(r"^(?P<resource_name>%s)/notification/list%s" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_notification_list'), name="get_notification_list"),
        ]

    def get_product_coupons(self, request, **kwargs):
        '''This API fetches all the coupons for a particular product
           whose VIN is provided in the request '''
        resp = []
        vin = request.GET.get('vin')
        if not vin:
            return HttpBadRequest("Vin is required.")
        try:
            product_object = common.ProductData.objects.get(vin = vin)
            product_coupons = common.CouponData.objects.filter(vin=product_object)
            for i in map(model_to_dict, product_coupons):
                resp.append(utils.get_dict_from_object(i))
        except Exception as ex:
            logger.info("[Exception get_product_coupons]:{0}".format(ex))
            return HttpBadRequest("Product VIN does not exists")
        return HttpResponse(json.dumps(resp))
    
    def get_product_purchase_information(self, request, **kwargs):
        '''This API fetches the purchase information for a particular product
           whose VIN is provided in the request '''
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
            return HttpBadRequest("Product VIN does not exists")
        return HttpResponse(json.dumps(resp))
    
    
    def get_user_product_information(self, request, **kwargs):
        '''This API fetches all the information of the products own 
           by a particular user whose mobile is provided in the request '''
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
            return HttpBadRequest("Not a registered number")
        return HttpResponse(json.dumps(resp))
        
        
    def get_product_warranty(self, request, **kwargs):
        '''This API fetches the warranty information for a particular product
           whose VIN is provided in the request '''

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
            return HttpBadRequest("No warranty info exists")
        return HttpResponse(json.dumps(resp))
    
    
    def get_product_insurance(self, request, **kwargs):
        '''This API fetches the insurance information for a particular product
           whose VIN is provided in the request '''

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
            return HttpBadRequest("No insurance info exists")
        return HttpResponse(json.dumps(resp))
            
    @csrf_exempt
    def get_notification_count(self, request, **kwargs):
        '''This API fetches count of unread notification of a particular 
           user whose mobile is provided in the request '''

        resp = {}
        phone_number = request.GET.get('mobile')
        if not phone_number:
            return HttpBadRequest("phone_number is required.")
        try:
            phone_number= mobile_format(phone_number)
            user_info = common.GladMindUsers.objects.get(phone_number=phone_number)
            notification_count = len(afterbuy_common.UserNotification.objects.filter(user=user_info, notification_read=0))
            resp = {'count': notification_count}
        except Exception as ex:
            logger.info("[Exception get_product_insurance]:{0}".format(ex))
            return HttpBadRequest("Not a registered number")
        return HttpResponse(json.dumps(resp))
    
    def get_notification_list(self, request, **kwargs):
        '''This API fetches all the notification of a particular 
           user whose mobile is provided in the request '''
#         self.is_authenticated(request)
        resp = []
        phone_number = request.GET.get('mobile')
        if not phone_number:
            return HttpBadRequest("phone_number is required.")
        try:
            phone_number= mobile_format(phone_number)
            user_info = common.GladMindUsers.objects.get(phone_number=phone_number)
            notifications = afterbuy_common.UserNotification.objects.filter(user=user_info)
            if not notifications:
                return HttpResponse("No notification exists.")
            else:
                for i in map(model_to_dict, notifications):
                    resp.append(utils.get_dict_from_object(i))
        except Exception as ex:
            logger.info("[Exception get_product_insurance]:{0}".format(ex))
            return HttpBadRequest("Not a registered number")
        return HttpResponse(json.dumps(resp))
    
    def save_user_details(self, request, **kwargs):
        phone_number = request.POST.get('mobile')
        if not phone_number:
            return HttpBadRequest("phone_number is required.")
        try:
            phone_number= mobile_format(phone_number)
            user_info = common.GladMindUsers.objects.get(phone_number=phone_number)
            user_info.customer_name = request.POST.get('name', None)
            user_info.email_id = request.POST.get('email', None)
            user_info.gender = request.POST.get('gender', None)
            user_info.address = request.POST.get('address', None)
            user_info.tshirt_size = request.POST.get('size', None)
            user_info.pincode = request.POST.get('pincode', None)
            user_info.save()
            data={'status':1, 'message':'details saved'}
        except Exception as ex:
            log_message = "unable to save details :{0}".format(ex)
            logger.info(log_message)
            data={'status':0, 'message':log_message}
        return HttpResponse(json.dumps(data), content_type="application/json")

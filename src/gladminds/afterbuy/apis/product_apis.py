import json
import logging
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse
from django.conf.urls import url
from django.template.base import kwarg_re
from tastypie.http import HttpBadRequest
from tastypie.resources import ModelResource
from tastypie.utils.urls import trailing_slash
from gladminds.core import base_models as common
from gladminds.core import utils
from gladminds.afterbuy import models as afterbuy_common
from gladminds.core.utils import mobile_format
from gladminds.core.apis.user_apis import AccessTokenAuthentication
from django.contrib.auth.models import User
from gladminds.core.apis.base_apis import CustomBaseModelResource
from gladminds.afterbuy.managers import get_product

logger = logging.getLogger("gladminds")

class ProductResources(CustomBaseModelResource):
    class Meta:
        resource_name = 'products'
        queryset = afterbuy_common.UserProduct.objects.all() 
        authentication = AccessTokenAuthentication()
        always_return_data = True

    def prepend_urls(self):
        return [
                url(r"^(?P<resource_name>%s)/(?P<product_id>[\d]+)/insurance%s" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_product_insurance'), name="get_product_insurance"),
                url(r"^(?P<resource_name>%s)/(?P<product_id>[\d]+)/insurance_save%s" % (self._meta.resource_name, trailing_slash()), self.wrap_view('save_product_insurance'), name="save_product_insurance"),
                url(r"^(?P<resource_name>%s)/(?P<product_id>[\d]+)/license%s" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_product_license'), name="get_product_license"),
                url(r"^(?P<resource_name>%s)/(?P<product_id>[\d]+)/registration%s" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_product_registration_certificate'), name="get_product_registration_certificate"),
                url(r"^(?P<resource_name>%s)/(?P<product_id>[\d]+)/pollution%s" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_product_pollution_certificate'), name="get_product_pollution_certificate"),
                url(r"^(?P<resource_name>%s)/(?P<product_id>[\d]+)/support%s" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_product_support'), name="get_product_support"),
                url(r"^(?P<resource_name>%s)/(?P<product_id>[\d]+)/invoice%s" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_product_invoice'), name="get_product_invoice")
        ]
        

    def get_product_insurance(self, request, **kwargs):
        resp = {}
        mobile = request.GET.get('phone_number')
        product_id = kwargs.get('product_id')
        try:
            phone_number= mobile_format(mobile)
            product_info = get_product(phone_number, product_id)
            insurance_info = afterbuy_common.ProductInsuranceInfo.objects.get(product=product_info)
            for field in ['agency_name', 'policy_number', 'premium', 'agency_contact',
                           'insurance_type', 'nominee', 'issue_date', 'expiry_date', 'vehicle_value','image_url']:
                resp[field] = getattr(insurance_info, field)
            resp = utils.get_dict_from_object(resp)
        except Exception as ex:
            logger.info("[Exception get_product_insurance]:{0}".format(ex))
            return HttpBadRequest("No insurance info exists")
        return HttpResponse(json.dumps(resp))
    
    def save_product_insurance(self, request, **kwargs):
        phone_number = request.POST.get('phone_number')
        product_id = kwargs.get('product_id')
        if not phone_number:
            return HttpBadRequest("phone_number is required.")
        try:
            phone_number= mobile_format(phone_number)
            product_info = get_product(phone_number, product_id)
            insurance_info = afterbuy_common.ProductInsuranceInfo(product=product_info)
            insurance_info.save()
            insurance_info.agency_name = request.POST.get('agency_name', None)
            insurance_info.policy_number = request.POST.get('policy_number', None)
            insurance_info.premium = request.POST.get('premium', None)
            insurance_info.agency_contact = request.POST.get('agency_contact', None)
            insurance_info.insurance_type = request.POST.get('insurance_type', None)
            insurance_info.nominee = request.POST.get('nominee', None)
            insurance_info.issue_date = request.POST.get('issue_date', None)
            insurance_info.expiry_date = request.POST.get('expiry_date', None)
            insurance_info.vehicle_value = request.POST.get('vehicle_value', None)
            insurance_info.image_url = request.POST.get('image_url', None)
            insurance_info.save()
            data={'status':1, 'message':'details saved'}
        except Exception as ex:
            print ex
            log_message = "unable to save details :{0}".format(ex)
            logger.info(log_message)
            data={'status':0, 'message':log_message}
        return HttpResponse(json.dumps(data), content_type="application/json")

        
    def get_product_license(self, request, **kwargs):
        resp = {}
        mobile = request.GET.get('phone_number')
        product_id = kwargs.get('product_id')
        try:
            phone_number= mobile_format(mobile)
            product_info = get_product(phone_number, product_id)
            license_info = afterbuy_common.License.objects.get(product=product_info)
            for field in ['license_number', 'issue_date', 'expiry_date', 'blood_group','image_url']:
                resp[field] = getattr(license_info, field)
            resp = utils.get_dict_from_object(resp)
        except Exception as ex:
            logger.info("[Exception get_product_license]:{0}".format(ex))
            return HttpBadRequest("No license info exists")
        return HttpResponse(json.dumps(resp))
    
    def get_product_registration_certificate(self, request, **kwargs):
        resp = {}
        mobile = request.GET.get('phone_number')
        product_id = kwargs.get('product_id')
        try:
            phone_number= mobile_format(mobile)
            product_info = get_product(phone_number, product_id)
            registration_info = afterbuy_common.RegistrationCertificate.objects.get(product=product_info)
            for field in ['vehicle_registration_number', 'registration_date', 'chassis_number', 'owner_name', 'address', 'registration_upto', 'manufacturer', 'manufacturing_date', 'model_number', 'colour', 'image_url']:
                resp[field] = getattr(registration_info, field)
            resp = utils.get_dict_from_object(resp)
        except Exception as ex:
            logger.info("[Exception get_product_registration_certificate]:{0}".format(ex))
            return HttpBadRequest("No registration_certificate info exists")
        return HttpResponse(json.dumps(resp))
  
    def get_product_pollution_certificate(self, request, **kwargs):
        resp = {}
        mobile = request.GET.get('phone_number')
        product_id = kwargs.get('product_id')
        try:
            phone_number= mobile_format(mobile)
            product_info = get_product(phone_number, product_id)
            pollution_info = afterbuy_common.PollutionCertificate.objects.get(product=product_info)
            for field in ['pucc_number', 'issue_date', 'expiry_date', 'image_url']:
                resp[field] = getattr(pollution_info, field)
            resp = utils.get_dict_from_object(resp)
        except Exception as ex:
            logger.info("[Exception get_product_pollution_certificate]:{0}".format(ex))
            return HttpBadRequest("No pollution_certificate info exists")
        return HttpResponse(json.dumps(resp))
  
    def get_product_support(self, request, **kwargs):
        resp = {}
        mobile = request.GET.get('phone_number')
        product_id = kwargs.get('product_id')
        try:
            phone_number= mobile_format(mobile)
            product_info = get_product(phone_number, product_id)
            support_info = afterbuy_common.Support.objects.get(product=product_info)
            for field in ['toll_free', 'service_center_name', 'service_center_number', 'feedback_form']:
                resp[field] = getattr(support_info, field)
            resp = utils.get_dict_from_object(resp)
        except Exception as ex:
            logger.info("[Exception get_product_support]:{0}".format(ex))
            return HttpBadRequest("No support info exists")
        return HttpResponse(json.dumps(resp))

    def get_product_invoice(self, request, **kwargs):
        resp = {}
        mobile = request.GET.get('phone_number')
        product_id = kwargs.get('product_id')
        try:
            phone_number= mobile_format(mobile)
            product_info = get_product(phone_number, product_id)
            invoice_info = afterbuy_common.Invoice.objects.get(product=product_info)
            for field in ['invoice_number', 'purchase_date', 'dealer_name', 'dealer_contact', 'amount', 'image_url']:
                resp[field] = getattr(invoice_info, field)
            resp = utils.get_dict_from_object(resp)
        except Exception as ex:
            logger.info("[Exception get_product_invoice]:{0}".format(ex))
            return HttpBadRequest("No invoice info exists")
        return HttpResponse(json.dumps(resp))


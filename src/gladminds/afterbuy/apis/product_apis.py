import json
import logging
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse
from django.conf.urls import url
from tastypie.http import HttpBadRequest
from tastypie.resources import ModelResource
from tastypie.utils.urls import trailing_slash

from gladminds.core import base_models as common
from gladminds.core import utils
from gladminds.afterbuy import models as afterbuy_common
from gladminds.core.utils import mobile_format
from gladminds.core.apis.user_apis import AccessTokenAuthentication
from tastypie.authorization import Authorization
from django.contrib.auth.models import User
from gladminds.core.apis.base_apis import CustomBaseResource

logger = logging.getLogger("gladminds")

class ProductResources(CustomBaseResource):
    class Meta:
        resource_name = 'product'
        print "hello"
        authentication = AccessTokenAuthentication()

    def prepend_urls(self):
        return [
                url(r"^(?P<resource_name>%s)/(?P<product_id>[\d]+)/insurance%s" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_product_insurance'), name="get_product_insurance"),
                url(r"^(?P<resource_name>%s)/(?P<product_id>[\d]+)/license%s" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_product_license'), name="get_product_license"),
                url(r"^(?P<resource_name>%s)/(?P<product_id>[\d]+)/registration%s" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_product_registration_certificate'), name="get_product_registration_certificate"),
                url(r"^(?P<resource_name>%s)/(?P<product_id>[\d]+)/pollution%s" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_product_pollution_certificate'), name="get_product_pollution_certificate"),
                url(r"^(?P<resource_name>%s)/(?P<product_id>[\d]+)/support%s" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_product_support'), name="get_product_support"),
                url(r"^(?P<resource_name>%s)/(?P<product_id>[\d]+)/invoice%s" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_product_invoice'), name="get_product_invoice")
        ]
        
    def get_product_insurance(self, request, **kwargs):
        resp = {}
        mobile = request.GET.get('phone_number')
        id = kwargs.get('product_id')
        id = int(id)
        id = id-1
        try:
            phone_number= mobile_format(mobile)
            user_info = afterbuy_common.Consumer.objects.get(phone_number=phone_number)
            product_info = afterbuy_common.UserProduct.objects.filter(consumer=user_info)
            insurance_info = afterbuy_common.ProductInsuranceInfo.objects.get(product=product_info[id])
            for field in ['agency_name', 'policy_number', 'premium', 'agency_contact',
                           'insurance_type', 'nominee', 'issue_date', 'expiry_date', 'vehicle_value','image_url']:
                resp[field] = getattr(insurance_info, field)
            resp = utils.get_dict_from_object(resp)
        except Exception as ex:
            logger.info("[Exception get_product_insurance]:{0}".format(ex))
            return HttpBadRequest("No insurance info exists")
        return HttpResponse(json.dumps(resp))

    def get_product_license(self, request, **kwargs):
        resp = {}
        mobile = request.GET.get('phone_number')
        id = kwargs.get('product_id')
        id = int(id)
        id = id-1
        try:
            phone_number= mobile_format(mobile)
            user_info = afterbuy_common.Consumer.objects.get(phone_number=phone_number)
            product_info = afterbuy_common.UserProduct.objects.filter(consumer=user_info)
            license_info = afterbuy_common.License.objects.get(product=product_info[id])
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
        id = kwargs.get('product_id')
        id = int(id)
        id = id-1
        try:
            phone_number= mobile_format(mobile)
            user_info = afterbuy_common.Consumer.objects.get(phone_number=phone_number)
            product_info = afterbuy_common.UserProduct.objects.filter(consumer=user_info)
            registration_info = afterbuy_common.RegistrationCertificate.objects.get(product=product_info[id])
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
        id = kwargs.get('product_id')
        id = int(id)
        id = id-1
        try:
            phone_number= mobile_format(mobile)
            user_info = afterbuy_common.Consumer.objects.get(phone_number=phone_number)
            product_info = afterbuy_common.UserProduct.objects.filter(consumer=user_info)
            pollution_info = afterbuy_common.PollutionCertificate.objects.get(product=product_info[id])
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
        id = kwargs.get('product_id')
        id = int(id)
        id = id-1
        try:
            phone_number= mobile_format(mobile)
            user_info = afterbuy_common.Consumer.objects.get(phone_number=phone_number)
            product_info = afterbuy_common.UserProduct.objects.filter(consumer=user_info)
            support_info = afterbuy_common.Support.objects.get(product=product_info[id])
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
        id = kwargs.get('product_id')
        id = int(id)
        id = id-1
        try:
#              phone_number= mobile_format(mobile)
            phone_number=mobile
            user_info = afterbuy_common.Consumer.objects.get(phone_number=phone_number)
            product_info = afterbuy_common.UserProduct.objects.filter(consumer=user_info)
            invoice_info = afterbuy_common.Invoice.objects.get(product=product_info[id])
            for field in ['invoice_number', 'purchase_date', 'dealer_name', 'dealer_contact', 'amount', 'image_url']:
                resp[field] = getattr(invoice_info, field)
            resp = utils.get_dict_from_object(resp)
        except Exception as ex:
            logger.info("[Exception get_product_invoice]:{0}".format(ex))
            return HttpBadRequest("No invoice info exists")
        return HttpResponse(json.dumps(resp))

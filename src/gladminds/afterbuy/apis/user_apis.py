import json
import logging
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse
from django.conf.urls import url
from tastypie.http import HttpBadRequest
from tastypie.resources import ModelResource
from tastypie.utils.urls import trailing_slash
from django.contrib.auth.models import User, Group
from gladminds.core import base_models as common
from gladminds.core import utils
from gladminds.afterbuy import models as afterbuy_common
from gladminds.core.utils import mobile_format
from gladminds.core.resource.authentication import AccessTokenAuthentication
from gladminds.core.resource.base_resource import CustomBaseResource

logger = logging.getLogger("gladminds")

class AfterBuyResources(CustomBaseResource):
    class Meta:
#         queryset = common.ProductData.objects.all()
        resource_name = 'afterbuy'
        authentication = AccessTokenAuthentication()

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/user/registration%s" % (self._meta.resource_name, trailing_slash()), self.wrap_view('save_user_details'), name="save_user_details"),
            url(r"^(?P<resource_name>%s)/user/feedback%s" % (self._meta.resource_name, trailing_slash()), self.wrap_view('save_user_feedback'), name="save_user_feedback"),
            url(r"^(?P<resource_name>%s)/product/coupons%s" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_product_coupons'), name="get_product_coupons"),
            url(r"^(?P<resource_name>%s)/product/purchase-info%s" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_product_purchase_information'), name="get_product_purchase_information"),
            url(r"^(?P<resource_name>%s)/product/warranty%s" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_product_warranty'), name="get_product_warranty"),
            url(r"^(?P<resource_name>%s)/product/insurance%s" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_product_insurance'), name="get_product_insurance"),
            url(r"^(?P<resource_name>%s)/product/info%s" % (self._meta.resource_name, trailing_slash()), self.wrap_view('dispatch_dict'), name="api_dispatch_dict"),
            url(r"^(?P<resource_name>%s)/notification/count%s" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_notification_count'), name="get_notification_count"),
            url(r"^(?P<resource_name>%s)/notification/list%s" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_notification_list'), name="get_notification_list"),
            url(r"^(?P<resource_name>%s)/product/spares%s" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_spares_list'), name="get_spares_list"),
            url(r"^(?P<resource_name>%s)/phone-details%s" % (self._meta.resource_name, trailing_slash()), self.wrap_view('save_user_phone_details'), name="save_user_phone_details"),
        ]

    def save_user_details(self, request, **kwargs):
        data = request.POST
        if not data:
            return HttpBadRequest("phone_number is required.")
        try:
            phone_number = mobile_format(request.POST.get('phone', None))
            create_user = User(username=data['username'], password=data['password'], email=data['email_id'])
            create_user.save()
            user_info = afterbuy_common.Consumer.objects.get(phone_number=phone_number)
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

    
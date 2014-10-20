import json
import logging
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse
from django.conf.urls import url
from tastypie.http import HttpBadRequest
from tastypie.resources import ModelResource
from tastypie.utils.urls import trailing_slash
from django.contrib.auth.models import User
from gladminds.core import base_models as common
from gladminds.core import utils
from gladminds.afterbuy import utils as afterbuy_utils
from gladminds.afterbuy import models as afterbuy_common

from gladminds.core.apis.user_apis import AccessTokenAuthentication
from gladminds import settings
from gladminds.bajaj.services import message_template
from gladminds.core.managers.mail import sent_otp_email
from gladminds.core.apis.base_apis import CustomBaseResource
from gladminds.core.utils import mobile_format, get_task_queue

logger = logging.getLogger("gladminds")

class UserResources(CustomBaseResource):
    class Meta:
#         queryset = common.ProductData.objects.all()
        resource_name = 'user'
        authentication = AccessTokenAuthentication()

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/registration%s" % (self._meta.resource_name, trailing_slash()), self.wrap_view('save_user_details'), name="save_user_details"),
            url(r"^(?P<resource_name>%s)/authenticate/email-id%s" % (self._meta.resource_name, trailing_slash()), self.wrap_view('authenticate_user_email_id'), name="authenticate_user_email_id"),
            url(r"^(?P<resource_name>%s)/send-opt%s" % (self._meta.resource_name, trailing_slash()), self.wrap_view('authenticate_user_send_otp'), name="authenticate_user_send_otp"),
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
            phone_number = mobile_format(data['phone_number'])
            create_user = User(username=data['name'], password=data['password'], email=data['email_id'])
            create_user.save()
            try:
                user_details = afterbuy_common.Consumer.objects.get(phone_number=phone_number)
                data = data={'status':0, 'message':'already registered'}
            except:
                customer_id = utils.generate_unique_customer_id()
                user_register = afterbuy_common.Consumer(user=create_user, phone_number=phone_number, consumer_id=customer_id)
                user_register.save()
                data = {'status': 1, 'message': 'succefully registerd'}
        except Exception as ex:
            log_message = "unable to save details :{0}".format(ex)
            logger.info(log_message)
            data={'status':0, 'message':log_message}
        return HttpResponse(json.dumps(data), content_type="application/json")

    def dispatch_dict(self, request, **kwargs):
        if request.method == "GET":
            return self.get_user_product_information(request, **kwargs)

    def get_user_product_information(self, request, **kwargs):
        '''This API fetches all the information of the products own
        by a particular user whose mobile is provided in the request '''
        resp = []
        mobile = request.GET.get('phone_number')
        if not mobile:
            return HttpBadRequest("Phone Number is required.")
        try:
            phone_number = mobile_format(mobile)
            user_info = afterbuy_common.Consumer.objects.get(phone_number=phone_number)
            product_info = afterbuy_common.UserProduct.objects.filter(consumer=user_info)
            if not product_info:
                data={'status':0, 'message':"No product exist."}
                return HttpResponse(json.dumps(data), content_type="application/json")
            else:
                for product_object in map(model_to_dict, product_info):
                    resp.append(utils.get_dict_from_object(product_object))
        except Exception as ex:
            logger.info("[Exception get_user_product_information]:{0}".format(ex))
            return HttpBadRequest("Not a registered number")
        return HttpResponse(json.dumps(resp))

    def authenticate_user_email_id(self, request, **kwargs):
        data = request.POST
        if not data:
            return HttpBadRequest("email id is required")
        try:
            user_email_id = User.objects.filter(email=data['email_id'])
            if len(user_email_id) > 0:
                data = {'status': 1, 'message': 'authenticated email_id'}
            else:
                data = {'status': 0, 'message': 'unauthenticated email_id'}
        except Exception as ex:
            log_message = "unable to authenticate email_id :{0}".format(ex)
            logger.info(log_message)
            data = {'status': 0, 'message': log_message}
        return HttpResponse(json.dumps(data), content_type="application/json")

    def authenticate_user_send_otp(self, request, **kwargs):
        data = request.POST
        if not data:
            return HttpBadRequest("email id is required")
        try:
            phone_number = data['phone_number']
            logger.info('OTP request received. Mobile: {0}'.format(phone_number))
            user = afterbuy_common.Consumer.objects.filter(phone_number=mobile_format(phone_number))[0]
            token = afterbuy_utils.get_token(user, phone_number)
            message = message_template.get_template('SEND_OTP').format(token)
            if settings.ENABLE_AMAZON_SQS:
                task_queue = get_task_queue()
                task_queue.add('send_otp', {'phone_number':phone_number, 'message':message})
            else:
                send_otp.delay(phone_number=phone_number, message=message)  # @UndefinedVariable
            logger.info('OTP sent to mobile {0}'.format(phone_number))
            #Send email if email address exist
            if user.user.email:
                sent_otp_email(data=token, receiver=user.email, subject='Your OTP')
                data = {'status': 1, 'message': "OTP sent_successfully"}
        except Exception as ex:
            print "ex",ex
            logger.error('Invalid details, mobile {0}'.format(request.POST.get('phone_number', '')))
            data = {'status': 0, 'message': "inavlid phone_number"}
        return HttpResponse(json.dumps(data), content_type="application/json")

from uuid import uuid4
import json
import logging
import requests
import re
from gladminds.core.utils import check_password
from django.http.response import HttpResponse
from django.conf.urls import url
from tastypie.http import HttpBadRequest
from tastypie.utils.urls import trailing_slash
from django.contrib.auth.models import User
from django.contrib.auth import  login
from django.conf import settings
from gladminds.afterbuy import utils as afterbuy_utils
from gladminds.core.auth import otp_handler
from gladminds.settings import API_FLAG, COUPON_URL

from gladminds.afterbuy import models as afterbuy_model
from tastypie import fields, http
from gladminds.core.apis.base_apis import CustomBaseModelResource
from gladminds.sqs_tasks import send_otp
from django.contrib.auth import authenticate
from tastypie.resources import  ALL, ModelResource
from tastypie.exceptions import ImmediateHttpResponse
from gladminds.core.views.auth_view import get_access_token, create_access_token
from tastypie.authorization import DjangoAuthorization
from gladminds.core.apis.authorization import CustomAuthorization,\
    MultiAuthorization
from django.contrib.sites.models import RequestSite
from gladminds.core.apis.authentication import AccessTokenAuthentication
from django.db.transaction import atomic
from gladminds.core.auth_helper import GmApps
from gladminds.afterbuy.apis.validations import ConsumerValidation,\
    UserValidation
from gladminds.core.cron_jobs.queue_utils import send_job_to_queue
from gladminds.core.model_helpers import format_phone_number
from gladminds.core.auth import otp_handler
from gladminds.core import constants

logger = logging.getLogger("gladminds")


class DjangoUserResources(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'users'
        authentication = AccessTokenAuthentication()
        validation = UserValidation()
        authorization = MultiAuthorization(DjangoAuthorization(), CustomAuthorization())
        excludes = ['password', 'is_superuser']
        always_return_data = True
        
class ConsumerResource(CustomBaseModelResource):

    user = fields.ForeignKey(DjangoUserResources, 'user', null=True, blank=True, full=True)

    class Meta:
        queryset = afterbuy_model.Consumer.objects.all()
        resource_name = "consumers"
        authentication = AccessTokenAuthentication()
        validation = ConsumerValidation()
        authorization = MultiAuthorization(DjangoAuthorization(), CustomAuthorization())
        detail_allowed_methods = ['get', 'delete', 'put']
        always_return_data = True
        filtering = {
                     "consumer_id": ALL
                     }

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/registration%s" % (self._meta.resource_name, trailing_slash()), self.wrap_view('user_registration'), name="user_registration"),
            url(r"^(?P<resource_name>%s)/activate-email%s" % (self._meta.resource_name, trailing_slash()), self.wrap_view('activate_email'), name="activate_email"),
            url(r"^(?P<resource_name>%s)/phone-number/send-otp%s" % (self._meta.resource_name, trailing_slash()), self.wrap_view('sent_otp_user_phone_number'), name="sent_otp_user_phone_number"),
            url(r"^(?P<resource_name>%s)/authenticate-email%s" % (self._meta.resource_name, trailing_slash()), self.wrap_view('authenticate_user_email_id'), name="authenticate_user_email_id"),
            url(r"^(?P<resource_name>%s)/send-otp/forgot-password%s" % (self._meta.resource_name, trailing_slash()), self.wrap_view('authenticate_user_send_otp'), name="authenticate_user_send_otp"),
            url(r"^(?P<resource_name>%s)/forgot-password/(?P<type>[a-zA-Z0-9.-]+)%s" % (self._meta.resource_name, trailing_slash()), self.wrap_view('change_user_password'), name="change_user_password"),
            url(r"^(?P<resource_name>%s)/login%s" % (self._meta.resource_name, trailing_slash()), self.wrap_view('auth_login'), name="auth_login"),
            url(r"^(?P<resource_name>%s)/validate-otp%s" % (self._meta.resource_name, trailing_slash()), self.wrap_view('validate_otp'), name="validate_otp"),
            url(r"^(?P<resource_name>%s)/logout%s" % (self._meta.resource_name, trailing_slash()), self.wrap_view('logout'), name="logout"),
            url(r"^(?P<resource_name>%s)/product-details%s" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_product_details'), name="get_product_details")
        ]

    def sent_otp_user_phone_number(self, request, **kwargs):
        if request.method != 'POST':
            return HttpResponse(json.dumps({"message":"method not allowed"}), content_type="application/json",status=401)
        try:
            load = json.loads(request.body)
        except:
            return HttpResponse(content_type="application/json", status=404)
        phone_number = load.get('phone_number')
        if not phone_number:
            return HttpBadRequest("phone_number is required.")
        try:
            otp = otp_handler.get_otp(phone_number=phone_number)
            message = afterbuy_utils.get_template('SEND_OTP').format(otp)
            send_job_to_queue(send_otp, {'phone_number':phone_number, 'message':message, 'sms_client':settings.SMS_CLIENT})
            logger.info('OTP sent to mobile {0}'.format(phone_number))
            data = {'status': 1, 'message': "OTP sent_successfully"}

        except Exception as ex:
            logger.error('Invalid details, mobile {0} and exception {1}'.format(request.POST.get('phone_number', ''),ex))
            data = {'status': 0, 'message': ex}
        return HttpResponse(json.dumps(data), content_type="application/json")
            
    @atomic(using=GmApps.AFTERBUY)
    def user_registration(self, request, **kwargs):
        if request.method != 'POST':
            return HttpResponse(json.dumps({"message":"method not allowed"}), content_type="application/json",status=401)
        try:
            load = json.loads(request.body)
        except:
            return HttpResponse(content_type="application/json", status=404)
#         otp_token = load['otp_token']
        phone_number = load['phone_number']
#         try:
#             if not (settings.ENV in settings.IGNORE_ENV and otp_token in settings.HARCODED_OTPS):
#                 otp_handler.validate_otp(otp_token, phone_number=phone_number)
#         except Exception:
#             raise ImmediateHttpResponse(
#                 response=http.HttpBadRequest('Wrong OTP!'))
        phone_number = load.get('phone_number')
        email_id = load.get('email_id')
        user_name = load.get('username', str(uuid4())[:30])
        first_name = load.get('first_name')
        last_name = load.get('last_name','')
        password = load.get('password')
        invalid_password = check_password(password)
        if not invalid_password:
            return HttpBadRequest("password is not meant according to the rules")
        if not phone_number or not password:
            return HttpBadRequest("phone_number, password required.")
        try:
            afterbuy_model.Consumer.objects.get(
                                                phone_number=phone_number)
            data = {'status': 0, 'message': 'phone number already registered'}
        except Exception as ex:
                try:
                    afterbuy_model.Consumer.objects.get(user__email=email_id, is_email_verified=True)
                    data = {'status': 0, 'message': 'email id already registered'}
                    return HttpResponse(json.dumps(data), content_type="application/json")
                except Exception as ex:
                        log_message = "new user :{0}".format(ex)
                        logger.info(log_message)
                        create_user = User.objects.using(GmApps.AFTERBUY).create(username=user_name)
                        create_user.set_password(password)
                        create_user.email = email_id
                        create_user.first_name = first_name
                        create_user.last_name = last_name
                        create_user.save(using=GmApps.AFTERBUY)
                        user_register = afterbuy_model.Consumer(user=create_user,
                                    phone_number=phone_number)
                        user_register.save()
                        site = RequestSite(request)
                        afterbuy_model.EmailToken.objects.create_email_token(user_register, email_id, site)
                        data = {'status': 1, 'message': 'succefully registered'}
        return HttpResponse(json.dumps(data), content_type="application/json")

    def activate_email(self, request, **kwargs):
        activation_key = request.GET['activation_key']
        activated_user = afterbuy_model.EmailToken.objects.activate_user(activation_key)
        if activated_user:
            data = {'status': 1, 'message': 'email-id validated'}
        else:
            data = {'status': 0, 'message': 'email-id not validated'}
        return HttpResponse(json.dumps(data), content_type="application/json")

    def validate_user_phone_number(self,phone_number, otp):
        if not otp and not phone_number :
            return HttpBadRequest("otp and phone_number required")
        try:
            otp_handler.validate_otp(otp, phone_number=phone_number)

        except Exception as ex:
                data = {'status': 0, 'message': "invalid OTP"}
                logger.info("[Exception OTP]:{0}".
                            format(ex))
        return HttpResponse(json.dumps(data), content_type="application/json")

    def authenticate_user_email_id(self, request, **kwargs):
        email_id = request.POST.get('email_id')
        if not email_id:
            return HttpBadRequest("email id is required")
        try:
            afterbuy_model.Consumer.objects.get(user__email=email_id, is_email_verified=True)
            data = {'status': 1, 'message': "emailid verified"}
            return HttpResponse(json.dumps(data), content_type="application/json")
        except Exception as ex:
                log_message = "new user :{0}".format(ex)
                logger.info(log_message)
                data = {'status': 0, 'message': "Either your email is not verified"}
        return HttpResponse(json.dumps(data), content_type="application/json")

    def authenticate_user_send_otp(self, request, **kwargs):
        if request.method != 'POST':
            return HttpResponse(json.dumps({"message":"method not allowed"}), content_type="application/json",status=401)
        try:
            load = json.loads(request.body)
        except:
            return HttpResponse(content_type="application/json", status=404)
        email = load.get('email_id')
        phone_number = load.get('phone_number')
        if not phone_number and not email:
            return HttpBadRequest("phone_number or email is required")
        try:
            if phone_number:
                phone_number = format_phone_number(phone_number)
                logger.info('OTP request received. Mobile: {0}'.format(phone_number))
                user_obj = afterbuy_model.Consumer.objects.get(phone_number=phone_number).user
                otp = otp_handler.get_otp(user=user_obj)
                message = afterbuy_utils.get_template('SEND_OTP').format(otp)
                send_job_to_queue('send_otp', {'phone_number': phone_number,
                                             'message': message, "sms_client": settings.SMS_CLIENT})
                logger.info('OTP sent to mobile {0}'.format(phone_number))
                data = {'status': 1, 'message': "OTP sent_successfully"}
                #Send email if email address exist
            if email:
                try:
                    consumer_obj = afterbuy_model.Consumer.objects.get(user__email=email, is_email_verified=True)
                    site = RequestSite(request)
                    afterbuy_model.EmailToken.objects.create_email_token(consumer_obj, email, site, trigger_mail='forgot-password')
                    data = {'status': 1, 'message': "Password reset link sent successfully"}
                    return HttpResponse(json.dumps(data), content_type="application/json")
                except Exception as ex:
                        log_message = "new user :{0}".format(ex)
                        logger.info(log_message)
                        data = {'status': 0, 'message': "Either your email is not verified or its not exist"}
        except Exception as ex:
            logger.error('Invalid details, mobile {0} and exception {1}'.format(request.POST.get('phone_number', ''),ex))
            data = {'status': 0, 'message': "inavlid phone_number/email_id"}
        return HttpResponse(json.dumps(data), content_type="application/json")

    def change_user_password(self, request, **kwargs):
        if request.method != 'POST':
            return HttpResponse(json.dumps({"message":"method not allowed"}), content_type="application/json",status=401)
        try:
            load = json.loads(request.body)
        except:
            return HttpResponse(content_type="application/json", status=404)
        type = kwargs['type']
        otp_token = load.get('otp_token')
        password = load.get('password1')
        repassword = load.get('password2')
        invalid_password = check_password(repassword)
        if (invalid_password):
            return HttpBadRequest("password is not meant according to the rules")
        auth_key = load.get('auth_key')
        user_details = {}
        if not type:
            return HttpBadRequest("type not defined use email/phone")
        if password != repassword:
            return HttpBadRequest("password1 and password2 not matched")
        try:
            if type=='phone':
                try:
                    if not (settings.ENV in settings.IGNORE_ENV and otp_token in settings.HARCODED_OTPS):
                        consumer = afterbuy_model.OTPToken.objects.get(token=otp_token).user
                        otp_handler.validate_otp(otp_token, user=consumer)
                except Exception:
                    raise ImmediateHttpResponse(
                        response=http.HttpBadRequest('Wrong OTP!'))
                user_details['id'] = consumer.user.id
            elif type=='email':
                try:
                    user_obj = afterbuy_model.EmailToken.objects.get(activation_key=auth_key).user
                except Exception:
                    raise ImmediateHttpResponse(
                        response=http.HttpBadRequest('invalid authentication key!'))
                user_details['email'] = user_obj.user.email
            user = User.objects.filter(**user_details)[0]
            user.set_password(password)
            user.save()
            data = {'status': 1, 'message': "password updated successfully"}
        except Exception as ex:
            logger.error('Invalid details, mobile {0} and exception {1}'.format(request.POST.get('phone_number', ''),ex))
            data = {'status': 0, 'message': "password not updated"}
        return HttpResponse(json.dumps(data), content_type="application/json")

    def auth_login(self, request, **kwargs):
        if request.method != 'POST':
            return HttpResponse(json.dumps({"message":"method not allowed"}), content_type="application/json",status=401)
        try:
            load = json.loads(request.body)
        except:
            return HttpResponse(content_type="application/json", status=404)
        phone_number = load.get('phone_number')
        email_id = load.get('email_id')
        password = load.get('password')
        if not phone_number and not email_id and password:
            return HttpBadRequest("Phone Number/email_id and password  required.")
        try:
            if phone_number:
                user_obj = afterbuy_model.Consumer.objects.get(phone_number
                                                 =phone_number).user
            elif email_id:
                    user_obj = afterbuy_model.Consumer.objects.get(user__email=email_id, is_email_verified=True).user
            http_host = request.META.get('HTTP_HOST', 'localhost')
            user_auth = authenticate(username=str(user_obj.username),
                                password=password)
            if user_auth is not None:
                access_token = create_access_token(user_auth, user_obj.username, password, http_host)
                if user_auth.is_active:
                    login(request, user_auth)
                    data = {'status': 1, 'message': "login successfully", 'access_token': access_token, "user_id": user_auth.id}
            else:
                data = {'status': 0, 'message': "login unsuccessfull"}
        except Exception as ex:
                data = {'status': 0, 'message': "login unsuccessfull"}
                logger.info("[Exception get_user_login_information]:{0}".
                            format(ex))
        return HttpResponse(json.dumps(data), content_type="application/json")

    def logout(self, request, **kwargs):
        from provider.oauth2.models import AccessToken
        access_token = request.GET.get('access_token')
        if access_token:
            try:
                at_obj = AccessToken.objects.using(settings.BRAND).get(token=access_token)
                if settings.OAUTH_DELETE_EXPIRED:
                    at_obj.delete()
                data = {'status': 0, 'message': "logout successfully"}
            except Exception as ex:
                data = {'status': 0, 'message': "access_token_not_valid"}
                logger.info("[Exception get_user_login_information]:{0}".
                            format(ex))
        return HttpResponse(json.dumps(data), content_type="application/json")
    
    def get_product_details(self, request, **kwargs):
        port = request.META['SERVER_PORT']
        access_token = request.META['QUERY_STRING'] 
        if request.method != 'POST':
            return HttpResponse(json.dumps({"message":"method not allowed"}), content_type="application/json",status=401)
        try:
            load = json.loads(request.body)
        except:
            return HttpResponse(content_type="application/json", status=404)

        phone_number = load.get('phone_number', None)
        product_id = load.get('product_id', None)
        query = '/v1/coupons/?'+ access_token
        
        if product_id:
            if product_id[:3].upper()!= constants.KTM_VIN:
                return HttpResponse(json.dumps({'message':'Incorrect VIN'}), content_type='application/json')
            query = query + '&product__product_id='+product_id
        
        if phone_number:
            query = query + '&product__customer_phone_number__contains='+phone_number+'&product__product_id__startswith=VBK'
        
        try:
            if not API_FLAG:
                result = requests.get('http://'+COUPON_URL+':'+port+query)
            else:
#                 result = requests.get('http://'+COUPON_URL+query)
                result = requests.get('http://qa.bajaj.gladminds.co'+query)
                logger.info("[Product details - KTM settings.evn]:{0}".format(settings.ENV))

            if len(json.loads(result.content)['objects']) == 0:
                    return HttpResponse(json.dumps({'message' : 'Invalid Details'}), content_type='application/json')
            else:
                return HttpResponse(json.dumps({'result': json.loads(result.content)}), content_type='application/json')
        
        except Exception as ex:
            logger.info("[Exception while fetching product details]:{0}".format(ex))

class UserNotificationResource(CustomBaseModelResource):
    consumer = fields.ForeignKey(ConsumerResource, 'consumer', null=True, blank=True, full=True)

    class Meta:
        queryset = afterbuy_model.UserNotification.objects.all()
        resource_name = "notifications"
        authentication = AccessTokenAuthentication()
        authorization = CustomAuthorization()
        detail_allowed_methods = ['get', 'post', 'put']
        allowed_update_fields = ['notification_read']
        always_return_data = True
        filtering = {
                     "consumer": ALL,
                     "id": ALL,
                     "notification_read": ALL
                     }


class ServiceTypeResource(CustomBaseModelResource):

    class Meta:
        queryset = afterbuy_model.ServiceType.objects.all()
        resource_name = "service-types"
        authentication = AccessTokenAuthentication()
        authorization = DjangoAuthorization()
        always_return_data = True


class ServiceResource(CustomBaseModelResource):
    consumer = fields.ForeignKey(ConsumerResource, 'consumer')
    service_type = fields.ForeignKey(ServiceTypeResource, 'service_type', full=True)

    class Meta:
        queryset = afterbuy_model.Service.objects.all()
        resource_name = "services"
        authentication = AccessTokenAuthentication()
        authorization = MultiAuthorization(DjangoAuthorization(), CustomAuthorization())
        always_return_data = True
        filtering = {
                     "consumer": ALL,
                     "service_type": ALL,
                     "is_active": ALL
                     }

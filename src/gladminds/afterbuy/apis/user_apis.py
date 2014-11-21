import json
import logging
from django.forms.models import model_to_dict
from django.http.response import HttpResponse
from django.conf.urls import url
from tastypie.http import HttpBadRequest
from tastypie.utils.urls import trailing_slash
from django.contrib.auth.models import User
from django.contrib.auth import  login
from django.conf import settings
from gladminds.core import utils
from gladminds.afterbuy import utils as afterbuy_utils
from gladminds.afterbuy import models as afterbuy_model
from gladminds.core.apis.user_apis import AccessTokenAuthentication
from tastypie import fields, http
from gladminds.core.managers.mail import sent_otp_email
from gladminds.core.apis.base_apis import CustomBaseModelResource
from gladminds.core.utils import mobile_format, get_task_queue
from gladminds.sqs_tasks import send_otp
from django.contrib.auth import authenticate
from tastypie.resources import  ALL, ModelResource
from tastypie.authorization import Authorization
from gladminds.core.exceptions import OtpFailedException
from tastypie.exceptions import ImmediateHttpResponse

logger = logging.getLogger("gladminds")


class DjangoUserResources(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'django'
        excludes = ['is_active', 'is_staff', 'is_superuser']
        authorization = Authorization()
        detail_allowed_methods = ['get','post', 'delete', 'put']
        always_return_data = True
        filtering = {
            'username': ALL,
        }


class ConsumerResource(CustomBaseModelResource):

    user = fields.ForeignKey(DjangoUserResources, 'user', null=True, blank=True, full=True)

    class Meta:
        queryset = afterbuy_model.Consumer.objects.all()
        resource_name = "consumers"
        authorization = Authorization()
        detail_allowed_methods = ['get', 'post', 'delete', 'put']
        always_return_data = True
        filtering = {
                     "consumer_id" : ALL
                     }

    def hydrate(self, bundle):
        if bundle.request.method != 'POST':
            return bundle

        otp_token = bundle.data['otp_token']
        phone_number = bundle.data['phone_number']
        
        try:
            if not (settings.ENV in ["dev", "local"] and otp_token in settings.HARCODED_OTPS):
                afterbuy_utils.validate_otp(otp_token, phone_number=phone_number)
        except Exception:
            raise ImmediateHttpResponse(
                response=http.HttpBadRequest('Wrong OTP!'))

        user_dict = bundle.data['user']
        if isinstance(user_dict, dict) and 'pk' not in user_dict.keys():
            username = user_dict['username']
            password = user_dict['password']
            email = user_dict.get('email')
            first_name = user_dict.get('first_name', '')
            last_name = user_dict.get('last_name', '')
            user_obj = User.objects.create_user(username, email, password)
            user_obj.first_name = first_name
            user_obj.last_name = last_name
            user_obj.save()
            bundle.data['user'] = {"pk": user_obj.id}
        return bundle

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/registration%s" % (self._meta.resource_name, trailing_slash()), self.wrap_view('save_user_details'), name="save_user_details"),
            url(r"^(?P<resource_name>%s)/phone-number/send-otp%s" % (self._meta.resource_name, trailing_slash()), self.wrap_view('sent_otp_user_phone_number'), name="sent_otp_user_phone_number"),
            url(r"^(?P<resource_name>%s)/authenticate-email%s" % (self._meta.resource_name, trailing_slash()), self.wrap_view('authenticate_user_email_id'), name="authenticate_user_email_id"),
            url(r"^(?P<resource_name>%s)/send-otp%s" % (self._meta.resource_name, trailing_slash()), self.wrap_view('authenticate_user_send_otp'), name="authenticate_user_send_otp"),
            url(r"^(?P<resource_name>%s)/forgot-password%s" % (self._meta.resource_name, trailing_slash()), self.wrap_view('change_user_password'), name="change_user_password"),
            url(r"^(?P<resource_name>%s)/(?P<user_id>\d+)/details%s" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_user_details'), name="get_user_details"),
            url(r"^(?P<resource_name>%s)/(?P<user_id>\d+)/products%s" % (self._meta.resource_name, trailing_slash()), self.wrap_view('dispatch_dict'), name="api_dispatch_dict"),
            url(r"^(?P<resource_name>%s)/login%s" % (self._meta.resource_name, trailing_slash()), self.wrap_view('auth_login'), name="auth_login"),
            url(r"^(?P<resource_name>%s)/validate-otp%s" % (self._meta.resource_name, trailing_slash()), self.wrap_view('validate_otp'), name="validate_otp"),
        ]

    def sent_otp_user_phone_number(self, request, **kwargs):
        phone_number = request.POST.get('phone_number')
        if not phone_number:
            return HttpBadRequest("phone_number is required.")
        try:
            otp = afterbuy_utils.get_otp(phone_number=mobile_format(phone_number))
            message = afterbuy_utils.get_template('SEND_OTP').format(otp)
            if settings.ENABLE_AMAZON_SQS:
                task_queue = get_task_queue()
                task_queue.add('send_otp', {'phone_number':phone_number, 'message':message})
            else:
                send_otp.delay(phone_number=phone_number, message=message)  # @UndefinedVariable
            logger.info('OTP sent to mobile {0}'.format(phone_number))
            data = {'status': 1, 'message': "OTP sent_successfully"}

        except Exception as ex:
            logger.error('Invalid details, mobile {0} and exception {1}'.format(request.POST.get('phone_number', ''),ex))
            data = {'status': 0, 'message': ex}
        return HttpResponse(json.dumps(data), content_type="application/json")

    def validate_user_phone_number(self,phone_number, otp):
        if not otp and not phone_number :
            return HttpBadRequest("otp and phone_number/email_id required")
        try:
            afterbuy_utils.validate_otp(otp, phone_number=phone_number)

        except Exception as ex:
                data = {'status': 0, 'message': "invalid OTP"}
                logger.info("[Exception OTP]:{0}".
                            format(ex))
        return HttpResponse(json.dumps(data), content_type="application/json")

    def dispatch_dict(self, request, **kwargs):
        if request.method == "GET":
            return self.get_user_product_information(request, **kwargs)

    def get_user_product_information(self, request, **kwargs):
        '''This API fetches all the information of the products own
        by a particular user whose mobile is provided in the request '''
        resp = []
        customer_id = kwargs['user_id']
        customer_id = int(customer_id)
        if not id:
            return HttpBadRequest("user_id is required.")
        try:
            user_info = afterbuy_model.Consumer.objects.get(
                                user__id=customer_id)
            product_info = afterbuy_model.UserProduct.objects.filter(
                                    consumer=user_info)
            if not product_info:
                data = {'status': 0, 'message': "No product exist."}
                return HttpResponse(json.dumps(data),
                                    content_type="application/json")
            else:
                for product_object in map(model_to_dict, product_info):
                    resp.append(utils.get_dict_from_object(product_object))
        except Exception as ex:
            logger.info("[Exception get_user_product_information]:{0}".
                        format(ex))
            return HttpBadRequest("Not a registered number")
        return HttpResponse(json.dumps(resp))

    def authenticate_user_email_id(self, request, **kwargs):
        email_id = request.POST.get('email_id')
        if not email_id:
            return HttpBadRequest("email id is required")
        try:
            user_email_id = User.objects.filter(email=email_id)
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
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email_id',None)
        if not phone_number and not email:
            return HttpBadRequest("phone_number or email is required")
        try:
            if phone_number:
                logger.info('OTP request received. Mobile: {0}'.format(phone_number))
                consumer = afterbuy_model.Consumer.objects.get(phone_number=phone_number)
                otp = afterbuy_utils.get_otp(user=consumer.user)
                message = afterbuy_utils.get_template('SEND_OTP').format(otp)
                if settings.ENABLE_AMAZON_SQS:
                    task_queue = get_task_queue()
                    task_queue.add('send_otp', {'phone_number':phone_number, 'message':message})
                else:
                    send_otp.delay(phone_number=phone_number, message=message)  # @UndefinedVariable
                logger.info('OTP sent to mobile {0}'.format(phone_number))
                data = {'status': 1, 'message': "OTP sent_successfully"}
                #Send email if email address exist
            if email:
                user_obj = User.objects.get(email=email)
                otp = afterbuy_utils.get_otp(user=user_obj)
                sent_otp_email(data=otp, receiver=email, subject='Your OTP')
                data = {'status': 1, 'message': "OTP sent_successfully"}
        except Exception as ex:
            logger.error('Invalid details, mobile {0} and exception {1}'.format(request.POST.get('phone_number', ''),ex))
            data = {'status': 0, 'message': "inavlid phone_number/email_id"}
        return HttpResponse(json.dumps(data), content_type="application/json")

    def change_user_password(self, request, **kwargs):
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email_id')
        password = request.POST.get('password')
        kwargs = {}
        if not phone_number and not password and not email:
            return HttpBadRequest("mobile and password required")
        try:
            if phone_number:
                consumer = afterbuy_model.Consumer.objects.filter(phone_number=phone_number)[0]
                kwargs['id'] = consumer.user__id
            elif email:
                kwargs['email'] = email
            user = User.objects.filter(**kwargs)[0]
            user.set_password(password)
            user.save()
            data = {'status': 1, 'message': "password updated successfully"}
        except Exception as ex:
            logger.error('Invalid details, mobile {0} and exception {1}'.format(request.POST.get('phone_number', ''),ex))
            data = {'status': 0, 'message': "inavlid phone_number/email"}
        return HttpResponse(json.dumps(data), content_type="application/json")

    def get_user_details(self, request, **kwargs):
        customer_id = kwargs['user_id']
        cosumer_data = {}
        if not id:
            return HttpBadRequest("id is required.")
        try:
            customer_id = int(customer_id)
            consumer_obj = afterbuy_model.Consumer.objects.get(
                                                        user__id=customer_id)
            cosumer_data['username'] = consumer_obj.user.username
            cosumer_data['created_date'] = str(consumer_obj.created_date)
            cosumer_data['email'] = consumer_obj.user.email
            cosumer_data['phone_number'] = consumer_obj.phone_number
            cosumer_data['password'] = consumer_obj.user.password
            cosumer_data['name'] = consumer_obj.user.first_name
        except Exception as ex:
            logger.info("[Exception get_user_product_information]:{0}".format(ex))
            return HttpBadRequest("Not a registered user")
        return HttpResponse(json.dumps(cosumer_data), content_type="application/json")

    def auth_login(self, request, **kwargs):
        phone_number = request.POST.get('phone_number')
        email_id = request.POST.get('email_id')
        password = request.POST.get('password')
        if not phone_number and not email_id and password:
            return HttpBadRequest("Phone Number/email_id and password  required.")
        try:
            if phone_number:
                user_obj = afterbuy_model.Consumer.objects.get(phone_number
                                                 =phone_number).user
            elif email_id:
                user_obj = User.objects.get(email
                                                 =email_id)
            password = request.POST['password']
            user_auth = authenticate(username=str(user_obj.username),
                                password=password)
            if user_auth is not None:
                if user_auth.is_active:
                    login(request, user_auth)
                    data = {'status': 1, 'message': "login successfully", "user_id": user_auth.id}
            else:
                data = {'status': 0, 'message': "login unsuccessfull"}
        except Exception as ex:
                data = {'status': 0, 'message': "login unsuccessfull"}
                logger.info("[Exception get_user_login_information]:{0}".
                            format(ex))
        return HttpResponse(json.dumps(data), content_type="application/json")

    def validate_otp(self, request, **kwargs):
        otp = request.POST.get('otp')
        phone_number = request.POST.get('phone_number')
        email_id = request.POST.get('email_id')
        if not otp and not email_id and not phone_number :
            return HttpBadRequest("otp and phone_number/email_id required")
        try:
            if phone_number:
                consumer = afterbuy_model.Consumer.objects.get(phone_number
                                                     =phone_number)
                afterbuy_utils.validate_otp(otp, user=consumer.user)

            elif email_id:
                consumer_obj = User.objects.get(email
                                                 =email_id)
                consumer = afterbuy_model.Consumer.objects.get(user
                                                     = consumer_obj)
            afterbuy_utils.validate_otp( otp, user=consumer.user)
            data = {'status': 1, 'message': "valid OTP"}
        except Exception as ex:
                data = {'status': 0, 'message': "invalid OTP"}
                logger.info("[Exception OTP]:{0}".
                            format(ex))
        return HttpResponse(json.dumps(data), content_type="application/json")


class InterestResource(CustomBaseModelResource):

    class Meta:
        queryset = afterbuy_model.Interest.objects.all()
        resource_name = "interest"
        authorization = Authorization()
        detail_allowed_methods = ['get', 'post', 'delete', 'put']
        always_return_data = True
        
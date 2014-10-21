import json
import logging
from django.forms.models import model_to_dict
from django.http.response import HttpResponse
from django.conf.urls import url
from tastypie.http import HttpBadRequest
from tastypie.utils.urls import trailing_slash
from django.contrib.auth.models import User
from django.contrib.auth import  login
from gladminds.core import utils
from gladminds.afterbuy import utils as afterbuy_utils
from gladminds.afterbuy import models as afterbuy_common

from gladminds.core.apis.user_apis import AccessTokenAuthentication
from gladminds import settings
from gladminds.bajaj.services import message_template
from gladminds.core.managers.mail import sent_otp_email
from gladminds.core.apis.base_apis import CustomBaseResource
from gladminds.core.utils import mobile_format, get_task_queue
from django.contrib.auth import authenticate

logger = logging.getLogger("gladminds")


class UserResources(CustomBaseResource):
    class Meta:
        resource_name = 'user'
        authentication = AccessTokenAuthentication()

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/registration%s" % (self._meta.resource_name, trailing_slash()), self.wrap_view('save_user_details'), name="save_user_details"),
            url(r"^(?P<resource_name>%s)/authenticate-email%s" % (self._meta.resource_name, trailing_slash()), self.wrap_view('authenticate_user_email_id'), name="authenticate_user_email_id"),
            url(r"^(?P<resource_name>%s)/send-otp%s" % (self._meta.resource_name, trailing_slash()), self.wrap_view('authenticate_user_send_otp'), name="authenticate_user_send_otp"),
            url(r"^(?P<resource_name>%s)/forgot-password%s" % (self._meta.resource_name, trailing_slash()), self.wrap_view('change_user_password'), name="change_user_password"),
            url(r"^(?P<resource_name>%s)/(?P<user_id>\d+)/details%s" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_user_details'), name="get_user_details"),
            url(r"^(?P<resource_name>%s)/(?P<user_id>\d+)/products%s" % (self._meta.resource_name, trailing_slash()), self.wrap_view('dispatch_dict'), name="api_dispatch_dict"),
            url(r"^(?P<resource_name>%s)/login%s" % (self._meta.resource_name, trailing_slash()), self.wrap_view('auth_login'), name="auth_login"),
        ]

    def save_user_details(self, request, **kwargs):
        phone_number = request.POST.get('phone_number')
        email_id = request.POST.get('email_id')
        name = request.POST.get('name')
        password = request.POST.get('password')
        if not phone_number or not email_id or not name:
            return HttpBadRequest("phone_number, username and password required.")
        try:
            customer_id = utils.generate_unique_customer_id()
            phone_number = mobile_format(phone_number)
            create_user = User.objects.create_user(customer_id,
                                                    email_id, password)
            create_user.save()
            try:
                afterbuy_common.Consumer.objects.get(
                                                phone_number=phone_number)
                data = {'status': 0, 'message': 'already registered'}
            except:
                user_register = afterbuy_common.Consumer(user=create_user,
                            phone_number=phone_number, consumer_id=customer_id)
                user_register.save()
                data = {'status': 1, 'message': 'succefully registerd'}
        except Exception as ex:
            log_message = "unable to save details :{0}".format(ex)
            logger.info(log_message)
            data = {'status': 0, 'message': log_message}
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
            user_info = afterbuy_common.Consumer.objects.get(
                                user__id=customer_id)
            product_info = afterbuy_common.UserProduct.objects.filter(
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
        phone_number = request.POST.get('phone_number')
        if not phone_number:
            return HttpBadRequest("email id is required")
        try:
            phone_number = phone_number
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
            logger.error('Invalid details, mobile {0}'.format(request.POST.get('phone_number', '')))
            data = {'status': 0, 'message': "inavlid phone_number"}
        return HttpResponse(json.dumps(data), content_type="application/json")

    def change_user_password(self, request, **kwargs):
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        if not phone_number and not password:
            return HttpBadRequest("mobile and password required")
        try:
            phone_number = phone_number
            consumer = afterbuy_common.Consumer.objects.filter(phone_number=mobile_format(phone_number))[0]
            user = User.objects.get(id=consumer.user_id)
            user.password = password
            user.save()
            data = {'status': 1, 'message': "password updated successfully"}
        except Exception as ex:
            logger.error('Invalid details, mobile {0}'.format(request.POST.get('phone_number', '')))
            data = {'status': 0, 'message': "inavlid phone_number"}
        return HttpResponse(json.dumps(data), content_type="application/json")

    def get_user_details(self, request, **kwargs):
        customer_id = kwargs['user_id']
        print kwargs
        cosumer_data = {}
        if not id:
            return HttpBadRequest("id is required.")
        try:
            customer_id = int(customer_id)
            consumer_obj = afterbuy_common.Consumer.objects.get(
                                                        user__id=customer_id)
            cosumer_data['username'] = consumer_obj.user.username
            cosumer_data['email'] = consumer_obj.user.email
            cosumer_data['phone_number'] = consumer_obj.phone_number
            cosumer_data['image_url'] = consumer_obj.image_url
            cosumer_data['address'] = consumer_obj.address
            cosumer_data['state'] = consumer_obj.state
            cosumer_data['country'] = consumer_obj.country
            cosumer_data['date_of_birth'] = consumer_obj.date_of_birth
            cosumer_data['accepted_terms'] = consumer_obj.accepted_terms
            cosumer_data['tshirt_size'] = consumer_obj.tshirt_size
        except Exception as ex:
            logger.info("[Exception get_user_product_information]:{0}".format(ex))
            return HttpBadRequest("Not a registered user")
        return HttpResponse(json.dumps(cosumer_data), content_type="application/json")

    def auth_login(self, request, **kwargs):
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        if not phone_number or not password:
            return HttpBadRequest("Phone Number and password  required.")
        phone_number = request.POST['phone_number']
        password = request.POST['phone_number']
        try:
            consumer_obj = afterbuy_common.Consumer.objects.get(phone_number
                                             =mobile_format(phone_number))
            password = request.POST['password']
            user = authenticate(username=consumer_obj.consumer_id,
                                password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    data = {'status': 1, 'message': "login successfully"}
            else:
                data = {'status': 0, 'message': "login unsuccessfully"}
        except Exception as ex:
                data = {'status': 0, 'message': "login unsuccessfully"}
                logger.info("[Exception get_user_login_information]:{0}".
                            format(ex))
        return HttpResponse(json.dumps(data), content_type="application/json")

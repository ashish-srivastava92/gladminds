import logging
import json

from tastypie.constants import ALL_WITH_RELATIONS, ALL
from tastypie.authorization import DjangoAuthorization
from django.contrib.auth.models import User
from django.conf.urls import url
from tastypie.utils.urls import trailing_slash
from tastypie import fields,http
from django.http.response import HttpResponse
from tastypie.http import HttpBadRequest
from django.contrib.auth import authenticate, login
from django.conf import settings
from gladminds.afterbuy import utils as core_utils
from tastypie.authorization import Authorization

from gladminds.core.model_fetcher import models
from gladminds.sqs_tasks import send_otp
from gladminds.core.auth.access_token_handler import create_access_token,\
    delete_access_token
from gladminds.core.apis.base_apis import CustomBaseModelResource
from gladminds.core.apis.authentication import AccessTokenAuthentication
from gladminds.core.apis.authorization import MultiAuthorization
from gladminds.core.cron_jobs.queue_utils import send_job_to_queue
from gladminds.core.auth import otp_handler
from django.contrib.sites.models import RequestSite
from gladminds.core.model_helpers import format_phone_number
from tastypie.exceptions import ImmediateHttpResponse
from gladminds.core.managers.mail import send_reset_link_email
from gladminds.core.loaders.module_loader import get_model

logger = logging.getLogger('gladminds')


class UserResource(CustomBaseModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'users'
        model_name = 'User'
        excludes = ['password', 'is_superuser']
        authorization = Authorization()
#         authentication = AccessTokenAuthentication()
#         authorization = MultiAuthorization(DjangoAuthorization())
        detail_allowed_methods = ['get', 'post', 'put']
        filtering = {
                     "is_active": ALL
                     }
        always_return_data = True


class UserProfileResource(CustomBaseModelResource):
    user = fields.ForeignKey(UserResource, 'user', null=True, blank=True, full=True)

    class Meta:
        queryset = models.UserProfile.objects.all()
        resource_name = 'gm-users'
        model_name = 'UserProfile'
        authorization = Authorization()
#         authorization = MultiAuthorization(DjangoAuthorization())
#         authentication = AccessTokenAuthentication()
        detail_allowed_methods = ['get', 'post', 'put']
        filtering = {
                     "user":  ALL_WITH_RELATIONS,
                     "phone_number": ALL,
                     "state": ALL,
                     "country": ALL,
                     "pincode": ALL
                     }
        always_return_data = True 

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/login%s" % (self._meta.resource_name,
                                                     trailing_slash()),
                self.wrap_view('login'), name="login"),
            url(r"^(?P<resource_name>%s)/activate-email%s" % 
                (self._meta.resource_name, trailing_slash()), 
                self.wrap_view('activate_email'), name="activate_email"),
            url(r"^(?P<resource_name>%s)/authenticate-email%s" % 
                (self._meta.resource_name, trailing_slash()), self.wrap_view
                ('authenticate_user_email_id'),
                 name="authenticate_user_email_id"),
            url(r"^(?P<resource_name>%s)/forgot-password/generate-link%s" % 
                (self._meta.resource_name, trailing_slash()), self.wrap_view
                ('generate_reset_link'), name="generate_reset_link"),
            url(r"^(?P<resource_name>%s)/forgot-password/email%s" % 
                (self._meta.resource_name, trailing_slash()), self.wrap_view
                ('change_user_password'), name="change_user_password"),
            url(r"^(?P<resource_name>%s)/phone-number/send-otp%s" % 
                (self._meta.resource_name, trailing_slash()), self.wrap_view
                ('sent_otp_user_phone_number'),
                 name="sent_otp_user_phone_number"),
            url(r"^(?P<resource_name>%s)/send-otp/forgot-password%s" % 
                (self._meta.resource_name, trailing_slash()), 
                self.wrap_view('authenticate_user_send_otp'), 
                name="authenticate_user_send_otp"),
            url(r"^(?P<resource_name>%s)/validate-otp%s" % 
                (self._meta.resource_name, trailing_slash()), 
                self.wrap_view('validate_otp'), name="validate_otp"),
            url(r"^(?P<resource_name>%s)/logout%s" % (self._meta.resource_name,
                                                      trailing_slash()),
                self.wrap_view('logout'), name="logout")
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
            message = core_utils.get_template('SEND_OTP').format(otp)
            send_job_to_queue(send_otp, {'phone_number':phone_number, 'message':message, 'sms_client':settings.SMS_CLIENT})
            logger.info('OTP sent to mobile {0}'.format(phone_number))
            data = {'status': 1, 'message': "OTP sent_successfully"}

        except Exception as ex:
            logger.error('Invalid details, mobile {0} and exception {1}'.format(request.POST.get('phone_number', ''),ex))
            data = {'status': 0, 'message': ex}
        return HttpResponse(json.dumps(data), content_type="application/json")
    
    def activate_email(self, request, **kwargs):
        activation_key = request.GET['activation_key']
        activated_user = models.EmailToken.objects.activate_user(activation_key)
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
        try:
            load = json.loads(request.body)
        except:
            return HttpResponse(content_type="application/json", status=404)
        email_id = load.get('email')

        if not email_id:
            return HttpBadRequest("email id is required")
        try:
            models.UserProfile.objects.get(user__email=email_id, is_email_verified=True)
            data = {'status': 1, 'message': "email id verified"}
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
                user_obj = models.UserProfile.objects.get(phone_number=phone_number).user
                otp = otp_handler.get_otp(user=user_obj)
                message = core_utils.get_template('SEND_OTP').format(otp)
                send_job_to_queue('send_otp', {'phone_number': phone_number,
                                             'message': message, "sms_client": settings.SMS_CLIENT})
                logger.info('OTP sent to mobile {0}'.format(phone_number))
                data = {'status': 1, 'message': "OTP sent_successfully"}
                #Send email if email address exist
            if email:
                try:
                    user_obj = models.UserProfile.objects.get(user__email=email, is_email_verified=True)
                    site = RequestSite(request)
                    models.EmailToken.objects.create_email_token(user_obj, email, site, trigger_mail='forgot-password')
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
    
    def generate_reset_link(self,request, **kwargs):
        if request.method != 'POST':
            return HttpResponse(json.dumps({"message":"method not allowed"}), content_type="application/json",status=401)
        try:
            load = json.loads(request.body)
        except:
            return HttpResponse(content_type="application/json", status=404)
        email = load.get('email')
        try:
            user_obj = models.UserProfile.objects.get(user__email=email, is_email_verified=True)
        except Exception as ex:
            return HttpBadRequest("Either your email is not verified or its not exist")
        site = RequestSite(request)
        token = get_model('EmailToken').objects.create_email_token(user_obj, email, site, trigger_mail='forgot-password')
        activation_key = token.activation_key
        data = {'status': 1, 'message': "Password reset link sent successfully"}
        return HttpResponse(json.dumps(data), content_type="application/json")
    
    def change_user_password(self, request, **kwargs):
        if request.method != 'POST':
            return HttpResponse(json.dumps({"message":"method not allowed"}), content_type="application/json",status=401)
        try:
            load = json.loads(request.body)
        except:
            return HttpResponse(content_type="application/json", status=404)
        email = load.get('email')
        password = load.get('password1')
        repassword = load.get('password2')
        user_details = {}
        if password != repassword:
            return HttpBadRequest("password1 and password2 not matched")
        try:
            user_obj = models.UserProfile.objects.get(user__email=email, is_email_verified=True)
        except Exception:
            raise ImmediateHttpResponse(
                response=http.HttpBadRequest('invalid authentication key!'))
        user_details['email'] = user_obj.user.email
        user = User.objects.filter(**user_details)[0]
        user.set_password(password)
        user.save()
        data = {'status': 1, 'message': "password updated successfully"}
        return HttpResponse(json.dumps(data), content_type="application/json")

    def login(self, request, **kwargs):
        if request.method != 'POST':
            return HttpResponse(json.dumps({"message":"method not allowed"}), content_type="application/json",status=401)
        try:
            load = json.loads(request.body)
        except:
            return HttpResponse(content_type="application/json", status=404)
        phone_number = load.get('phone_number')
        email_id = load.get('email')
        username = load.get('username')
        password = load.get('password')
        if not phone_number and not email_id and not username:
            return HttpBadRequest("phone_number/email/username required.")
        if phone_number:
            user_obj = models.UserProfile.objects.get(phone_number
                                             =phone_number,is_phone_verified=True).user
        elif email_id:
            user_obj = models.UserProfile.objects.using(settings.BRAND).get(user__email=
                                                                  email_id,is_email_verified=True).user
        elif username:
            user_obj = User.objects.using(settings.BRAND).get(username=
                                                                  username)

        http_host = request.META.get('HTTP_HOST', 'localhost')
        user_auth = authenticate(username=str(user_obj.username),
                            password=password)

        if user_auth is not None:
            access_token = create_access_token(user_auth, http_host)
            if user_auth.is_active:
                login(request, user_auth)
                data = {'status': 1, 'message': "login successfully",
                        'access_token': access_token, "user_id": user_auth.id}
        else:
            data = {'status': 0, 'message': "login unsuccessful"}
        return HttpResponse(json.dumps(data), content_type="application/json")

    def logout(self, request, **kwargs):
        access_token = request.GET.get('access_token')
        try:
            delete_access_token(access_token)
            data = {'status': 0, 'message': "logout successfully"}
        except Exception as ex:
            data = {'status': 0, 'message': "access_token_not_valid"}
            logger.info("[Exception get_user_login_information]:{0}".
                        format(ex))
        return HttpResponse(json.dumps(data), content_type="application/json")


class DealerResource(CustomBaseModelResource):
    user = fields.ForeignKey(UserProfileResource, 'user', full=True)

    class Meta:
        queryset = models.Dealer.objects.all()
        resource_name = "dealers"
        model_name = 'Dealer'
        authentication = AccessTokenAuthentication()
        authorization = MultiAuthorization(DjangoAuthorization())
        detail_allowed_methods = ['get']
        filtering = {
                     "user": ALL_WITH_RELATIONS,
                     "dealer_id": ALL,
                     }
        always_return_data = True


class AuthorizedServiceCenterResource(CustomBaseModelResource):
    user = fields.ForeignKey(UserProfileResource, 'user', full=True)
    dealer = fields.ForeignKey(DealerResource, 'dealer', null=True, blank=True, full=True)

    class Meta:
        queryset = models.AuthorizedServiceCenter.objects.all()
        resource_name = "authorized-service-centers"
        model_name = 'AuthorizedServiceCenter'
        authentication = AccessTokenAuthentication()
        authorization = MultiAuthorization(DjangoAuthorization())
        detail_allowed_methods = ['get']
        filtering = {
                     "user": ALL_WITH_RELATIONS,
                     "asc_id": ALL,
                     "dealer": ALL_WITH_RELATIONS
                     }
        always_return_data = True


class ServiceAdvisorResource(CustomBaseModelResource):
    user = fields.ForeignKey(UserProfileResource, 'user', full=True)
    dealer = fields.ForeignKey(DealerResource, 'dealer', null=True, blank=True, full=True)
    asc = fields.ForeignKey(AuthorizedServiceCenterResource, 'asc', null=True, blank=True, full=True)

    class Meta:
        queryset = models.ServiceAdvisor.objects.all()
        resource_name = "service-advisors"
        model_name = 'ServiceAdvisor'
        authentication = AccessTokenAuthentication()
        authorization = MultiAuthorization(DjangoAuthorization())
        detail_allowed_methods = ['get']
        filtering = {
                     "user": ALL_WITH_RELATIONS,
                     "dealer": ALL_WITH_RELATIONS,
                     "asc": ALL_WITH_RELATIONS,
                     "service_advisor_id": ALL,
                     "status": ALL
                     }
        always_return_data = True
    
class NationalSparesManagerResource(CustomBaseModelResource):
    class Meta:
        queryset = models.NationalSparesManager.objects.all()
        resource_name = "national-spares-managers"
        model_name = 'NationalSparesManager'
        authorization = Authorization()
        detail_allowed_methods = ['get', 'post', 'put']
        always_return_data = True
        
        
class AreaSparesManagerResource(CustomBaseModelResource):
    class Meta:
        queryset = models.AreaSparesManager.objects.all()
        resource_name = "area-spares-managers"
        model_name = 'AreaSparesManager'
        authorization = Authorization()
        detail_allowed_methods = ['get', 'post', 'put']
        always_return_data = True
        
class PartnerResource(CustomBaseModelResource):
    class Meta:
        queryset = models.Partner.objects.all()
        resource_name = "partners"
        model_name = 'Partner'
        authorization = Authorization()
        detail_allowed_methods = ['get', 'post', 'put']
        always_return_data = True


class DistributorResource(CustomBaseModelResource):
    user = fields.ForeignKey(UserProfileResource, 'user', full=True)
    asm = fields.ForeignKey(AreaSparesManagerResource, 'asm', full=True)
    class Meta:
        queryset = models.Distributor.objects.all()
        resource_name = "distributors"
        model_name = 'Distributor'
        authorization = Authorization()
        detail_allowed_methods = ['get', 'post', 'put']
        always_return_data = True


class RetailerResource(CustomBaseModelResource):
    class Meta:
        queryset = models.Retailer.objects.all()
        resource_name = "retailers"
        model_name = 'Retailer'
        authorization = Authorization()
        detail_allowed_methods = ['get', 'post', 'put']
        always_return_data = True

class MemberResource(CustomBaseModelResource):
    distributor = fields.ForeignKey(DistributorResource, 'registered_by_distributor', null=True, blank=True, full=True) 
    preferred_retailer = fields.ForeignKey(RetailerResource, 'preferred_retailer', null=True, blank=True, full=True)
    
    class Meta:
        queryset = models.Mechanic.objects.all()
        resource_name = "members"
        model_name = 'Mechanic'
        authorization = Authorization()
        detail_allowed_methods = ['get', 'post', 'put']
        always_return_data = True
        filtering = {
                     "state": ALL,
                     "locality":ALL,
                     "district":ALL,
                     }


class ServiceDeskUserResource(CustomBaseModelResource):
    '''
    Service Desk User Resource
    '''
    user = fields.ForeignKey(UserProfileResource, 'user_profile',
                                        full=True, null=True, blank=True)
    
    class Meta:
        queryset = models.ServiceDeskUser.objects.all()
        resource_name = "service-desk-users"
        model_name = 'ServiceDeskUser'
#         authorization = MultiAuthorization(DjangoAuthorization())
#         authentication = MultiAuthentication(AccessTokenAuthentication())
        authorization = Authorization()
        detail_allowed_methods = ['get']
        always_return_data = True
        filtering = {
                        "user": ALL_WITH_RELATIONS,
                     }


class DepartmentSubCategoriesResource(CustomBaseModelResource):
    sub_department_user = fields.ToManyField(ServiceDeskUserResource, 'sub_department_user', full=True)

    class Meta:
        queryset = models.DepartmentSubCategories.objects.all()
        resource_name = "department-sub-categories"
        model_name = 'DepartmentSubCategories'
        authorization = Authorization()
        detail_allowed_methods = ['get']
        always_return_data = True
        filtering = { 
                     "department": ALL_WITH_RELATIONS
                     } 


class BrandDepartmentResource(CustomBaseModelResource):
    department_sub_categories = fields.ToManyField(DepartmentSubCategoriesResource, 'department_sub_categories', full=True)
    class Meta:
        queryset = models.BrandDepartment.objects.all()
        resource_name = "brand-departments"
        model_name = 'BrandDepartment'
        authorization = Authorization()
        detail_allowed_methods = ['get']
        always_return_data = True

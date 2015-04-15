from datetime import datetime, timedelta, date
import json
import logging

from django.conf import settings
from django.conf.urls import url
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.db.models.aggregates import Count, Sum
from django.http.response import HttpResponse
from tastypie import fields
from tastypie.utils.urls import trailing_slash
from tastypie import fields,http
from django.http.response import HttpResponse
from tastypie.http import HttpBadRequest
from django.contrib.auth import authenticate, login
from django.conf import settings
from gladminds.afterbuy import utils as core_utils
from tastypie.authorization import Authorization
from tastypie.authorization import DjangoAuthorization
from tastypie.constants import ALL_WITH_RELATIONS, ALL
from tastypie.http import HttpBadRequest
from tastypie.utils.urls import trailing_slash

from gladminds.core import constants
from gladminds.core.apis.authentication import AccessTokenAuthentication
from gladminds.core.apis.authorization import MultiAuthorization, \
     ZSMCustomAuthorization, DealerCustomAuthorization
from gladminds.core.apis.base_apis import CustomBaseModelResource
from gladminds.core.auth.access_token_handler import create_access_token, \
    delete_access_token
from gladminds.core.auth_helper import Roles
from gladminds.core.managers.user_manager import RegisterUser
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
from gladminds.core.utils import get_sql_data
from django.core.serializers.json import DjangoJSONEncoder

logger = logging.getLogger('gladminds')

register_user = RegisterUser()

class UserResource(CustomBaseModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'users'
        excludes = ['password', 'is_superuser']
        authorization = Authorization()
#         authentication = AccessTokenAuthentication()
#         authorization = MultiAuthorization(DjangoAuthorization())
        detail_allowed_methods = ['get', 'post', 'put']
        filtering = {
                     "is_active": ALL,
                     "username" : ALL
                     }
        always_return_data = True
        ordering = ['username', 'email']

class UserProfileResource(CustomBaseModelResource):
    user = fields.ForeignKey(UserResource, 'user', null=True, blank=True, full=True)

    class Meta:
        queryset = models.UserProfile.objects.all()
        resource_name = 'gm-users'
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
        ordering = ['user', 'phone_number']
        
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
        token = models.EmailToken.objects.create_email_token(user_obj, email, site, trigger_mail='forgot-password')
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
            user_groups = []
            for group in request.user.groups.values():
                user_groups.append(group['name'])
            if user_auth.is_active:
                login(request, user_auth)
                data = {'status': 1, 'message': "login successfully",
                        'access_token': access_token, "user_id": user_auth.id, "user_groups" : user_groups}
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

class ZonalServiceManagerResource(CustomBaseModelResource):
    user = fields.ForeignKey(UserProfileResource, 'user', full=True)

    class Meta:
        queryset = models.ZonalServiceManager.objects.all()
        resource_name = "zonal-service-managers"
        authentication = AccessTokenAuthentication()
        authorization = MultiAuthorization(DjangoAuthorization())
        detail_allowed_methods = ['get']
        filtering = {
                     "user": ALL_WITH_RELATIONS,
                     "zsm_id": ALL,
                     }
        always_return_data = True

class AreaServiceManagerResource(CustomBaseModelResource):
    user = fields.ForeignKey(UserProfileResource, 'user', full=True)
    zsm = fields.ForeignKey(ZonalServiceManagerResource, 'zsm', full=True)

    class Meta:
        queryset = models.AreaServiceManager.objects.all()
        resource_name = "area-service-managers"
        authentication = AccessTokenAuthentication()
        authorization = MultiAuthorization(DjangoAuthorization(), ZSMCustomAuthorization())
        detail_allowed_methods = ['get']
        filtering = {
                     "user": ALL_WITH_RELATIONS,
                     "asm_id": ALL, 
                     "zsm": ALL_WITH_RELATIONS,
                     }
        always_return_data = True


class DealerResource(CustomBaseModelResource):
    user = fields.ForeignKey(UserProfileResource, 'user', full=True)
    asm = fields.ForeignKey(AreaServiceManagerResource, 'asm', full=True)
    
    class Meta:
        queryset = models.Dealer.objects.all()
        resource_name = "dealers"
        authentication = AccessTokenAuthentication()
        authorization = MultiAuthorization(DjangoAuthorization(), DealerCustomAuthorization())
        detail_allowed_methods = ['get', 'post']
        filtering = {
                     "user": ALL_WITH_RELATIONS,
                     "dealer_id": ALL,
                     "asm":ALL_WITH_RELATIONS,
                     }
        always_return_data = True
        ordering = ['user']
        
    def prepend_urls(self):
        return [
                 url(r"^(?P<resource_name>%s)/register%s" % (self._meta.resource_name,trailing_slash()),
                     self.wrap_view('register_dealer'), name="register_dealer"),
                url(r"^(?P<resource_name>%s)/active%s" % (self._meta.resource_name,trailing_slash()),
                                                        self.wrap_view('get_active_dealer'), name="get_active_dealer"),
                ]
    
    
    def register_dealer(self, request, **kwargs):
        if request.method != 'POST':
            return HttpResponse(json.dumps({"message" : "Method not allowed"}), content_type= "application/json",
                                status=401)
        try:
            load = json.loads(request.body)
        except:
            return HttpResponse(content_type="application/json", status=404)
        username = load.get('username')
        phone_number = load.get('phone-number')
        email = load.get('email')
        try:
            user = models.Dealer.objects.get(user__phone_number=phone_number, dealer_id=username)
            data = {'status': 0 , 'message' : 'Dealer with this id or phone number already exists'}

        except Exception as ex:
            logger.info("Exception while registering dealer {0}".format(ex))
            user_data = register_user.register_user(Roles.DEALERS,username=username,
                                             phone_number=phone_number,
                                             email = email, APP=settings.BRAND)
            dealer_data = models.Dealer(dealer_id=username, user=user_data)
            dealer_data.save()
            data = {"status": 1 , "message" : "Dealer registered successfully"}

        return HttpResponse(json.dumps(data), content_type="application/json")
    
    def get_active_dealer(self, request, **kwargs):
        print request.GET
        result = []
        active_today = models.Dealer.objects.filter(last_transaction_date__startswith=date.today()).count()
        today = {}
        today['count_on'] = 'Today'
        today['active'] = active_today
        result.append(today)
        try:
            load = request.GET
        except Exception as ex:
            return HttpResponse(content_type="application/json", status=404)
        
#         month = load.get('month', None)
#         year = load.get('year', None)
#         if month and year:
#             actual = str(year) + "-" + str(month) + "%"
#             active_count = get_sql_data("select count(*) as cnt from gm_dealer where last_transaction_date\
#              like '%s' " %actual)
# #             active_count = models.Dealer.objects.filter(last_transaction_date__year=year,
# #                                                         last_transaction_date__month=month).count()
        return HttpResponse(content=json.dumps(result), 
                            content_type='application/json')
    
class AuthorizedServiceCenterResource(CustomBaseModelResource):
    user = fields.ForeignKey(UserProfileResource, 'user', full=True)
    dealer = fields.ForeignKey(DealerResource, 'dealer', null=True, blank=True, full=True)

    class Meta:
        queryset = models.AuthorizedServiceCenter.objects.all()
        resource_name = "authorized-service-centers"
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
        authorization = Authorization()
        detail_allowed_methods = ['get', 'post', 'put']
        always_return_data = True
        
        
class AreaSparesManagerResource(CustomBaseModelResource):
    class Meta:
        queryset = models.AreaSparesManager.objects.all()
        resource_name = "area-spares-managers"
        authorization = Authorization()
        detail_allowed_methods = ['get', 'post', 'put']
        always_return_data = True
        
class PartnerResource(CustomBaseModelResource):
    class Meta:
        queryset = models.Partner.objects.all()
        resource_name = "partners"
        authorization = Authorization()
        detail_allowed_methods = ['get', 'post', 'put']
        always_return_data = True


class DistributorResource(CustomBaseModelResource):
    user = fields.ForeignKey(UserProfileResource, 'user', full=True)
    asm = fields.ForeignKey(AreaSparesManagerResource, 'asm', full=True)
    class Meta:
        queryset = models.Distributor.objects.all()
        resource_name = "distributors"
        authorization = Authorization()
        detail_allowed_methods = ['get', 'post', 'put']
        always_return_data = True


class RetailerResource(CustomBaseModelResource):
    class Meta:
        queryset = models.Retailer.objects.all()
        resource_name = "retailers"
        authorization = Authorization()
        detail_allowed_methods = ['get', 'post', 'put']
        always_return_data = True

class MemberResource(CustomBaseModelResource):
    distributor = fields.ForeignKey(DistributorResource, 'registered_by_distributor', null=True, blank=True, full=True) 
    preferred_retailer = fields.ForeignKey(RetailerResource, 'preferred_retailer', null=True, blank=True, full=True)
    
    class Meta:
        queryset = models.Member.objects.all()
        resource_name = "members"
        authorization = Authorization()
        authentication = AccessTokenAuthentication()
        detail_allowed_methods = ['get', 'post', 'put']
        always_return_data = True
        args = constants.LOYALTY_ACCESS
        filtering = {
                     "state": ALL,
                     "locality":ALL,
                     "district":ALL,
                     }
        
    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/active%s" % (self._meta.resource_name,
                                                     trailing_slash()),
                self.wrap_view('get_active_member'), name="get_active_member"),
            url(r"^(?P<resource_name>%s)/points%s" % (self._meta.resource_name,
                                                     trailing_slash()),
                self.wrap_view('get_total_points'), name="get_total_points"),
        ]
   
    def get_role_access_query(self, user, area, args):
        if user.groups.filter(name=Roles.AREASPARESMANAGERS).exists():
            asm_state_list=models.AreaSparesManager.objects.get(user__user=user).state.all()
            args[area] = asm_state_list
        elif user.groups.filter(name=Roles.DISTRIBUTORS).exists():
            distributor_city =  models.Distributor.objects.get(user__user=user).city
            args[area] = str(distributor_city)
        return args

    def get_active_member(self, request, **kwargs):
        self.is_authenticated(request)
        args={}
        try:
            load = request.GET
        except Exception as ex:
            return HttpResponse(content_type="application/json", status=404)
        try:
            active_days = load.get('active_days', None)
            if not active_days:
                active_days=30
            if not request.user.is_superuser:
                user_group = request.user.groups.values()[0]['name']
                area = self._meta.args['query_field'][user_group]['area']
                region = self._meta.args['query_field'][user_group]['group_region']
                args = self.get_role_access_query(request.user, area, args)
            registered_member = models.Member.objects.filter(**args).values(region).annotate(count= Count('mechanic_id'))
            args['last_transaction_date__gte']=datetime.now()-timedelta(int(active_days))
            active_member = models.Member.objects.filter(**args).values(region).annotate(count= Count('mechanic_id'))
            member_report={}
            for member in registered_member:
                member_report[member[region]]={}
                member_report[member[region]]['registered_count'] = member['count']
                member_report[member[region]]['active_count']= 0
                active = filter(lambda active: active[region] == member[region], active_member)
                if active:
                    member_report[member[region]]['active_count']= active[0]['count']
        except Exception as ex:
            logger.error('Active member count requested by {0}:: {1}'.format(request.user, ex))
            member_report = {'status': 0, 'message': 'could not retrieve the count of active members'}
        return HttpResponse(json.dumps(member_report), content_type="application/json")

    def get_total_points(self, request, **kwargs):
        self.is_authenticated(request)
        args={}
        try:
            load = request.GET
        except Exception as ex:
            return HttpResponse(content_type="application/json", status=404)
        try:
            if not request.user.is_superuser:
                user_group = request.user.groups.values()[0]['name']
                area = 'member__' + self._meta.args['query_field'][user_group]['area']
                region = 'member__' + self._meta.args['query_field'][user_group]['group_region']
                args = self.get_role_access_query(request.user, area, args)
            total_redeem_points = models.RedemptionRequest.objects.filter(**args).values(region).annotate(sum=Sum('points'))
            total_accumulate_points = models.AccumulationRequest.objects.filter(**args).values(region).annotate(sum=Sum('points'))
            member_report={}
            for region_point in total_redeem_points:
                member_report[region_point[region]]={}
                member_report[region_point[region]]['total_redeem'] = region_point['sum']
                member_report[region_point[region]]['total_accumulate'] = 0
                active = filter(lambda active: active[region] == region_point[region], total_accumulate_points)
                if active:
                    member_report[region_point[region]]['total_accumulate']= active[0]['sum']
        except Exception as ex:
            logger.error('redemption/accumulation request count requested by {0}:: {1}'.format(request.user, ex))
            member_report = {'status': 0, 'message': 'could not retrieve the sum of points of requests'}
        return HttpResponse(json.dumps(member_report), content_type="application/json")

class BrandDepartmentResource(CustomBaseModelResource):
    class Meta:
        queryset = models.BrandDepartment.objects.all()
        resource_name = "brand-departments"
        authorization = Authorization()
        detail_allowed_methods = ['get']
        always_return_data = True
        filtering = {
                     "id" : ALL
                     }


class DepartmentSubCategoriesResource(CustomBaseModelResource):
    department = fields.ForeignKey(BrandDepartmentResource, 'department', full=True, null=True, blank=True)

    class Meta:
        queryset = models.DepartmentSubCategories.objects.all()
        resource_name = "department-sub-categories"
        authorization = Authorization()
        detail_allowed_methods = ['get']
        always_return_data = True
        filtering = { 
                     "department": ALL_WITH_RELATIONS,
                     "id" : ALL
                     } 


class ServiceDeskUserResource(CustomBaseModelResource):
    '''
    Service Desk User Resource
    '''
    user = fields.ForeignKey(UserProfileResource, 'user_profile',
                                        full=True, null=True, blank=True)
    sub_department = fields.ForeignKey(DepartmentSubCategoriesResource, 'sub_department',
                                       full=True, null=True, blank=True)

    class Meta:
        queryset = models.ServiceDeskUser.objects.all()
        resource_name = "service-desk-users"
#         authorization = MultiAuthorization(DjangoAuthorization())
#         authentication = MultiAuthentication(AccessTokenAuthentication())
        authorization = Authorization()
        detail_allowed_methods = ['get']
        always_return_data = True
        filtering = {
                        "user": ALL_WITH_RELATIONS,
                        "sub_department" : ALL_WITH_RELATIONS,
                        "id" : ALL
                     }


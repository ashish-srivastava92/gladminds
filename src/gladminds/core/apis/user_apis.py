from datetime import datetime, timedelta
import json
import logging

from django.conf import settings
from django.conf.urls import url
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.db.models.aggregates import Count, Sum
from django.http.response import HttpResponse
from tastypie import fields
from tastypie.authorization import Authorization
from tastypie.authorization import DjangoAuthorization
from tastypie.constants import ALL_WITH_RELATIONS, ALL
from tastypie.http import HttpBadRequest
from tastypie.utils.urls import trailing_slash

from gladminds.core import constants
from gladminds.core.apis.authentication import AccessTokenAuthentication
from gladminds.core.apis.authorization import MultiAuthorization
from gladminds.core.apis.base_apis import CustomBaseModelResource
from gladminds.core.auth.access_token_handler import create_access_token, \
    delete_access_token
from gladminds.core.auth_helper import Roles
from gladminds.core.managers.user_manager import RegisterUser
from gladminds.core.model_fetcher import models


logger = logging.getLogger('gladminds')

register_user = RegisterUser()

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
            url(r"^(?P<resource_name>%s)/logout%s" % (self._meta.resource_name,
                                                      trailing_slash()),
                self.wrap_view('logout'), name="logout")
        ]

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
                                             =phone_number).user
        elif email_id:
            user_obj = User.objects.using(settings.BRAND).get(email=
                                                                  email_id)
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
        detail_allowed_methods = ['get', 'post']
        filtering = {
                     "user": ALL_WITH_RELATIONS,
                     "dealer_id": ALL,
                     }
        always_return_data = True

    def prepend_urls(self):
        return [
                 url(r"^(?P<resource_name>%s)/register%s" % (self._meta.resource_name,trailing_slash()),
                     self.wrap_view('register_dealer'), name="register_dealer")]
    
    
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
        queryset = models.Member.objects.all()
        resource_name = "members"
        model_name = 'Member'
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
   
    def get_active_member(self, request, **kwargs):
        print self.is_authenticated(request)
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
                if request.user.groups.filter(name=Roles.AREASPARESMANAGERS).exists():
                    asm_state_list=models.AreaSparesManager.objects.get(user__user=request.user).state.all()
                    args[area] = asm_state_list
                elif request.user.groups.filter(name=Roles.DISTRIBUTORS).exists():
                    distributor_city =  models.Distributor.objects.get(user__user=request.user).city
                    args[area] = str(distributor_city)
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
            logger.error('redemption request count requested by {0}:: {1}'.format(request.user, ex))
            data = {'status': 0, 'message': 'could not retrieve the count of redemption request'}
        return HttpResponse(json.dumps(member_report), content_type="application/json")

    def get_total_points(self, request, **kwargs):
        print self.is_authenticated(request)
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
                region = 'member__' + self._meta.args['query_field'][user_group]['group_region']
                if request.user.groups.filter(name=Roles.AREASPARESMANAGERS).exists():
                    asm_state_list=models.AreaSparesManager.objects.get(user__user=request.user).state.all()
                    args[area] = asm_state_list
                elif request.user.groups.filter(name=Roles.DISTRIBUTORS).exists():
                    distributor_city =  models.Distributor.objects.get(user__user=request.user).city
                    args[area] = str(distributor_city)
            total_redeem_points = models.RedemptionRequest.objects.filter(**args).values(region).annotate(sum=Sum('points'))
            total_accumulate_list = models.AccumulationRequest.objects.filter(**args).values(region).annotate(sum=Sum('points'))
            member_report={}
#             for region_point in total_redeem_points:
#                 member_report[region_point[region]]={}
#                 member_report[region_point[region]]['sum'] = region_point['sum']
#                 active = filter(lambda active: active[region] == region_point[region], total_accumulate_list)
#                 if active:
#                     member_report[member[region]]['active_count']= active[0]['count']
        except Exception as ex:
            logger.error('redemption request count requested by {0}:: {1}'.format(request.user, ex))
            data = {'status': 0, 'message': 'could not retrieve the count of redemption request'}
        return HttpResponse(json.dumps(member_report), content_type="application/json")

class BrandDepartmentResource(CustomBaseModelResource):
    class Meta:
        queryset = models.BrandDepartment.objects.all()
        resource_name = "brand-departments"
        model_name = 'BrandDepartment'
        authorization = Authorization()
        detail_allowed_methods = ['get']
        always_return_data = True


class DepartmentSubCategoriesResource(CustomBaseModelResource):
    department = fields.ForeignKey(BrandDepartmentResource, 'department', full=True, null=True, blank=True)

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
        model_name = 'ServiceDeskUser'
#         authorization = MultiAuthorization(DjangoAuthorization())
#         authentication = MultiAuthentication(AccessTokenAuthentication())
        authorization = Authorization()
        detail_allowed_methods = ['get']
        always_return_data = True
        filtering = {
                        "user": ALL_WITH_RELATIONS,
                        "sub_department" : ALL_WITH_RELATIONS
                     }


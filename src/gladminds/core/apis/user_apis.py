import logging
import json

from tastypie.constants import ALL_WITH_RELATIONS, ALL
from tastypie.authorization import DjangoAuthorization
from django.contrib.auth.models import User
from django.conf.urls import url
from tastypie.utils.urls import trailing_slash
from tastypie import fields
from django.http.response import HttpResponse
from tastypie.http import HttpBadRequest
from django.contrib.auth import authenticate, login
from django.conf import settings
from tastypie.authorization import Authorization

from gladminds.core.model_fetcher import models
from gladminds.core.auth.access_token_handler import create_access_token,\
    delete_access_token
from gladminds.core.apis.base_apis import CustomBaseModelResource
from gladminds.core.apis.authentication import AccessTokenAuthentication
from gladminds.core.apis.authorization import MultiAuthorization

logger = logging.getLogger('gladminds')


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
                     "is_active": ALL
                     }
        always_return_data = True


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

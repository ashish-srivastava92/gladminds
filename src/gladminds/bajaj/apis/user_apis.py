from tastypie.authorization import Authorization, DjangoAuthorization
from tastypie import fields
from tastypie.constants import ALL_WITH_RELATIONS, ALL

from gladminds.bajaj import models
from gladminds.core.apis.base_apis import CustomBaseModelResource
from gladminds.core.apis.user_apis import UserProfileResource, UserResource
from gladminds.core.apis.authorization import MultiAuthorization
from gladminds.core.apis.authentication import AccessTokenAuthentication
from gladminds.bajaj.apis.authorization import CustomAuthorization


class UserProfileResource(UserProfileResource):
    user = fields.ForeignKey(UserResource, 'user', null=True, blank=True, full=True)

    class Meta:
        queryset = models.UserProfile.objects.all()
        resource_name = 'gm-users'
        authorization = MultiAuthorization(DjangoAuthorization(),
                                           CustomAuthorization())
        authentication = AccessTokenAuthentication()
        detail_allowed_methods = ['get']
        filtering = {
                     "user":  ALL_WITH_RELATIONS,
                     "phone_number": ALL
                     }
        always_return_data = True


class DealerResources(CustomBaseModelResource):
    class Meta:
        queryset = models.Dealer.objects.all()
        resource_name = "dealers"
        authorization = Authorization()
        detail_allowed_methods = ['get', 'post', 'delete']
        always_return_data = True


class AuthorizedServiceCenterResources(CustomBaseModelResource):
    class Meta:
        queryset = models.AuthorizedServiceCenter.objects.all()
        resource_name = "authorized-service-centers"
        authorization = Authorization()
        detail_allowed_methods = ['get', 'post', 'delete']
        always_return_data = True


class ServiceAdvisorResources(CustomBaseModelResource):
    class Meta:
        queryset = models.ServiceAdvisor.objects.all()
        resource_name = "service-advisors"
        authorization = Authorization()
        detail_allowed_methods = ['get', 'post', 'delete']
        always_return_data = True

from tastypie.authorization import Authorization
from gladminds.bajaj.models import ServiceAdvisor, Dealer,\
    UserProfile, AuthorizedServiceCenter
from gladminds.core.apis.base_apis import CustomBaseModelResource


class UserProfileResource(CustomBaseModelResource):
    class Meta:
        queryset = UserProfile.objects.all()
        resource_name = "user_profile"
        authorization = Authorization()
        detail_allowed_methods = ['get', 'post', 'delete']
        always_return_data = True


class DealerResources(CustomBaseModelResource):
    class Meta:
        queryset = Dealer.objects.all()
        resource_name = "dealers"
        authorization = Authorization()
        detail_allowed_methods = ['get', 'post', 'delete']
        always_return_data = True


class AuthorizedServiceCenterResources(CustomBaseModelResource):
    class Meta:
        queryset = AuthorizedServiceCenter.objects.all()
        resource_name = "authorized-service-centers"
        authorization = Authorization()
        detail_allowed_methods = ['get', 'post', 'delete']
        always_return_data = True


class ServiceAdvisorResources(CustomBaseModelResource):
    class Meta:
        queryset = ServiceAdvisor.objects.all()
        resource_name = "service-advisors"
        authorization = Authorization()
        detail_allowed_methods = ['get', 'post', 'delete']
        always_return_data = True

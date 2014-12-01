from tastypie.constants import ALL_WITH_RELATIONS, ALL
from tastypie.authorization import Authorization
from django.contrib.auth.models import User

from gladminds.core.apis.base_apis import CustomBaseResource
from gladminds.default.models import GladmindsUser


class UserResource(CustomBaseResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'users'
        excludes = ['password']
        authorization = Authorization()
        detail_allowed_methods =['get', 'post', 'put', 'delete']
        always_return_data = True


class GladMindUserResources(CustomBaseResource):
#     user = fields.OneToOneField(User, 'user', full=True)
    class Meta:
        queryset = GladmindsUser.objects.all()
        resource_name = 'gmusers'
        authorization = Authorization()
        detail_allowed_methods = ['get', 'post', 'put', 'delete']
        filtering = {
                     "user":  ALL_WITH_RELATIONS,
                     "phone_number" : ALL
                     }
        always_return_data = True

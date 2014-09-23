from tastypie.constants import ALL_WITH_RELATIONS, ALL
from tastypie.authorization import Authorization
from tastypie import fields 
from django.contrib.auth.models import User
from gladminds.models import common
from gladminds.apis.baseresource import CustomBaseResource

class UserResource(CustomBaseResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'users'
        excludes = ['password']
        authorization= Authorization()
        detail_allowed_methods =['get', 'post', 'put', 'delete']
        always_return_data = True
        
     
class UserProfileResources(CustomBaseResource):
    user = fields.OneToOneField(UserResource, 'user', full=True)
    class Meta:
        queryset = common.UserProfile.objects.all()
        resource_name = 'userprofile'
        authorization= Authorization()
        detail_allowed_methods =['get', 'post', 'put', 'delete']
        always_return_data = True
        filtering = {
                     "user":  ALL_WITH_RELATIONS
                     }
        always_return_data = True


class GladMindUserResources(CustomBaseResource):
    user = fields.OneToOneField(UserProfileResources, 'user', full=True)
    class Meta:
        queryset = common.GladMindUsers.objects.all()
        resource_name = 'gmusers'
        authorization= Authorization()
        detail_allowed_methods = ['get', 'post', 'put', 'delete']
        filtering = {
                     "user":  ALL_WITH_RELATIONS,
                     "customer_name" : ALL,
                     "phone_number" : ALL
                     }
        always_return_data = True

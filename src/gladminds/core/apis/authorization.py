from tastypie.authorization import Authorization
from tastypie.exceptions import Unauthorized
from provider.oauth2.models import AccessToken
from django.conf import settings

from gladminds.afterbuy import models as afterbuy
from gladminds.core.auth_helper import Roles
from gladminds.bajaj import models
import operator
from django.db.models.query_utils import Q

class CustomAuthorization(Authorization):

    def read_list(self, object_list, bundle):
        user = bundle.request.user
        # This assumes a ``QuerySet`` from ``ModelResource``
        if len(object_list)>0:
            if hasattr(object_list[0], 'consumer'):
                return object_list.filter(consumer__user=user)
            elif hasattr(object_list[0], 'user'):
                return object_list.filter(user=user)
            elif hasattr(object_list[0], 'product'):
                return object_list.filter(product__consumer__user=user)
        else:
            return object_list

    def read_detail(self, object_list, bundle):
        if self.read_list(object_list, bundle):
            return True

    def create_detail(self, object_list, bundle):
        data = bundle.obj.__dict__
        try:
            access_token_container = bundle.request.GET.urlencode().split('access_token=')[1]
            key = access_token_container.split('&')[0]
        except:
            key = bundle.request.META.get('HTTP_ACCESS_TOKEN')
        if  (settings.ENV in settings.IGNORE_ENV and key in settings.HARCODED_TOKEN):
                return True
        try:
            authorization = AccessToken.objects.filter(token=key)[0]
        except:
            raise Unauthorized("You are not allowed to access that data.")
        user_id = int(authorization.user.id)
        if data.get('consumer_id'):
            try:
                update_obj = afterbuy.Consumer.objects.get(user=int(data['consumer_id']))
            except:
                raise Unauthorized("You are not allowed to access that data.")
            if user_id == update_obj.user.id:
                return True
            raise Unauthorized("You are not allowed to access that data.")
        if bundle.obj.__dict__.get('product_id'):
            try:
                update_obj = afterbuy.UserProduct.objects.get(id=int(data['product_id']))
            except Exception as ex:
                raise Unauthorized("You are not allowed to access that data.")
            if user_id == update_obj.consumer.user.id:
                return True
            raise Unauthorized("You are not allowed to access that data.")
        return True

    def update_detail(self, object_list, bundle):
        self.authorize_user(object_list, bundle)
        return True

    def delete_detail(self, object_list, bundle):
        self.authorize_user(object_list, bundle)
        return True

    def authorize_user(self, object_list, bundle):
        data = bundle.obj.__dict__
        klass = bundle.obj.__class__
        try:
            access_token_container = bundle.request.GET.urlencode().split('access_token=')[1]
            key = access_token_container.split('&')[0]
        except:
            key = bundle.request.META.get('HTTP_ACCESS_TOKEN')

        if (settings.ENV in settings.IGNORE_ENV and key in settings.HARCODED_TOKEN):
            return True
        try:
            authorization = AccessToken.objects.filter(token=key)[0]
        except:
            raise Unauthorized("You are not allowed to access that data.")
        user_id = int(authorization.user.id)
        klass = bundle.obj.__class__
        if klass._meta.module_name == 'consumer':
            if user_id == data['user_id']:
                update_obj = klass.objects.get(user__id=user_id)
                return True
            raise Unauthorized("You are not allowed to access that data.")
        if bundle.obj.__dict__.get('consumer_id'):
            try:
                update_obj = klass.objects.get(id=int(data['id']))
            except:
                raise Unauthorized("You are not allowed to access that data.")
            if user_id == update_obj.consumer.user.id:
                return True
            raise Unauthorized("You are not allowed to access that data.")
        if bundle.obj.__dict__.get('product_id'):
            try:
                update_obj = klass.objects.get(id=int(data['id']))
            except:
                raise Unauthorized("You are not allowed to access that data.")
            if user_id == update_obj.product.consumer.user.id:
                return True
            raise Unauthorized("You are not allowed to access that data.")


class MultiAuthorization(Authorization):
    def __init__(self, *args, **kwargs):
        self.authorizers = args

    def read_list(self, object_list, bundle):
        for authorizer in self.authorizers:
            if object_list is []:
                return []
            object_list = authorizer.read_list(object_list, bundle)
        return object_list

    def read_detail(self, object_list, bundle):
        for authorizer in self.authorizers:
            klass = authorizer.read_detail(object_list, bundle)
            if klass is False:
                raise Unauthorized("You are not allowed to access that resource.")
        return True

    def create_list(self, object_list, bundle):
        for authorizer in self.authorizers:
            if object_list is []:
                return []
            object_list = authorizer.create_list(object_list, bundle)
        return object_list

    def create_detail(self, object_list, bundle):
        for authorizer in self.authorizers:
            klass = authorizer.create_detail(object_list, bundle)
            if klass is False:
                raise Unauthorized("You are not allowed to access that resource.")
        return True

    def update_list(self, object_list, bundle):
        for authorizer in self.authorizers:
            if object_list is []:
                return []
            object_list = authorizer.update_list(object_list, bundle)
        return object_list

    def update_detail(self, object_list, bundle):
        for authorizer in self.authorizers:
            klass = authorizer.update_detail(object_list, bundle)
            if klass is False:
                raise Unauthorized("You are not allowed to access that resource.")
        return True

    def delete_list(self, object_list, bundle):
        for authorizer in self.authorizers:
            if object_list is []:
                return []
            object_list = authorizer.delete_list(object_list, bundle)
        return object_list

    def delete_detail(self, object_list, bundle):
        for authorizer in self.authorizers:
            klass = authorizer.delete_detail(object_list, bundle)
            if klass is False:
                raise Unauthorized("You are not allowed to access that resource.")
        return True


class LoyaltyCustomAuthorization():

    def __init__(self, display_field=None, query_field=None):
        self.display_field = display_field
        self.query_field = query_field
        
    def read_list(self, object_list, bundle):  
        user = bundle.request.user
        user_name = user.groups.values()[0]['name']    
        klass_name = bundle.obj.__class__._meta.module_name
        
        try:
            ''' filter the object list based on query defined for specific Role'''
            query = self.query_field[user_name]
            query.setdefault('query', [])
            query.setdefault('user_name', None)
            query.setdefault('user', None)
            
            if query:
                q_object = Q()
                if query['user_name']:
                    q_object.add(query['user_name'], user.username)
                    query['query'].append(q_object)
                if query['user']:
                    q_object.add(query['user'], user)
                    query['query'].append(q_object)
                object_list = object_list.filter(reduce(operator.and_, query['query']))
        except:
            if klass_name == 'redemptionrequest' and user.groups.filter(name=Roles.AREASPARESMANAGERS).exists():
                asm_state_list= models.AreaSparesManager.objects.get(user__user= user).state.all()
                object_list=object_list.filter(member__state__in=asm_state_list)            

        try:
            ''' hides the fields in object_list '''            
            if self.display_field:
                for obj in object_list:
                    for x in self.display_field[user_name]:
                        delattr(obj, x)
            return object_list
        except:
            return object_list
        
    def read_detail(self, object_list, bundle):
        if self.read_list(object_list, bundle):
            return True
    
    def create_detail(self, object_list, bundle):
        return True

    def update_detail(self, object_list, bundle):
        return True

    def delete_detail(self, object_list, bundle):
        return True

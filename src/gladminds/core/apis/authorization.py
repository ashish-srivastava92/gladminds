from tastypie.authorization import DjangoAuthorization, Authorization
from tastypie.exceptions import Unauthorized
from provider.oauth2.models import AccessToken
from django.conf import settings

from gladminds.afterbuy import models as afterbuy


class CustomAuthorization(DjangoAuthorization):

    def base_checks(self, request, model_klass):
        # If it doesn't look like a model, we can't check permissions.
        if not model_klass or not getattr(model_klass, '_meta', None):
            return False

        # User must be logged in to check permissions.
#         if not hasattr(request, 'user'):
#             return False

        return model_klass
    def read_list(self, object_list, bundle):
        try:
            access_token_container = bundle.request.GET.urlencode().split('access_token=')[1]
            key = access_token_container.split('&')[0]
        except:
            key = bundle.request.META.get('HTTP_ACCESS_TOKEN')
        if  (settings.ENV in ["dev", "local"] and key in settings.HARCODED_TOKEN):
                return True
        try:
            authorization = AccessToken.objects.filter(token=key)[0]
        except:
                raise Unauthorized("You are not allowed to access that data.")
        user = authorization.user
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
                    
 
    def create_detail(self, object_list, bundle):
        data = bundle.obj.__dict__
        klass = self.base_checks(bundle.request, bundle.obj.__class__)
        if klass is False:
            raise Unauthorized("You are not allowed to access that resource.")
        try:
            access_token_container = bundle.request.GET.urlencode().split('access_token=')[1]
            key = access_token_container.split('&')[0]
        except:
            key = bundle.request.META.get('HTTP_ACCESS_TOKEN')
        if  (settings.ENV in ["dev", "local"] and key in settings.HARCODED_TOKEN):
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
        klass = self.base_checks(bundle.request, bundle.obj.__class__)
        if klass is False:
            raise Unauthorized("You are not allowed to access that resource.")
        try:
            access_token_container = bundle.request.GET.urlencode().split('access_token=')[1]
            key = access_token_container.split('&')[0]
        except:
            key = bundle.request.META.get('HTTP_ACCESS_TOKEN')

        if (settings.ENV in ["dev", "local"] and key in settings.HARCODED_TOKEN):
                return True
        try:
            authorization = AccessToken.objects.filter(token=key)[0]
        except:
                raise Unauthorized("You are not allowed to access that data.")
        user_id = int(authorization.user.id)
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


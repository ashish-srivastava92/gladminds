from tastypie.authorization import DjangoAuthorization
from tastypie.exceptions import Unauthorized
from provider.oauth2.models import AccessToken
from gladminds.afterbuy import models as afterbuy
from django.conf import settings

class CustomAuthorization(DjangoAuthorization):
    
    def base_checks(self, request, model_klass):
        # If it doesn't look like a model, we can't check permissions.
        if not model_klass or not getattr(model_klass, '_meta', None):
            return False

        # User must be logged in to check permissions.
#         if not hasattr(request, 'user'):
#             return False

        return model_klass

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

    def read_detail(self, object_list, bundle):
        self.authorize_user(object_list, bundle)
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
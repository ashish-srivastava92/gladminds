# from django.db.utils import IntegrityError
# from django.db import transaction
# from tastypie import fields, http
# from tastypie.bundle import Bundle
# from tastypie.authorization import Authorization
# from tastypie.exceptions import ImmediateHttpResponse
# from tastypie.authentication import SessionAuthentication
#  
# from gladminds.apis.api_resource import GladMindsResource, GladMindsObject
# from gladminds.managers.common_orm import get_preferences_list,\
#     update_preference, delete_preference, get_preference, save_preference,\
#     update_app_preference, delete_app_preference, get_app_preferences_list,\
#     get_app_preference, save_app_preference
#  
# class UserPreferencesResource(GladMindsResource):
#     id = fields.IntegerField(attribute="id")
#     user_profile = fields.IntegerField(attribute="user_profile")
#     key = fields.CharField(attribute='key')
#     value = fields.CharField(attribute='value', null=True)
#     """
#     It is a preferences resource
#     """
#     class Meta:
#         resource_name = 'user-preferences'
#         authorization = Authorization()
#         object_class = GladMindsObject
#  
#     def detail_uri_kwargs(self, bundle_or_obj):
#         """
#         Overriding the details_uri_kwargs and setting kwargs to Null
#         It will be using for POST methods
#         """
#         kwargs = {}
#  
#         if isinstance(bundle_or_obj, Bundle):
#             kwargs['pk'] = bundle_or_obj.obj.id
#         else:
#             kwargs['pk'] = bundle_or_obj.id
#         return kwargs
#  
#     def obj_update(self, bundle, **kwargs):
#         filters = {}
#         if hasattr(bundle.request, 'GET'):
#             filters = bundle.request.GET.copy()
#         q = filters.get('user_profile', None)
#         preference_key = kwargs["pk"]
#         data = bundle.data
#         data['key'] = preference_key
#         data['user_profile'] = q
#         update_preference(bundle.data, preference_key, q)
#  
#     def obj_delete(self, bundle, **kwargs):
#         preference_id = kwargs["pk"]
#         delete_preference(preference_id)
#  
#     def get_object_list(self, request):
#         filters = {}
#         if hasattr(request, 'GET'):
#             filters = request.GET.copy()
#         q = filters.get('user_profile', None)
#         data = get_preferences_list(user_profile=q)
#         return map(GladMindsObject, data)
#  
#     def obj_get_list(self, bundle, **kwargs):
#         return self.get_object_list(bundle.request)
#  
#     def obj_get(self, bundle, **kwargs):
#         filters = {}
#         if hasattr(bundle.request, 'GET'):
#             filters = bundle.request.GET.copy()
#         q = filters.get('user_profile', None)
#         # We can use select_related it will solve the performance issue
#         serialized_obj = get_preference(kwargs["pk"], q)
#         return GladMindsObject(serialized_obj)
#  
#     @transaction.atomic
#     def save_preferences(self, bundle, **kwargs):
#         """
#         This saves the preferences
#         """
#         data = bundle.data
#         try:
#             if data['key'].find(' ') != -1:
#                 raise ImmediateHttpResponse(
#                 response=http.HttpBadRequest('key cannot have blank spaces!'))
#         except Exception as e:
#             raise ImmediateHttpResponse(
#                 response=http.HttpBadRequest('Key is missing!'))
#         try:
#             save_preference(data)
#         except IntegrityError as e:
#             raise ImmediateHttpResponse(
#                 response=http.HttpBadRequest(e.message))
#         except Exception as e:
#             raise Exception()
#  
#     def obj_create(self, bundle, **kwargs):
#         """
#         Overriding the obj_create
#         """
#         self.save_preferences(bundle, **kwargs)
#         return bundle
#      
# class AppPreferencesResource(GladMindsResource):
#     """
#     It is a preferences resource
#     """
#     id = fields.IntegerField(attribute="id")
#     brand = fields.IntegerField(attribute="brand")
#     key = fields.CharField(attribute='key')
#     value = fields.CharField(attribute='value', null=True)
#  
#     class Meta:
#         resource_name = 'app-preferences'
#         authorization = Authorization()
#         object_class = GladMindsObject
#  
#     def detail_uri_kwargs(self, bundle_or_obj):
#         """
#         Overriding the details_uri_kwargs and setting kwargs to Null
#         It will be using for POST methods
#         """
#         kwargs = {}
#  
#         if isinstance(bundle_or_obj, Bundle):
#             kwargs['pk'] = bundle_or_obj.obj.id
#         else:
#             kwargs['pk'] = bundle_or_obj.id
#         return kwargs
#  
#     def obj_update(self, bundle, **kwargs):
#         filters = {}
#         if hasattr(bundle.request, 'GET'):
#             filters = bundle.request.GET.copy()
#         q = filters.get('brand', None)
#         preference_key = kwargs["pk"]
#         data = bundle.data
#         data['key'] = preference_key
#         data['brand'] = q
#         update_app_preference(bundle.data, preference_key, q)
#  
#     def obj_delete(self, bundle, **kwargs):
#         preference_id = kwargs["pk"]
#         delete_app_preference(preference_id)
#  
#     def get_object_list(self, request):
#         filters = {}
#         if hasattr(request, 'GET'):
#             filters = request.GET.copy()
#         q = filters.get('brand', None)
#         data = get_app_preferences_list(brand=q)
#         return map(GladMindsObject, data)
#  
#     def obj_get_list(self, bundle, **kwargs):
#         return self.get_object_list(bundle.request)
#  
#     def obj_get(self, bundle, **kwargs):
#         filters = {}
#         if hasattr(bundle.request, 'GET'):
#             filters = bundle.request.GET.copy()
#         q = filters.get('brand', None)
#         # We can use select_related it will solve the performance issue
#         serialized_obj = get_app_preference(kwargs["pk"], q)
#         return GladMindsObject(serialized_obj)
#  
#     @transaction.atomic
#     def save_preferences(self, bundle, **kwargs):
#         """
#         This saves the preferences
#         """
#         data = bundle.data
#         try:
#             if data['key'].find(' ') != -1:
#                 raise ImmediateHttpResponse(
#                 response=http.HttpBadRequest('key cannot have blank spaces!'))
#         except Exception as e:
#             raise ImmediateHttpResponse(
#                 response=http.HttpBadRequest('Key is missing!'))
#         try:
#             save_app_preference(data)
#         except IntegrityError as e:
#             raise ImmediateHttpResponse(
#                 response=http.HttpBadRequest(e.message))
#         except Exception as e:
#             raise Exception()
#  
#     def obj_create(self, bundle, **kwargs):
#         """
#         Overriding the obj_create
#         """
#         self.save_preferences(bundle, **kwargs)
#         return bundle
#      
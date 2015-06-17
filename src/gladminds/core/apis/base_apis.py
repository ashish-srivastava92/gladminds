"""
It has base resource for API.
and Object_Class which we are using instead of query set
"""
from tastypie.resources import Resource, ModelResource
from tastypie.utils.mime import determine_format
from tastypie.http import HttpBadRequest
from tastypie.exceptions import ImmediateHttpResponse
from tastypie.fields import ApiField
from django.http.response import HttpResponse
from tastypie import http
from django.conf import settings
from gladminds.core.model_fetcher import get_model


class BaseCorsResource(Resource):
    """
    Class implementing CORS
    """
    def create_response(self, *args, **kwargs):
        response = super(BaseCorsResource, self).create_response(*args, **kwargs)
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Headers'] = 'Content-Type'
        return response

    def method_check(self, request, allowed=None):
        if allowed is None:
            allowed = []

        request_method = request.method.lower()
        for i,method in enumerate(allowed):
            allowed[i] = method.encode('ascii','ignore')
        allows = ','.join(map(str.upper, allowed))

        if request_method == 'options':
            response = HttpResponse(allows)
            response['Access-Control-Allow-Origin'] = '*'
            response['Access-Control-Allow-Headers'] = 'Content-Type'
            response['Allow'] = allows
            raise ImmediateHttpResponse(response=response)

        if not request_method in allowed:
            response = http.HttpMethodNotAllowed(allows)
            response['Allow'] = allows
            raise ImmediateHttpResponse(response=response)

        return request_method


class CustomBaseModelResource(BaseCorsResource, ModelResource):
    def determine_format(self, request):
        """
        return application/json as the default format
        """
        fmt = determine_format(request, self._meta.serializer,\
                               default_format=self._meta.default_format)
        if fmt == 'text/html' and 'format' not in request:
            fmt = 'application/json'
        return fmt
    
    def dispatch(self, request_type, request, **kwargs):
        if self._meta and hasattr(self._meta, 'queryset'):
            if settings.BRAND in settings.OUTSIDE_BRANDS:
                model = get_model(self._meta.queryset.model.__name__, brand=settings.BRAND)
                setattr(self._meta, 'object_class', model)
        return super(CustomBaseModelResource, self).dispatch(request_type, request, **kwargs)
 
    def get_object_list(self, request):
        if settings.BRAND in settings.OUTSIDE_BRANDS:
            return get_model(self._meta.queryset.model.__name__, brand=settings.BRAND).objects.all()
        return self._meta.queryset._clone()

 
class CustomApiObject(dict):
    """
    GladMindsObject is used because:-
    If we don't use the queryset then we need to specify the object_class
    """
    def __getattr__(self, name):
        """
        Tastypie access attr using dot(.) operator.
        So we need to override the __getattr_
        """
        if name in self:
            return self[name]
        else:
            return None
  
  
class JSONApiField(ApiField):
    """
    Custom ApiField for dealing with data from custom JSONFields.
    """
    dehydrated_type = 'json'
    help_text = 'JSON structured data.'
  
    def dehydrate(self, bundle, for_list=True):
        return self.convert(super(JSONApiField, self).dehydrate(bundle, for_list))
  
    def convert(self, value):
        return value
  
  
def get_required_dictionary(original_dict, *fields):
    """
    It will return the new dictionary which will have only given fields
    """
    new_dict = {}
    for f in fields:
        val = original_dict.get(f, None)
        #FIXME : Bad way to handle empty strings
        new_dict[f] = None if val == "" else val
    return new_dict
  
  
class CustomBaseResource(Resource):
    """
    All resourses are inheriting this resource,
    it have all functions which is commonly using to all classes
    """
    def determine_format(self, request):
        """
        return application/json as the default format
        """
        fmt = determine_format(request, self._meta.serializer,\
                               default_format=self._meta.default_format)
        if fmt == 'text/html' and 'format' not in request:
            fmt = 'application/json'
        return fmt
  
    def check_mandatory_fields(self, bundle, *mandatory_fields):
        """
        For given mandatory fields it will check from bundle.
        raise error if not present
        """
        for f in mandatory_fields:
            if f not in bundle.data.keys():
                raise ImmediateHttpResponse(HttpBadRequest("%s cannot be\
                empty" % f))

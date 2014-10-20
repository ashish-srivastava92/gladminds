#########################AfterBuy Resources############################################
from gladminds.core.apis.base_apis import CustomBaseResource
from tastypie import fields, http
from gladminds.gm.models import GladmindsUser, UserProduct
from gladminds.core.resource.authentication import AccessTokenAuthentication
from tastypie.utils.urls import trailing_slash
from django.conf.urls import url
from tastypie.exceptions import ImmediateHttpResponse
from django.forms.models import model_to_dict
from django.http.response import HttpResponse, HttpResponseBadRequest



class GladmindsUserResource(CustomBaseResource):
    products = fields.ListField()
    class Meta:
        queryset = GladmindsUser.objects.all()
        resource_name = 'users'
        #authentication = AccessTokenAuthentication()

    def prepend_urls(self):
        return [
            #url(r"^(?P<resource_name>%s)/otp%s" % (self._meta.resource_name, trailing_slash()), self.wrap_view('process_otp'), name="validate_otp"),
            #url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/products%s" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_products'), name="api_get_products"),
        ]    
        
    def obj_get(self, bundle, **kwargs):
        request = bundle.request
        customer_id = kwargs['pk']
        try:
            customer_detail = GladmindsUser.objects.get(gladmind_customer_id=customer_id)
            return customer_detail
        except:
            raise ImmediateHttpResponse(response=http.HttpBadRequest())
    
    def obj_create(self, bundle, **kwargs):
        """
        A ORM-specific implementation of ``obj_create``.
        """
#        bundle.obj = self._meta.object_class()
#        for key, value in kwargs.items():
#            setattr(bundle.obj, key, value)
#
#        bundle = self.full_hydrate(bundle)
#        return self.save(bundle)
        return bundle
    
    def get_products(self, request, **kwargs):
        user_id = kwargs['pk']
        products = UserProduct.objects.filter(user=user_id)
        products = [model_to_dict(product) for product in products]
        to_be_serialized = {"products": products}
        return self.create_response(request, data=to_be_serialized)
    
    def dehydrate(self, bundle):
        products = UserProduct.objects.filter(user=bundle.data['id'])
        bundle.data['products'] = [model_to_dict(product) for product in products]
        return bundle
    
    def process_otp(self, bundle, **kwargs):
        if bundle.GET.get('otp', None) and bundle.GET.get('user_id', None):
            try:
                customer = UserProduct.objects.get(gladmind_customer_id=bundle.GET['user_id'])
                http_class=HttpResponse
                data={'status':True}
            except:
                http_class=HttpResponseBadRequest
                data={'message':'User does not exist.'}
        elif bundle.GET.get('user_id', None):
            try:
                #TODO: Implement real API
                customer = UserProduct.objects.get(gladmind_customer_id=bundle.GET['user_id'])
                http_class=HttpResponse
                data={'message':'OTP has been sent to user mobile.'}
            except:
                http_class=HttpResponseBadRequest
                data={'message':'User does not exist.'}
        else:
            http_class=HttpResponseBadRequest
            data={'message': 'Invalid OTP or User.'}

        return self.create_response(bundle, response_class=http_class, data=data)

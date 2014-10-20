import json
import logging
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse
from django.conf.urls import url
from tastypie.http import HttpBadRequest
from tastypie.resources import ModelResource
from tastypie.utils.urls import trailing_slash

from gladminds.core import base_models as common
from gladminds.core import utils
from gladminds.afterbuy import models as afterbuy_common
from gladminds.core.utils import mobile_format
from gladminds.core.apis.base_resource import CustomBaseResource
from gladminds.core.apis.user_apis import AccessTokenAuthentication
from tastypie.authorization import Authorization

logger = logging.getLogger("gladminds")

class ProductResources(CustomBaseResource):
    class Meta:
#         queryset = common.ProductData.objects.all()
        resource_name = 'product'
        print "hello"
        authentication = AccessTokenAuthentication()

    def prepend_urls(self):
        return [
                url(r"^(?P<resource_name>%s)/insurance%s" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_product_insurance'), name="get_product_insurance")
        ]
        
    def get_product_insurance(self, request, **kwargs):
        print kwargs
        '''This API fetches the insurance information for a particular product
            whose VIN is provided in the request '''
        resp = {}
#         id = request.User
        print kwargs
        id = request.GET.get('id')
        if not id:
            return HttpBadRequest("Product ID is required.")
        try:
            product_info = afterbuy_common.UserProduct.objects.filter(id=id)
            print "productinfo",product_info
            insurance_info = afterbuy_common.ProductInsuranceInfo.objects.filter(product=product_info)
            print "insuranceinfo",insurance_info
            for field in ['agency_name', 'policy_number', 'expiry_date', 'insurance_brand_id',
                           'insurance_brand_name', 'policy_number', 'premium', 'insurance_phone', 'insurance_email']:
                resp[field] = getattr(insurance_info, field)
            resp = utils.get_dict_from_object(resp)
        except Exception as ex:
            logger.info("[Exception get_product_insurance]:{0}".format(ex))
            return HttpBadRequest("No insurance info exists")
        return HttpResponse(json.dumps(resp))

        

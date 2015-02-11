#from tastypie.constants import ALL
from gladminds.core.apis.base_apis import CustomBaseModelResource
from gladminds.core.model_fetcher import models
from tastypie.authorization import Authorization
from tastypie import fields
from gladminds.core.apis.user_apis import UserProfileResource
from gladminds.core.apis.product_apis import ProductTypeResource
from django.conf.urls import url
from django.http.response import HttpResponse
import json
from django.forms.models import model_to_dict
from django.db.models.query_utils import Q
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.utils.urls import trailing_slash
from tastypie import fields

class NsmResource(CustomBaseModelResource):
    class Meta:
        queryset = models.NationalSalesManager.objects.all()
        resource_name = "nsms"
        authorization = Authorization()
        detail_allowed_methods = ['get', 'post', 'put']
        always_return_data = True
        
        
class AsmResource(CustomBaseModelResource):
    class Meta:
        queryset = models.AreaSalesManager.objects.all()
        resource_name = "asms"
        authorization = Authorization()
        detail_allowed_methods = ['get', 'post', 'put']
        always_return_data = True
        
class PartnerResource(CustomBaseModelResource):
    class Meta:
        queryset = models.Partner.objects.all()
        resource_name = "partners"
        authorization = Authorization()
        detail_allowed_methods = ['get', 'post', 'put']
        always_return_data = True


class DistributorResource(CustomBaseModelResource):
    user = fields.ForeignKey(UserProfileResource, 'user', full=True)
    asm = fields.ForeignKey(AsmResource, 'asm', full=True)
    class Meta:
        queryset = models.Distributor.objects.all()
        resource_name = "distributors"
        authorization = Authorization()
        detail_allowed_methods = ['get', 'post', 'put']
        always_return_data = True


class RetailerResource(CustomBaseModelResource):
    class Meta:
        queryset = models.Retailer.objects.all()
        resource_name = "retailers"
        authorization = Authorization()
        detail_allowed_methods = ['get', 'post', 'put']
        always_return_data = True

class SpareMasterResource(CustomBaseModelResource):
    product_type = fields.ForeignKey(ProductTypeResource, 'product_type', full=True)
    class Meta:
        queryset = models.SparePartMasterData.objects.all()
        resource_name = "spare-master"
        authorization = Authorization()
        detail_allowed_methods = ['get', 'post', 'put']
        always_return_data = True

class ProductResource(CustomBaseModelResource):
    partner = fields.ForeignKey(PartnerResource, 'partner', null=True, blank=True, full=True)
    
    class Meta:
        queryset = models.ProductCatalog.objects.all()
        resource_name = "product-catalog"
        authorization = Authorization()
        detail_allowed_methods = ['get', 'post', 'put']
        always_return_data = True
    
class MemberResource(CustomBaseModelResource):
    distributor = fields.ForeignKey(DistributorResource, 'registered_by_distributor', null=True, blank=True, full=True) 
    preferred_retailer = fields.ForeignKey(RetailerResource, 'preferred_retailer', null=True, blank=True, full=True)
    
    class Meta:
        queryset = models.Mechanic.objects.all()
        resource_name = "member"
        authorization = Authorization()
        detail_allowed_methods = ['get', 'post', 'put']
        always_return_data = True
        filtering = {
                     "state": ALL,
                     }
        
class RedemptionResource(CustomBaseModelResource):
    member = fields.ForeignKey(MemberResource, 'member')
    product = fields.ForeignKey(ProductResource, 'product')
    
    class Meta:
        queryset = models.RedemptionRequest.objects.all()
        resource_name = "redemption-request"
        authorization = Authorization()
        detail_allowed_methods = ['get', 'post', 'put']
        always_return_data = True
        filtering = {
                     "member": ALL_WITH_RELATIONS,
                     "resolution_flag":ALL,
                     }

#     def prepend_urls(self):
#         return [
#             url(r"^(?P<resource_name>%s)/member-pending-request%s" % (self._meta.resource_name,trailing_slash()),
#                                                         self.wrap_view('pending_redemption_request'), name="pending_redemption_request")
#                 ]
#   
#     def pending_redemption_request(self,request, **kwargs):
#         redemptionrequests = models.RedemptionRequest.objects.filter(~Q(status='Delivered')).select_related('member')
#         requests  = []
#         for redemptionrequest in redemptionrequests: 
#             redemption_dict = model_to_dict(redemptionrequest.member,exclude=['expected_delivery_date','due_date','image_url'])
#             redemption_dict['created_date'] = str(redemptionrequest.member.created_date)
#             redemption_dict['due_date'] = str(redemptionrequest.member.modified_date)
#             redemption_dict['image_url'] = str(redemptionrequest.member.image_url)
#             redemption_dict['registered_date'] = str(redemptionrequest.member.registered_date)
#             redemption_dict['date_of_birth'] = str(redemptionrequest.member.date_of_birth)
#             requests.append(redemption_dict)
#         return HttpResponse(json.dumps(request), content_type="application/json")

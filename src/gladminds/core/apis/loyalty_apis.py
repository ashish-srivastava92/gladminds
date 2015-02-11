#from tastypie.constants import ALL
from gladminds.core.apis.base_apis import CustomBaseModelResource
from gladminds.core.model_fetcher import models
from tastypie.authorization import Authorization
from tastypie import fields
from gladminds.core.apis.user_apis import UserProfileResource
from gladminds.core.apis.product_apis import ProductTypeResource

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
#from tastypie.constants import ALL
from gladminds.core.apis.base_apis import CustomBaseModelResource
from gladminds.core.model_fetcher import models
from tastypie.authorization import Authorization

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
        resource_name = "partner"
        authorization = Authorization()
        detail_allowed_methods = ['get', 'post', 'put']
        always_return_data = True
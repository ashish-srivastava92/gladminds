#from tastypie.constants import ALL
from gladminds.core.apis.base_apis import CustomBaseModelResource
from gladminds.core.model_fetcher import models
from tastypie.authorization import Authorization

class NationalSalesResource(CustomBaseModelResource):
    class Meta:
        queryset = models.NationalSalesManager.objects.all()
        resource_name = "nsmnames"
        authorization = Authorization()
        detail_allowed_methods = ['get', 'post', 'put']
        always_return_data = True
        
        
class AreaSalesResource(CustomBaseModelResource):
    class Meta:
        queryset = models.AreaSalesManager.objects.all()
        resource_name = "asmnames"
        authorization = Authorization()
        detail_allowed_methods = ['get', 'post', 'put']
        always_return_data = True
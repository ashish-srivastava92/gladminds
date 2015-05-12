from tastypie.authorization import Authorization
from tastypie.constants import ALL, ALL_WITH_RELATIONS

from gladminds.core.apis.authentication import AccessTokenAuthentication
from gladminds.core.apis.base_apis import CustomBaseModelResource
from gladminds.core.model_fetcher import get_model
from tastypie import fields


class BrandVerticalResource(CustomBaseModelResource):
    
    class Meta:
        queryset = get_model('BrandVertical').objects.all()
        resource_name ="brand-vertical"
        authorization = Authorization()
        authentication = AccessTokenAuthentication()
        detail_allowed_methods = ['get', 'post']
        always_return_data = True
        filtering = {
                     "name" : ALL
                     }
        
class BrandProductRangeResource(CustomBaseModelResource):
    
    class Meta:
        queryset = get_model('BrandProductRange').objects.all()
        resource_name = "brand-product-range"
        authorization = Authorization()
        authentication = AccessTokenAuthentication()
        detail_allowed_methods =['get', 'post']
        always_return_data = True 
        filtering = {
                     "sku_code": ALL,
                     "vertical" : ALL
                     }
    
class BOMHeaderResource(CustomBaseModelResource):
    
    class Meta:
        queryset = get_model('BOMHeader').objects.all()
        resource_name = 'bom-header'
        authorization = Authorization()
        authentication = AccessTokenAuthentication()
        detail_allowed_methods = ['get', 'post'] 
        always_return_data = True
        excludes = ['created_date', 'created_on', 'modified_date', 'plant', 'valid_from', 'valid_to']
        include_resource_uri = False
        filtering = {
                     "sku_code" : ALL,
                     "bom_number" : ALL
                     }
class BOMPlateResource(CustomBaseModelResource):
    
    class Meta:
        queryset = get_model('BOMPlate').objects.all()
        resource_name = 'bom-plate'
        authorization = Authorization()
        authentication = AccessTokenAuthentication()
        detail_allowed_method = ['get', 'post']
        always_return_data = True
        include_resource_uri = False
        excludes = ['created_date', 'modified_date', 'image_url', 'plate_txt']

class BOMPartResource(CustomBaseModelResource):
    
    class Meta:
        queryset = get_model('BOMPart').objects.all()
        resource_name = 'bom-plate'
        authorization = Authorization()
        authentication = AccessTokenAuthentication()
        always_return_date = True
        include_resource_uri = False
        
class BOMPlatePartResource(CustomBaseModelResource):
    bom = fields.ForeignKey(BOMHeaderResource, 'bom', null=True , blank=True, full=True)
    plate = fields.ForeignKey(BOMPlateResource, 'plate', null=True, blank=True, full=True)
    part = fields.ForeignKey(BOMPartResource, 'part', null=True, blank=True)
    class Meta:
        queryset = get_model('BOMPlatePart').objects.all()
        resource_name = 'bom-plate-part'
        authorization = Authorization()
        authentication = AccessTokenAuthentication()
        detail_allowed_methods = ['get', 'post']
        always_return_data = True
        include_resource_uri = False
        excludes = ['quantity', 'valid_from', 'valid_to', 'created_date', 'modified_date', 'part']
        
        filtering = {
                     "bom" : ALL_WITH_RELATIONS
                     }
        
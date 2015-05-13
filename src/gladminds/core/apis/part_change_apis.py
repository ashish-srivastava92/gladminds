import json
import logging

from django.conf import settings
from django.conf.urls import url
from django.forms.models import model_to_dict
from django.http.response import HttpResponse, HttpResponseBadRequest
from tastypie import fields
from tastypie.authorization import Authorization
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.utils.urls import trailing_slash

from gladminds.core.apis.authentication import AccessTokenAuthentication
from gladminds.core.apis.base_apis import CustomBaseModelResource
from gladminds.core.model_fetcher import get_model


LOG = logging.getLogger('gladminds')


class BrandVerticalResource(CustomBaseModelResource):
    
    class Meta:
        queryset = get_model('BrandVertical').objects.all()
        resource_name = "brand-verticals"
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
        detail_allowed_methods = ['get', 'post']
        always_return_data = True 
        filtering = {
                     "sku_code": ALL,
                     "vertical" : ALL
                     }
    
class BOMHeaderResource(CustomBaseModelResource):
    
    class Meta:
        queryset = get_model('BOMHeader').objects.all()
        resource_name = 'bom-headers'
        authorization = Authorization()
        authentication = AccessTokenAuthentication()
        detail_allowed_methods = ['get', 'post'] 
        always_return_data = True
        include_resource_uri = False
        filtering = {
                     "sku_code" : ALL,
                     "bom_number" : ALL
                     }
        
class BOMPlateResource(CustomBaseModelResource):
    
    class Meta:
        queryset = get_model('BOMPlate').objects.all()
        resource_name = 'bom-plates'
        authorization = Authorization()
        authentication = AccessTokenAuthentication()
        detail_allowed_method = ['get', 'post']
        always_return_data = True
        include_resource_uri = False
        filtering = {
                     "plate_id" : ALL
                     }
        
class BOMPartResource(CustomBaseModelResource):
    
    class Meta:
        queryset = get_model('BOMPart').objects.all()
        resource_name = 'bom-parts'
        authorization = Authorization()
        authentication = AccessTokenAuthentication()
        always_return_date = True
        include_resource_uri = False
        filtering = {
                     "part_number" : ALL
                     }
        
        
class BOMPlatePartResource(CustomBaseModelResource):
    bom = fields.ForeignKey(BOMHeaderResource, 'bom', null=True , blank=True, full=True)
    plate = fields.ForeignKey(BOMPlateResource, 'plate', null=True, blank=True, full=True)
    part = fields.ForeignKey(BOMPartResource, 'part', null=True, blank=True, full=True)
    class Meta:
        queryset = get_model('BOMPlatePart').objects.all()
        resource_name = 'bom-plate-parts'
        authorization = Authorization()
        authentication = AccessTokenAuthentication()
        detail_allowed_methods = ['get', 'post']
        always_return_data = True
        include_resource_uri = False
        
        filtering = {
                     "bom" : ALL_WITH_RELATIONS,
                     "plate" : ALL_WITH_RELATIONS,
                     "part" : ALL_WITH_RELATIONS
                     }
    
    def prepend_urls(self):
        return [ url(r"^(?P<resource_name>%s)/get-plates%s" % (self._meta.resource_name,trailing_slash()),
                     self.wrap_view('get_plates'), name="get_plates")]
    
    def dehydrate(self, bundle):
        bom_visualization = get_model('BOMVisualization').objects.filter(bom=bundle.data['id'])
        bundle.data['bom_visualization'] = [model_to_dict(b) for b in bom_visualization]
        return bundle    
        
    
    def get_plates(self, request, **kwargs):
        self.is_authenticated(request)
        sku_code = request.GET.get('sku_code')
        bom_number = request.GET.get('bom_number')
        try:
            bom_plate_part =  get_model('BOMPlatePart', settings.BRAND).objects.\
            select_related('plate').filter(bom__sku_code=sku_code, bom__bom_number=bom_number)
            plate_details = []
            for data in bom_plate_part:
                plate = {}
                plate['plate_id'] = data.plate.plate_id
                plate['image_url'] = data.plate.plate_image
                if not data.plate.plate_image:
                    plate['image_url'] = ""
                plate['description'] = data.plate.plate_txt
                plate_details.append(plate)
            return HttpResponse(content=json.dumps(plate_details),
                                content_type='application/json')
        except Exception as ex:
            LOG.error('Exception while fetching plate images : {0}'.format(ex))
            return HttpResponseBadRequest()
    
class BOMVisualizationResource(CustomBaseModelResource):
    bom = fields.ForeignKey(BOMPlatePartResource, 'bom', null=True, blank=True, full=True)
    
    class Meta:
        queryset = get_model('BOMVisualization').objects.all()
        resource_name = 'bom-visualizations'
        authorization = Authorization()
        authentication = AccessTokenAuthentication()
        detail_allowed_methods = ['get']
        filtering = {
                     "bom" : ALL_WITH_RELATIONS
                     }
        
        
class ECOReleaseResource(CustomBaseModelResource):
    
    class Meta:
        queryset = get_model('ECORelease').objects.all()
        resource_name = 'eco-releases'
        authorization = Authorization()
        authentication = AccessTokenAuthentication()
        detail_allowed_methods = ['get', 'post']

class ECOImplementationResource(CustomBaseModelResource):
    
    class Meta:
        queryset = get_model('ECOImplementation').objects.all()
        resource_name = 'eco-implementations'
        authorization = Authorization()
        authentication = AccessTokenAuthentication()
        detail_allowed_methods = ['get', 'post']
        always_return_data = True
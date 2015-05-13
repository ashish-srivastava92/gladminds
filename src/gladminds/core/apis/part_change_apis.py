import json
import logging
import csv
from django.conf.urls import url
from django.conf import settings
from django.http.response import HttpResponse

from tastypie import fields
from tastypie.utils.urls import trailing_slash
from tastypie.authorization import Authorization
from tastypie.constants import ALL, ALL_WITH_RELATIONS

from gladminds.core.apis.authentication import AccessTokenAuthentication
from gladminds.core.apis.base_apis import CustomBaseModelResource
from gladminds.core.model_fetcher import get_model
from gladminds.core.auth_helper import Roles
from gladminds.core.core_utils.utils import format_part_csv

logger = logging.getLogger('gladminds')

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
        return [
                 url(r"^(?P<resource_name>%s)/save-part%s" % (self._meta.resource_name,trailing_slash()),
                     self.wrap_view('save_plate_part'), name="save_plate_part"),
                ]
    
    
    def save_plate_part(self, request, **kwargs):
        self.is_authenticated(request)
        if request.method != 'POST':
            return HttpResponse(json.dumps({"message" : "Method not allowed"}), content_type= "application/json",
                                status=400)
        post_data=request.POST
        model = post_data.get('model')
        sku_code = post_data.get('skuCode')
        bom_number = post_data.get('bomNumber')
        plate_id = post_data.get('plateId')
        plate_image=request.FILES['platImage']
        plate_map=request.FILES['plateMap']
        sbom_part_mapping=[]
        try:
            queryset = get_model('BOMPlatePart').objects.filter(bom__sku_code=sku_code,
                                                                bom__bom_number=bom_number,
                                                                plate__plate_id=plate_id)
            for query in queryset:
                temp={}
                temp['part_number']=query.part.part_number
                temp['bomplatepart_object']=query
                sbom_part_mapping.append(temp)

            plate_obj=get_model('BOMPlate').objects.filter(plate_id=plate_id)
            plate_obj[0].plate_image_with_part.save(plate_image.name, plate_image)

        
            data={'plate_id':plate_id, 'sku_code':sku_code,
                  'bom_number':bom_number,
                  'model':model, 'part':[]}
            spamreader = csv.reader(plate_map, delimiter=',')
            next(spamreader)
            csv_data=format_part_csv(spamreader)
            for part_entry in csv_data:
                active = filter(lambda active: active['part_number'] == part_entry['part_number'], sbom_part_mapping)
                if active:
                    bompartplate_obj=active[0]['bomplatepart_object']
                    part_data=bompartplate_obj.part
                    part_data.description=part_entry['desc']
                    part_data.save(using=settings.BRAND)
                    try:
                        visual_obj=get_model('BOMVisualization').objects.filter(bom=bompartplate_obj)
                        if not visual_obj:
                            visual_obj=get_model('BOMVisualization')(bom=bompartplate_obj,
                                                        x_coordinate=part_entry['x-axis'],
                                                        y_coordinate=part_entry['y-axis'],
                                                        z_coordinate=part_entry['z-axis'],
                                                        serial_number=part_entry['serial_number'],
                                                        part_href=part_entry['href'])
                        else:
                            visual_obj=visual_obj[0]
                            visual_obj.x_coordinate=part_entry['x-axis']
                            visual_obj.y_coordinate=part_entry['y-axis']
                            visual_obj.z_coordinate=part_entry['z-axis']
                            visual_obj.serial_number=part_entry['serial_number']
                            visual_obj.part_href=part_entry['href']
                        visual_obj.save(using=settings.BRAND)
                        part_entry['status']='SUCCESS'
                    except Exception as ex:
                        logger.error('[save_plate_part]: {0}'.format(ex))
                        part_entry['status']='INCOMPLETE'
                else:
                    logger.info('[save_plate_part]: the part number {0} is invalid'.format(part_entry['part_number']))
                    part_entry['status']='ERROR'
                data['part'].append(part_entry)
            for part in sbom_part_mapping:
                active = filter(lambda active: active['part_number'] == part['part_number'], data['part'])
                if not active:
                    temp={}
                    temp['part_number']=part['part_number']
                    temp['status']='MISSING'
                    data['part'].append(temp)
        except Exception as ex:
            logger.info('[save_plate_part]: {0}'.format(ex))
        return HttpResponse(json.dumps(data), content_type="application/json")
 
class BOMVisualizationResource(CustomBaseModelResource):
    bom = fields.ForeignKey(BOMPlatePartResource, 'bom', null=True, blank=True, full=True)
    
    class Meta:
        queryset = get_model('BOMVisualization').objects.all()
        resource_name = 'bom-visualizations'
        authorization = Authorization()
        authentication = AccessTokenAuthentication()
        detail_allowed_methods = ['get']
        
        
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

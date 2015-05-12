from django.conf.urls import url
from tastypie.authorization import Authorization
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from django.conf.urls import url
from django.conf import settings

from gladminds.core.apis.authentication import AccessTokenAuthentication
from gladminds.core.apis.base_apis import CustomBaseModelResource
from gladminds.core.model_fetcher import get_model
from tastypie import fields
from tastypie.utils.urls import trailing_slash
from django.http.response import HttpResponse
import json
from gladminds.core.auth_helper import Roles


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
        import csv
#         self.is_authenticated(request)
        print "344444444444444", request.POST
        print "344444444444444", request.FILES['platImage']
        print "344444444444444", request.FILES['plateMap']
        abc=request.FILES['platImage']
        xyz=request.FILES['plateMap']
        mapping=[]
        queryset = get_model('BOMPlatePart').objects.filter(bom__sku_code='00DH15ZZ',
                                                            bom__bom_number='211760',
                                                            plate__plate_id='44')
        for query in queryset:
            temp={}
            temp['part_id']=query.part.part_id
            
#         try:
#             plate_obj=get_model('BOMPlate').objects.filter(plate_id='44')
#             plate_obj[0].plate_image_with_part.save(abc.name, abc)
#         except Exception as ex:
#             print "344444444444444", ex
        print "4555555555555", queryset
        try:
            spamreader = csv.reader(xyz, delimiter=',')
            next(spamreader)
            for row_list in spamreader:
                print "3444444444444444", row_list
        except Exception as ex:
            print "344444444444444", ex
        return
        if request.method != 'POST':
            return HttpResponse(json.dumps({"message" : "Method not allowed"}), content_type= "application/json",
                                status=400)
        if not request.user.is_superuser and not request.user.groups.filter(name=Roles.ZSM).exists():
            return HttpResponse(json.dumps({"message" : "Not Authorized to add ASM"}), content_type= "application/json",
                                status=401)
        try:
            load = json.loads(request.body)
        except:
            return HttpResponse(content_type="application/json", status=404)
        asm_id = load.get('id')
        try:
            asm_data = models.AreaServiceManager.objects.get(asm_id=asm_id)
            data = {'status': 0 , 'message' : 'Area service manager with this id already exists'}
        except Exception as ex:
            logger.info("[register_area_service_manager]: New ASM registration:: {0}".format(ex))
            name = load.get('name')
            area = load.get('area')
            phone_number = load.get('phone-number')
            email = load.get('email')
            zsm_id = load.get('zsm_id')
            zsm_data = models.ZonalServiceManager.objects.get(zsm_id=zsm_id)
            user_data = register_user.register_user(Roles.AREASERVICEMANAGER,
                                             username=email,
                                             phone_number=phone_number,
                                             first_name=name,
                                             email = email,
                                             APP=settings.BRAND)
            asm_data = models.AreaServiceManager(asm_id=asm_id, user=user_data,
                                        area=area, zsm=zsm_data)
            asm_data.save()
            data = {"status": 1 , "message" : "Area service manager registered successfully"}
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

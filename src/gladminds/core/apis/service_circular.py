from gladminds.core.apis.base_apis import CustomBaseModelResource
from gladminds.core.model_fetcher import models, get_model
from gladminds.core import constants
from gladminds.core.apis.authentication import AccessTokenAuthentication
from tastypie.authorization import Authorization
from django.http.response import HttpResponse, HttpResponseBadRequest
from tastypie import fields
import json
import logging
from gladminds.core.apis.part_change_apis import BrandProductRangeResource
from tastypie.utils.urls import trailing_slash
from django.conf.urls import url
from gladminds.bajaj.models import BrandProductRange
from tastypie.constants import ALL_WITH_RELATIONS

logger = logging.getLogger("gladminds")

class ServiceCircularResource(CustomBaseModelResource):
    model_sku_code = fields.ManyToManyField(BrandProductRangeResource, 'model_sku_code', full=True)
    
    class Meta:
        queryset = models.ServiceCircular.objects.all()
        resource_name = "service-circular"
        authorization = Authorization()
        detail_allowed_methods = ['get', 'post']
        always_return_data = True
        filtering = {
                     'model_sku_code' : ALL_WITH_RELATIONS,
                     }
        
    def prepend_urls(self):
        return [
              url(r"^(?P<resource_name>%s)/save_circular%s" % (self._meta.resource_name,trailing_slash()),
                                                     self.wrap_view('save_circular'), name="save_circular")
                ]
        
    def save_circular(self,request, **kwargs):
        try:
            data = request.POST.copy()
            sku_list=data.getlist('model_sku_code')
            if sku_list:
                circular_obj = get_model('ServiceCircular')(product_type=data['product_type'],
                                                            type_of_circular = data['type_of_circular'],
                                                            change_no = data['change_no'],
                                                            new_circular = data['new_circular'],
                                                            buletin_no = data['buletin_no'],
                                                            circular_date = data['circular_date'],
                                                            from_circular = data['from_circular'],
                                                            to_circular = data['to_circular'],
                                                            cc_circular = data['cc_circular'],
                                                            circular_subject = data['circular_subject'],
                                                            part_added = data['part_added'],
                                                            circular_title = data['circular_title'],
                                                            part_deleted = data['part_deleted'],
                                                            part_changed = data['part_changed'],
                                                            model_name = data['model_name'],
                                                            sku_description = data['sku_description'])
                circular_obj.save()
                sku_code_list = get_model('BrandProductRange').objects.filter(sku_code__in=sku_list)
                for sku_code in sku_code_list:
                    circular_obj.model_sku_code.add(sku_code)
                data = {'status':1, 'message': 'Successfully saved'}
            else:
                data = {'status':0, 'message': 'sku_code is mandatary'}
        except Exception as ex:
            logger.error('[service_circular]:{0}:: {1}'.format(ex))
            data = {'status': 0, 'message': 'could not save'}
        return HttpResponse(json.dumps(data), content_type="application/json")

from tastypie.constants import  ALL

'''Contains audit log sms details'''
from gladminds.core.model_fetcher import models
from gladminds.core.apis.base_apis import CustomBaseModelResource


class AuditResources(CustomBaseModelResource):
    class Meta:
            queryset = models.AuditLog.objects.all()
            resource_name = 'audit'
            detail_allowed_methods = ['get']
            filtering = {
                     "date": ALL
                     }

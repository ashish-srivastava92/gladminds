from tastypie.constants import  ALL
from gladminds.aftersell.models import logs
from gladminds.apis.baseresource import CustomBaseResource


'''Contains audit log sms details'''


class AuditResources(CustomBaseResource):
    class Meta:
            queryset = logs.AuditLog.objects.all()
            resource_name = 'audit'
            detail_allowed_methods = ['get']
            filtering = {
                     "date": ALL
                     }

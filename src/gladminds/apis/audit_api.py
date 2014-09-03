from gladminds.aftersell.models import logs
from gladminds.apis.baseresource import CustomBaseResource


'''Contains audit log sms details'''


class AuditResources(CustomBaseResource):
    class Meta:
            queryset = logs.AuditLog.objects.all()
            resource_name = 'audit'
            include_resource_uri = False
            detail_allowed_methods = ['get']
            always_return_data = True

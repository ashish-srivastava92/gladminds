from tastypie.resources import ModelResource
from tastypie.utils.mime import determine_format
from gladminds.aftersell.models import logs


class AuditBaseResource(ModelResource):
    def determine_format(self, request):
        """
        return application/json as the default format
        """
        fmt = determine_format(request, self._meta.serializer,\
                               default_format=self._meta.default_format)
        if fmt == 'text/html' and 'format' not in request:
            fmt = 'application/json'
        return fmt

'''Contains audit log sms details'''


class AuditResources(AuditBaseResource):
    class Meta:
            queryset = logs.AuditLog.objects.all()
            resource_name = 'audit'
            include_resource_uri = False
            detail_allowed_methods = ['get']
            always_return_data = True

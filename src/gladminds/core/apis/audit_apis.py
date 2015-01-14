'''Contains audit log sms details'''

from tastypie.constants import  ALL
from tastypie.authorization import DjangoAuthorization

from gladminds.core.model_fetcher import models
from gladminds.core.apis.base_apis import CustomBaseModelResource
from gladminds.core.apis.authentication import AccessTokenAuthentication
from gladminds.core.apis.authorization import CustomAuthorization,\
    MultiAuthorization

_FILTERING = {"created_date": ALL}


class AuditResource(CustomBaseModelResource):
    class Meta:
        queryset = models.AuditLog.objects.all()
        resource_name = 'audit'
        authentication = AccessTokenAuthentication()
        authorization = MultiAuthorization(DjangoAuthorization(), CustomAuthorization())
        detail_allowed_methods = ['get']
        filtering = _FILTERING


class SMSLogResource(CustomBaseModelResource):
    class Meta:
        queryset = models.SMSLog.objects.all()
        resource_name = 'sms-logs'
        authentication = AccessTokenAuthentication()
        authorization = MultiAuthorization(DjangoAuthorization(), CustomAuthorization())
        detail_allowed_methods = ['get']
        filtering = _FILTERING
        ordering = ['created_date']

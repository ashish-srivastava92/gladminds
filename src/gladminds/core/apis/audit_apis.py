'''Contains audit log sms details'''
from tastypie.constants import ALL_WITH_RELATIONS, ALL
from tastypie.authorization import DjangoAuthorization
from tastypie import fields
from gladminds.core.apis.base_apis import CustomBaseModelResource
from gladminds.core.apis.authentication import AccessTokenAuthentication
from gladminds.core.apis.authorization import MultiAuthorization
from tastypie.authentication import MultiAuthentication
from gladminds.core.model_fetcher import models
from gladminds.core.apis.product_apis import ProductResource
from gladminds.core.apis.user_apis import ServiceAdvisorResource

_FILTERING = {"created_date": ALL}


class AuditResource(CustomBaseModelResource):
    class Meta:
        queryset = models.AuditLog.objects.all()
        resource_name = 'audit'
        authentication = AccessTokenAuthentication()
        authorization = MultiAuthorization(DjangoAuthorization())
        detail_allowed_methods = ['get']
        filtering = _FILTERING


class SMSLogResource(CustomBaseModelResource):
    class Meta:
        queryset = models.SMSLog.objects.all()
        resource_name = 'sms-logs'
        authentication = AccessTokenAuthentication()
        authorization = MultiAuthorization(DjangoAuthorization())
        detail_allowed_methods = ['get']
        filtering = _FILTERING
        ordering = ['created_date']


class DataFeedLogResource(CustomBaseModelResource):
    class Meta:
        queryset = models.DataFeedLog.objects.all()
        resource_name = "feed-logs"
        authorization = MultiAuthorization(DjangoAuthorization())
        authentication = MultiAuthentication(AccessTokenAuthentication())
        detail_allowed_methods = ['get']
        always_return_data = True
        filtering = {
                        "feed_type": ALL,
                        "action": ALL
                     }

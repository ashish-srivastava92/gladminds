'''
This contains the dasboards apis
'''
from gladminds.core.apis.base_apis import CustomBaseResource, CustomApiObject
from tastypie.bundle import Bundle
from tastypie import fields
from tastypie.authorization import Authorization
from gladminds.core.model_fetcher import models
from gladminds.core.apis.authentication import AccessTokenAuthentication
from django.views.decorators.cache import cache_page
from django.core.cache import cache


class OverallStatusResource(CustomBaseResource):
    """
    It is a preferences resource
    """
    id = fields.CharField(attribute="id")
    name = fields.CharField(attribute="name")
    value = fields.CharField(attribute='value', null=True)

    class Meta:
        resource_name = 'overall-status'
        authentication = AccessTokenAuthentication()
        object_class = CustomApiObject

    def detail_uri_kwargs(self, bundle_or_obj):
        """
        Overriding the details_uri_kwargs and setting kwargs to Null
        It will be using for POST methods
        """
        kwargs = {}

        if isinstance(bundle_or_obj, Bundle):
            kwargs['pk'] = bundle_or_obj.obj.id
        else:
            kwargs['pk'] = bundle_or_obj.id
        return kwargs

    def obj_get_list(self, bundle, **kwargs):
        self.is_authenticated(bundle.request)
        vins = cache.get('gm_vins')
        coupons_closed = cache.get('gm_coupons_closed')
        coupons_progress = cache.get('gm_coupons_progress')
        coupons_expired = cache.get('gm_coupons_expired')
        tickets_raised = cache.get('gm_ticket_raised')
        tickets_progress = cache.get('gm_ticket_progress')

        if not vins:
            vins = set_cache('gm_vins', models.ProductData.objects.all().count())
        if not coupons_closed:
            coupons_closed = set_cache('gm_coupons_closed',
                                       models.CouponData.objects.filter(status=2).count())
        if not coupons_progress:
            coupons_progress = set_cache('gm_coupons_progress',
                                         models.CouponData.objects.filter(status=4).count())
        if not coupons_expired:
            coupons_expired = set_cache('gm_coupons_expired',
                                        models.CouponData.objects.filter(status=3).count())
        if not tickets_raised:
            tickets_raised = set_cache('gm_ticket_raised',
                                       models.Feedback.objects.all().count())
        if not tickets_progress:
            tickets_progress = set_cache('gm_ticket_progress',
                                       models.Feedback.objects.filter(status="In Progress").count())

        return map(CustomApiObject, [{"id": "1", "name": "#of Vins", "value": vins},
                                     {"id": "2", "name": "Service Coupons Closed",
                                      "value": coupons_closed},
                                     {"id": "3", "name": "Service Coupons In Progress",
                                      "value": coupons_progress},
                                     {"id": "4", "name": "Service Coupons Expired",
                                      "value": coupons_expired},
                                     {"id": "5", "name": "Tickets Raised",
                                      "value": tickets_raised},
                                     {"id": "6", "name": "Tickets In Progress",
                                      "value": tickets_progress}
                                     ]
                   )


def set_cache(key, data, timeout=60*15):
    cache.set(key, data, timeout)
    return data
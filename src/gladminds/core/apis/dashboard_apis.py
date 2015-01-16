'''
This contains the dasboards apis
'''
from gladminds.core.apis.base_apis import CustomBaseResource, CustomApiObject
from tastypie import fields
from gladminds.core.model_fetcher import models
from gladminds.core.apis.authentication import AccessTokenAuthentication
from django.core.cache import cache
from tastypie.constants import ALL


def get_vins():
    return models.ProductData.objects.all().count()


def get_set_cache(key, data_func, timeout=15):
    '''
    Used for putting data in cache .. specified on a timeout
    :param key:
    :type string:
    :param data:
    :type queryset result:
    :param timeout:
    :type int:
    '''
    result = cache.get(key)
    if result is None:
        result = data_func()
        cache.set(key, result, timeout*60)
    return result

_KEYS = ["id", "name", "value"]


def create_dict(values, keys=_KEYS):
    return dict(zip(keys, values))


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

    def obj_get_list(self, bundle, **kwargs):
        self.is_authenticated(bundle.request)
        vins = get_set_cache('gm_vins', get_vins)
        coupons_closed = get_set_cache('gm_coupons_closed',
                                       models.CouponData.objects.closed_count,
                                       timeout=13)
        coupons_progress = get_set_cache('gm_coupons_progress',
                                         models.CouponData.objects.inprogress_count,
                                         timeout=11)
        coupons_expired = get_set_cache('gm_coupons_expired',
                                        models.CouponData.objects.expired_count,
                                        timeout=16)
        tickets_raised = get_set_cache('gm_ticket_raised',
                                       models.Feedback.objects.raised_count)
        tickets_progress = get_set_cache('gm_ticket_progress',
                                         models.Feedback.objects.inprogress_count)
        dealers = get_set_cache('gm_dealers',
                               models.Dealer.objects.count)
        dealers_active = get_set_cache('gm_dealers_active',
                               models.AuthorizedServiceCenter.objects.active_count)
        ascs = get_set_cache('gm_ascs',
                               models.AuthorizedServiceCenter.objects.count)
        ascs_active = get_set_cache('gm_ascs_active',
                               models.AuthorizedServiceCenter.objects.active_count)

        return map(CustomApiObject, [create_dict(["1", "#of Vins", vins]),
                                     create_dict(["2", "Service Coupons Closed",
                                                  coupons_closed]),
                                     create_dict(["3", "Service Coupons In Progress",
                                                  coupons_progress]),
                                     create_dict(["4", "Service Coupons Expired",
                                                  coupons_expired]),
                                     create_dict(["5", "Tickets Raised",
                                                  tickets_raised]),
                                     create_dict(["6", "Tickets In Progress",
                                                  tickets_progress]),
                                     create_dict(["7", "# of Dealers",
                                                  dealers]),
                                     create_dict(["8", "# of Active Dealers",
                                                  dealers_active]),
                                     create_dict(["7", "# of ASCs",
                                                  ascs]),
                                     create_dict(["8", "# of Active ASCs",
                                                  ascs_active])
                                     ]
                   )


class FeedStatusResource(CustomBaseResource):
    """
    It is a preferences resource
    """
    id = fields.CharField(attribute="id")
    name = fields.CharField(attribute="name")
    value = fields.CharField(attribute='value', null=True)

    class Meta:
        resource_name = 'feeds-status'
        authentication = AccessTokenAuthentication()
        object_class = CustomApiObject

    def obj_get_list(self, bundle, **kwargs):
        self.is_authenticated(bundle.request)
        filters = {}
        if hasattr(bundle.request, 'GET'):
            filters = bundle.request.GET.copy()
        dtstart = filters.get('from')
        dtend = filters.get('to')
        return map(CustomApiObject, [
                                     ]
                   )

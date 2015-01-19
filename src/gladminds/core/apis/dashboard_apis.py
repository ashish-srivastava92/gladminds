'''
This contains the dasboards apis
'''
from gladminds.core.apis.base_apis import CustomBaseResource, CustomApiObject
from tastypie import fields
from gladminds.core.model_fetcher import models
from gladminds.core.apis.authentication import AccessTokenAuthentication
from django.core.cache import cache
from tastypie.constants import ALL
from gladminds.core.constants import FEED_TYPES, FeedStatus


def get_vins():
    return models.ProductData.objects.all().count()


def get_success_and_failure_counts(objects):
    fail = 0
    success = 0
    for data in objects:
        fail = fail + int(data.failed_data_count)
        success = success + int(data.success_data_count)
    return success, fail

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
                                                  ascs_active]),
                                     create_dict(["9", "# of SAs",
                                                  0]),
                                     create_dict(["10", "# of Active SAs",
                                                  0])
                                     ]
                   )


_KEYS_FEED = ["status", "type", "success_count", "failure_count"]


def create_feed_dict(values, keys=_KEYS_FEED):
    return dict(zip(keys, values))


class FeedStatusResource(CustomBaseResource):
    """
    It is a preferences resource
    """
    status = fields.CharField(attribute="status")
    feed_type = fields.CharField(attribute="type")
    success = fields.CharField(attribute="success_count")
    failure = fields.CharField(attribute="failure_count")

    class Meta:
        resource_name = 'feeds-status'
        authentication = AccessTokenAuthentication()
        object_class = CustomApiObject

    def obj_get_list(self, bundle, **kwargs):
        self.is_authenticated(bundle.request)
        filters = {}
        params = {}
        if hasattr(bundle.request, 'GET'):
            params = bundle.request.GET.copy()
        dtstart = params.get('created_date__gte')
        dtend = params.get('created_date__lte')
        if dtstart:
            filters['created_date__gte'] = dtstart
        if dtend:
            filters['created_date__lte'] = dtend

        data = []
        for status in [FeedStatus.SENT, FeedStatus.RECEIVED]:
            filters['action'] = status
            for feed_type in FEED_TYPES:
                filters['feed_type'] = feed_type
                success_count, failure_count = get_success_and_failure_counts(models.DataFeedLog.objects.filter(**filters))
                data.append(create_feed_dict([status,
                                              feed_type,
                                              success_count,
                                              failure_count]))
        return map(CustomApiObject, data)

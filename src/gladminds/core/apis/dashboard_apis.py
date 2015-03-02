'''
This contains the dasboards apis
'''
from gladminds.core.apis.base_apis import CustomBaseResource, CustomApiObject
from tastypie import fields
from gladminds.bajaj import models
from gladminds.core.apis.authentication import AccessTokenAuthentication
from django.core.cache import cache
from gladminds.core.constants import FEED_TYPES, FeedStatus, FEED_SENT_TYPES,\
    CouponStatus
from django.db import connections
from django.conf import settings
from gladminds.core.core_utils.utils import dictfetchall
from django.http.response import HttpResponse
from tastypie.utils.mime import build_content_type


def get_vins():
    return models.ProductData.objects.all().count()


def get_customers_count():
    return models.ProductData.objects.filter(purchase_date__isnull=True).count()


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
        if data_func is None:
            raise
        if not hasattr(data_func, '__call__'):
            result = data_func
        else:
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
        vins = get_set_cache('gm_vins', get_vins, timeout=30)
        customers = get_set_cache('gm_customers', get_customers_count, timeout=35)
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
                               models.Dealer.objects.active_count)
        ascs = get_set_cache('gm_ascs',
                               models.AuthorizedServiceCenter.objects.count)
        ascs_active = get_set_cache('gm_ascs_active',
                               models.AuthorizedServiceCenter.objects.active_count)
        sas = get_set_cache('gm_sas',
                            models.ServiceAdvisor.objects.count)
        sas_active = get_set_cache('gm_sas_active',
                            models.ServiceAdvisor.objects.active_count)

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
                                     create_dict(["9", "# of ASCs",
                                                  ascs]),
                                     create_dict(["10", "# of Active ASCs",
                                                  ascs_active]),
                                     create_dict(["11", "# of SAs",
                                                  sas]),
                                     create_dict(["12", "# of Active SAs",
                                                  sas_active]),
                                     create_dict(["13", "# of Customers",
                                                  customers])
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
        hash_key = "gm-feeds-status1-"
        if dtstart:
            filters['created_date__gte'] = dtstart
            hash_key = hash_key + dtstart
        if dtend:
            filters['created_date__lte'] = dtend
            hash_key = hash_key + dtend

        data_map = {}
        result = []
        filters['feed_type__in'] = FEED_SENT_TYPES + FEED_TYPES

        output = cache.get(hash_key)
        if output:
            return map(CustomApiObject, output)

        objects = models.DataFeedLog.objects.filter(**filters)

        for feed_type in FEED_SENT_TYPES + FEED_TYPES:
            data_map[feed_type] = [0, 0]
        for obj in objects:
            feed_counts = data_map[obj.feed_type] 
            feed_counts[0] = feed_counts[0] + int(obj.failed_data_count)
            feed_counts[1] = feed_counts[1] + int(obj.success_data_count)
            data_map[obj.feed_type] = feed_counts

        for key, value in data_map.items():
            action = FeedStatus.RECEIVED
            if key in FEED_SENT_TYPES:
                action = FeedStatus.SENT
            result.append(create_feed_dict([action,
                                          key,
                                          value[1],
                                          value[0]]))
        cache.set(hash_key, result, 15*60)
        return map(CustomApiObject, result)
#         data = []   
#         filters['action'] = FeedStatus.RECEIVED
#         for feed_type in FEED_TYPES:
#             filters['feed_type'] = feed_type
#             success_count, failure_count = get_success_and_failure_counts(models.DataFeedLog.objects.filter(**filters))
#             data.append(create_feed_dict([FeedStatus.RECEIVED,
#                                           feed_type,
#                                           success_count,
#                                           failure_count]))
#         filters['action'] = FeedStatus.SENT
#         for feed_type in FEED_SENT_TYPES:
#             filters['feed_type'] = feed_type
#             success_count, failure_count = get_success_and_failure_counts(models.DataFeedLog.objects.filter(**filters))
#             data.append(create_feed_dict([FeedStatus.SENT,
#                                           feed_type,
#                                           success_count,
#                                           failure_count]))
#         return map(CustomApiObject, data)


class SMSReportResource(CustomBaseResource):
    """
    It is a preferences resource
    """
    date = fields.DateField(attribute="date")
    sent = fields.DecimalField(attribute="sent", default=0)
    received = fields.DecimalField(attribute="received", default=0)

    class Meta:
        resource_name = 'sms-report'
        authentication = AccessTokenAuthentication()
        object_class = CustomApiObject

    def create_response(self, request, data, response_class=HttpResponse, **response_kwargs):
        """
        Extracts the common "which-format/serialize/return-response" cycle.

        Mostly a useful shortcut/hook.
        """
        desired_format = self.determine_format(request)
        data['overall'] = {'sent': self.get_sms_count(FeedStatus.SENT.upper()),
                           'received': self.get_sms_count(FeedStatus.RECEIVED.upper())}

        serialized = self.serialize(request, data, desired_format)
        return response_class(content=serialized, content_type=build_content_type(desired_format), **response_kwargs)

    def get_sms_count(self, action):
        data = self.get_sql_data("select count(*) as count from bajaj_smslog where action=%(action)s",
                                 filters={'action': action})
        return data[0]['count']

    def get_sql_data(self, query, filters={}):
        conn = connections[settings.BRAND]
        cursor = conn.cursor()
        cursor.execute(query, filters)
        data = dictfetchall(cursor)
        conn.close()
        return data

    def obj_get_list(self, bundle, **kwargs):
        self.is_authenticated(bundle.request)
        filters = {}
        params = {}
        if hasattr(bundle.request, 'GET'):
            params = bundle.request.GET.copy()
        dtstart = params.get('created_date__gte')
        dtend = params.get('created_date__lte')
        where_and = " AND "
        query = "select DATE(created_date) as date, action, count(*) as count from bajaj_smslog where action!='SEND TO QUEUE' "

        if dtstart:
            query = query + where_and + "DATE(created_date) >= %(dtstart)s "
            filters['dtstart'] = dtstart
        if dtend:
            query = query + where_and + "DATE(created_date) <= %(dtend)s "
            filters['dtend'] = dtend

        query = query + " group by DATE(created_date), action;"

        objs = {}
        all_data = self.get_sql_data(query, filters)
        for data in all_data:
            obj = objs.get(data['date'], {'date': data['date']})
            objs[data['date']] = obj
            objs[data['date']][data['action'].lower()] = data['count']
        return map(CustomApiObject, objs.values())


class CouponReportResource(CustomBaseResource):
    """
    It is a preferences resource
    """
    date = fields.DateField(attribute="date")
    closed = fields.DecimalField(attribute="closed", default=0)
    inprogress = fields.DecimalField(attribute="inprogress", default=0)
    unused = fields.DecimalField(attribute="unused", default=0)
    exceeds_limit = fields.DecimalField(attribute="exceeds", default=0)

    class Meta:
        resource_name = 'coupons-report'
        authentication = AccessTokenAuthentication()
        object_class = CustomApiObject

    def create_response(self, request, data, response_class=HttpResponse, **response_kwargs):
        """
        Extracts the common "which-format/serialize/return-response" cycle.

        Mostly a useful shortcut/hook.
        """
        desired_format = self.determine_format(request)
        data['overall'] = {'closed': self.get_coupon_count(CouponStatus.CLOSED),
                           'inprogress': self.get_coupon_count(CouponStatus.IN_PROGRESS)}

        serialized = self.serialize(request, data, desired_format)
        return response_class(content=serialized, content_type=build_content_type(desired_format), **response_kwargs)

    def get_coupon_count(self, status):
        status = str(status)
        try:
            return get_set_cache('gm_coupon_counter' + status, None)
        except:
            data = self.get_sql_data("select count(*) as count from bajaj_coupondata where status=%(status)s",
                                 filters={'status': status})
            return get_set_cache('gm_coupon_counter' + status, data[0]['count'])

    def get_sql_data(self, query, filters={}):
        conn = connections[settings.BRAND]
        cursor = conn.cursor()
        cursor.execute(query, filters)
        data = dictfetchall(cursor)
        conn.close()
        return data

    def obj_get_list(self, bundle, **kwargs):
        self.is_authenticated(bundle.request)
        filters = {}
        params = {}
        if hasattr(bundle.request, 'GET'):
            params = bundle.request.GET.copy()
        dtstart = params.get('created_date__gte')
        dtend = params.get('created_date__lte')
        where_and = " AND "
        query = "select c.*, d.date from bajaj_couponfact c inner join \
        bajaj_datedimension d on c.date_id=d.date_id where c.data_type='TOTAL' ";
        if dtstart:
            query = query + where_and + "DATE(d.date) >= %(dtstart)s "
            filters['dtstart'] = dtstart
        if dtend:
            query = query + where_and + "DATE(d.date) <= %(dtend)s "
            filters['dtend'] = dtend

        all_data = self.get_sql_data(query, filters)
        return map(CustomApiObject, all_data)

'''
This contains the dasboards apis
'''
from gladminds.core.apis.base_apis import CustomBaseResource, CustomApiObject
from tastypie import fields
from gladminds.core.apis.authentication import AccessTokenAuthentication
from gladminds.core.core_utils.cache_utils import Cache
from gladminds.core.constants import FEED_TYPES, FeedStatus, FEED_SENT_TYPES,\
    CouponStatus, TicketStatus
from django.db import connections
from django.conf import settings
from gladminds.core.core_utils.utils import dictfetchall
from django.http.response import HttpResponse
from tastypie.utils.mime import build_content_type
from gladminds.core.model_fetcher import get_model
from gladminds.core.auth_helper import Roles
    
def get_vins():
    return get_model('ProductData').objects.all().count()


def get_customers_count():
    return get_model('ProductData').objects.filter(purchase_date__isnull=False).count()


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
    result = Cache.get(key)
    if result is None:
        if data_func is None:
            raise
        if not hasattr(data_func, '__call__'):
            result = data_func
        else:
            result = data_func()
        Cache.set(key, result, timeout*60)
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
                                       get_model('CouponData').objects.closed_count,
                                       timeout=13)
        coupons_progress = get_set_cache('gm_coupons_progress',
                                         get_model('CouponData').objects.inprogress_count,
                                         timeout=11)
        coupons_expired = get_set_cache('gm_coupons_expired',
                                        get_model('CouponData').objects.expired_count,
                                        timeout=16)
        tickets_raised = get_set_cache('gm_ticket_raised',
                                       get_model('Feedback').objects.raised_count)
        tickets_progress = get_set_cache('gm_ticket_progress',
                                         get_model('Feedback').objects.inprogress_count)
        dealers = get_set_cache('gm_dealers',
                               get_model('Dealer').objects.count)
        dealers_active = get_set_cache('gm_dealers_active',
                               get_model('Dealer').objects.active_count)
        ascs = get_set_cache('gm_ascs',
                               get_model('AuthorizedServiceCenter').objects.count)
        ascs_active = get_set_cache('gm_ascs_active',
                               get_model('AuthorizedServiceCenter').objects.active_count)
        sas = get_set_cache('gm_sas',
                            get_model('ServiceAdvisor').objects.count)
        sas_active = get_set_cache('gm_sas_active',
                            get_model('ServiceAdvisor').objects.active_count)

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

        output = Cache.get(hash_key)
        if output:
            return map(CustomApiObject, output)

        objects = get_model('DataFeedLog').objects.filter(**filters)

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
        Cache.set(hash_key, result, 15*60)
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
        data = self.get_sql_data("select count(*) as count from gm_smslog where action=%(action)s",
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
        query = "select DATE(created_date) as date, action, count(*) as count from gm_smslog where action!='SEND TO QUEUE' "

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
            data = self.get_sql_data("select count(*) as count from gm_coupondata where status=%(status)s",
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
        query = "select c.*, d.date from gm_couponfact c inner join \
        gm_datedimension d on c.date_id=d.date_id where c.data_type='TOTAL' ";
        if dtstart:
            query = query + where_and + "DATE(d.date) >= %(dtstart)s "
            filters['dtstart'] = dtstart
        if dtend:
            query = query + where_and + "DATE(d.date) <= %(dtend)s "
            filters['dtend'] = dtend

        all_data = self.get_sql_data(query, filters)
        return map(CustomApiObject, all_data)

class TicketStatusResource(CustomBaseResource):
    """
    It is a preferences resource
    """
    id = fields.CharField(attribute="id")
    name = fields.CharField(attribute="name")
    value = fields.CharField(attribute='value', null=True)

    class Meta:
        resource_name = 'ticket-status'
        authentication = AccessTokenAuthentication()
        object_class = CustomApiObject
    
    def get_ticket_count(self, request, status):
        status = str(status)
        if request.user.groups.filter(name=Roles.SDOWNERS):
            assignee_id = get_model('ServiceDeskUser').objects.get(user_profile__user_id=int(request.user.id)).id
            data = self.get_sql_data("select count(*) as count from gm_feedback where status=%(status)s and assignee_id=%(assignee_id)s",
                     filters={'status' : status, 'assignee_id' : assignee_id})
        
        elif request.user.groups.filter(name__in=[Roles.SDMANAGERS, Roles.DEALERADMIN]):
            data = self.get_sql_data("select count(*) as count from gm_feedback where status=%(status)s",
                                 filters={'status' : status})
        
        elif request.user.groups.filter(name=Roles.DEALERS):
            reporter_id = get_model('ServiceDeskUser').objects.get(user_profile__user_id=int(request.user.id)).id
            data = self.get_sql_data("select count(*) as count from gm_feedback where status=%(status)s and reporter_id=%(reporter_id)s",
                     filters={'status' : status, 'reporter_id' : reporter_id})
            
        return get_set_cache('gm_ticket_count' + status, data[0]['count'])
    
    def get_sql_data(self, query, filters={}):
        conn = connections[settings.BRAND]
        cursor = conn.cursor()
        cursor.execute(query, filters)
        data = dictfetchall(cursor)
        conn.close()
        return data
        
    def obj_get_list(self, bundle, **kwargs):
        self.is_authenticated(bundle.request)
        tickets_open = self.get_ticket_count(bundle.request, TicketStatus.OPEN)
        tickets_progress = self.get_ticket_count(bundle.request, TicketStatus.IN_PROGRESS)
        tickets_pending = self.get_ticket_count(bundle.request, TicketStatus.PENDING)
        tickets_resolved = self.get_ticket_count(bundle.request, TicketStatus.RESOLVED)
        tickets_closed = self.get_ticket_count(bundle.request, TicketStatus.CLOSED)
        tickets_raised = tickets_open + tickets_progress + tickets_pending + tickets_resolved + tickets_closed 

        return map(CustomApiObject, [
                                     create_dict(["1", "Tickets Raised",
                                                  tickets_raised]),
                                     create_dict(["2", "Tickets Open",
                                                  tickets_open]),
                                     create_dict(["3", "Tickets In Progress",
                                                  tickets_progress]),
                                     create_dict(["4", "Tickets Pending",
                                                 tickets_pending]),
                                     create_dict(["5", "Tickets Resolved",
                                                 tickets_resolved]),
                                     create_dict(["6", "Tickets Closed",
                                                 tickets_closed])
                                     ]
                   )

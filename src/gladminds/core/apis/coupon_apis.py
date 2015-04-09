from tastypie.constants import ALL_WITH_RELATIONS, ALL
from tastypie.authorization import DjangoAuthorization
from tastypie import fields
import json
import logging
from django.conf.urls import url
from gladminds.core.apis.base_apis import CustomBaseModelResource
from gladminds.core.apis.authentication import AccessTokenAuthentication
from gladminds.core.apis.authorization import MultiAuthorization
from tastypie.authentication import MultiAuthentication
from gladminds.core.model_fetcher import models
from django.core.serializers.json import DjangoJSONEncoder
from django.conf import settings
from django.http.response import HttpResponse,HttpResponseBadRequest
from gladminds.core.core_utils.utils import dictfetchall
from django.db import connections
from tastypie.utils.urls import trailing_slash
from gladminds.core.apis.product_apis import ProductResource
from gladminds.core.apis.user_apis import ServiceAdvisorResource
import datetime

LOG = logging.getLogger('gladminds')

class CouponDataResource(CustomBaseModelResource):
    product = fields.ForeignKey(ProductResource, 'product', full=True)
    service_advisor = fields.ForeignKey(ServiceAdvisorResource, 'service_advisor',
                                        full=True, null=True, blank=True)

    class Meta:
        queryset = models.CouponData.objects.all()
        resource_name = "coupons"
        authorization = MultiAuthorization(DjangoAuthorization())
        authentication = MultiAuthentication(AccessTokenAuthentication())
        detail_allowed_methods = ['get']
        always_return_data = True
        filtering = {
                        "service_type": ALL,
                        "status": ALL,
                        "closed_date": ['gte', 'lte'],
                        "product": ALL_WITH_RELATIONS,
                        "unique_service_coupon": ALL
                     }
        
    def prepend_urls(self):
        return [
                 url(r"^(?P<resource_name>%s)/closed-ticket-count%s" % (self._meta.resource_name,trailing_slash()),
                                                        self.wrap_view('closed_ticket_count'), name="closed_ticket_count")
                ]
    def get_sql_data(self, query):
        conn = connections[settings.BRAND]
        cursor = conn.cursor()
        cursor.execute(query)
        data = dictfetchall(cursor)
        conn.close()
        return data
        
    def closed_ticket_count(self, request, **kwargs):
        date = request.GET
        year = date.get('year')
        month = date.get('month')
        trans_date = datetime.datetime.now() - datetime.timedelta(days=30)
        try:
            query = "select count(*) as cnt, day(c.closed_date) as day, a.asc_id, e.address, f.first_name \
                                      from gm_coupondata c\
                                      left outer join gm_serviceadvisor s on c.service_advisor_id=s.user_id \
                                      left outer join gm_dealer d on s.dealer_id=d.user_id left outer join \
                                      gm_authorizedservicecenter a on s.asc_id=a.user_id \
                                      left outer join gm_userprofile e on a.user_id = e.user_id \
                                      left outer join auth_user f on a.asc_id = f.username \
                                      where YEAR(closed_date)={0} and MONTH(closed_date)={1} \
                                      and a.last_transaction_date > \"{2}\"\
                                      group by c.closed_date,a.asc_id;".format( year, month, trans_date)
            details = self.get_sql_data(query)
        except Exception as ex:
            LOG.error('Exception while quering data : {0}'.format(ex))
            return HttpResponseBadRequest()
        data =  json.dumps(details, cls=DjangoJSONEncoder)
        return HttpResponse(content=data,content_type='application/json')
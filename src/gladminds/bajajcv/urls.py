from django.conf.urls import patterns, url, include
from gladminds.demo.admin import brand_admin
from gladminds.core import urls as core_urls
from gladminds.core.urls import api_v1
from gladminds.core.apis import user_apis, preferences_apis, coupon_apis, product_apis,\
    audit_apis, dashboard_apis, service_desk_apis, loyalty_apis
from tastypie.api import Api

api_v1 = Api(api_name="v1")

api_v1.register(user_apis.UserProfileResource())
api_v1.register(user_apis.DealerResource())
api_v1.register(user_apis.AuthorizedServiceCenterResource())
api_v1.register(user_apis.ServiceAdvisorResource())
api_v1.register(user_apis.NationalSparesManagerResource())
api_v1.register(user_apis.AreaSparesManagerResource())
api_v1.register(user_apis.PartnerResource())
api_v1.register(user_apis.DistributorResource())
api_v1.register(user_apis.RetailerResource())
api_v1.register(user_apis.MemberResource())
api_v1.register(user_apis.ServiceDeskUserResource())
api_v1.register(user_apis.DepartmentSubCategoriesResource())
api_v1.register(user_apis.BrandDepartmentResource())

api_v1.register(product_apis.ProductTypeResource())
api_v1.register(product_apis.ProductResource())
api_v1.register(product_apis.CustomerTempRegistrationResource())
api_v1.register(product_apis.ProductTypeResource())
api_v1.register(product_apis.SpareMasterResource())
api_v1.register(product_apis.ProductCatalogResource())
api_v1.register(product_apis.SparePartUPCResource())
api_v1.register(product_apis.SparePartPointResource())

api_v1.register(coupon_apis.CouponDataResource())

api_v1.register(loyalty_apis.RedemptionResource())
api_v1.register(loyalty_apis.LoyaltySLAResource())
api_v1.register(loyalty_apis.AccumulationResource())

api_v1.register(service_desk_apis.FeedbackResource())


api_v1.register(preferences_apis.UserPreferenceResource())
api_v1.register(preferences_apis.BrandPreferenceResource())

api_v1.register(audit_apis.SMSLogResource())
api_v1.register(audit_apis.DataFeedLogResource())

api_v1.register(dashboard_apis.OverallStatusResource())
api_v1.register(dashboard_apis.FeedStatusResource())
api_v1.register(dashboard_apis.SMSReportResource())
api_v1.register(dashboard_apis.CouponReportResource())

urlpatterns = patterns('',
    url(r'^site-info/$', 'gladminds.demo.views.site_info', name='site_info'),
    url(r'^admin/', include(brand_admin.urls)),
    url(r'', include(api_v1.urls)),
    url(r'', include(core_urls))
    
)
from django.conf.urls import patterns, url, include
from gladminds.bajajcv.admin import brand_admin
from gladminds.core import urls as core_urls
from gladminds.core.apis import user_apis 
from gladminds.core.urls import api_v1
from gladminds.bajajcv.services.loyalty.loyalty import LoyaltyService
from tastypie.api import Api
from gladminds.core.apis import loyalty_apis, product_apis

loyalty = LoyaltyService

loyalty_v1 = Api(api_name="loyalty/v1")
loyalty_v1.register(user_apis.UserResource())
loyalty_v1.register(user_apis.UserProfileResource())
loyalty_v1.register(loyalty_apis.NSMResource())
loyalty_v1.register(loyalty_apis.ASMResource())
loyalty_v1.register(loyalty_apis.PartnerResource())
loyalty_v1.register(loyalty_apis.DistributorResource())
loyalty_v1.register(loyalty_apis.RetailerResource())
loyalty_v1.register(product_apis.ProductTypeResource())
loyalty_v1.register(loyalty_apis.SpareMasterResource())
loyalty_v1.register(loyalty_apis.RedemptionResource())
loyalty_v1.register(loyalty_apis.ProductResource())
loyalty_v1.register(loyalty_apis.SparePartUPCResource())
loyalty_v1.register(loyalty_apis.SparePartPointResource())
loyalty_v1.register(loyalty_apis.LoyaltySLAResource())
loyalty_v1.register(loyalty_apis.MemberResource())
loyalty_v1.register(loyalty_apis.AccumulationResource())
loyalty_v1.register(loyalty_apis.CommentThreadResource())
loyalty_v1.register(loyalty_apis.WelcomeKitResource())
loyalty_v1.register(loyalty_apis.DiscrepantAccumulationResource())

urlpatterns = patterns('',
    url(r'', include(brand_admin.urls)),
    url(r'', include(loyalty_v1.urls)),
    url(r'',include(core_urls)),
    url(r'^welcome', loyalty.send_welcome_message, name='send_welcome_message'),
    url(r'^kit/download/(?P<choice>[a-zA-Z0-9]+)$', loyalty.download_welcome_kit, name='download_welcome_kit'),
)
from tastypie.api import Api
from gladminds.afterbuy.apis import product_apis

api_v1 = Api(api_name="afterbuy/v1")
api_v1.register(product_apis.ProductResources())

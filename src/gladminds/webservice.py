from django.views.decorators.csrf import csrf_exempt
from spyne.application import Application
from spyne.decorator import srpc
from spyne.model.complex import Array
from spyne.model.complex import ComplexModel
from spyne.model.complex import Iterable
from spyne.model.primitive import Integer,DateTime,Decimal
from spyne.model.primitive import Unicode, Mandatory
from spyne.protocol.soap import Soap11
from spyne.server.django import DjangoApplication
from spyne.server.wsgi import WsgiApplication
from spyne.service import ServiceBase
from spyne.util.wsgi_wrapper import WsgiMounter

from gladminds.feed import BrandProductTypeFeed, DealerAndServiceAdvisorFeed, ProductDispatchFeed, ProductPurchaseFeed
from gladminds.soap_authentication import AuthenticationService

tns = "http://api.gladmindsplatform.co/api/v1/bajaj/feed/"
success = "SUCCESS"
failed = "FAILURE"

class AuthenticationModel(ComplexModel):
    UserName = Unicode(min_occurs=1, nillable=False)
    Password = Unicode(min_occurs=1, nillable=False)
        
class BrandModel(ComplexModel):
    BRAND_ID = Unicode
    BRAND_NAME = Unicode
    PRODUCT_TYPE = Unicode
    PRODUCT_NAME = Unicode
    TIMESTAMP = DateTime

class BrandModelList(AuthenticationModel):
    BrandData = Array(BrandModel)
    
class DealerModel(ComplexModel):
    KUNNR = Unicode
    ADDRESS = Unicode
    SER_ADV_ID = Unicode
    SER_ADV_NAME = Unicode
    SER_ADV_MOBILE = Unicode
    TIMESTAMP = DateTime

class DealerModelList(AuthenticationModel):
    DealerData = Array(DealerModel)

class ProductDispatchModel(ComplexModel):
    CHASSIS = Unicode
    PRODUCT_TYPE = Unicode 
    VEC_DIS_DT = DateTime
    KUNNR = Unicode
    UCN_NO = Unicode
    DAYS_LIMIT_FROM = Decimal
    DAYS_LIMIT_TO = Decimal
    KMS_FROM = Decimal
    KMS_TO = Decimal
    SERVICE_TYPE = Unicode
    TIMESTAMP = DateTime

class ProductDispatchModelList(AuthenticationModel):
    ProductDispatchData = Array(ProductDispatchModel)

class ProductPurchaseModel(ComplexModel):
    CHASSIS = Unicode
    CUSTOMER_ID = Unicode
    CUST_MOBILE = Unicode
    CUSTOMER_NAME = Unicode
    CITY = Unicode
    STATE = Unicode
    PIN_NO = Unicode
    VEH_SL_DT = DateTime
    VEH_REG_NO = Unicode
    VEH_SL_DLR = Unicode
    ENGINE = Unicode
    KUNNR = Unicode
    TIMESTAMP = DateTime

class ProductPurchaseModelList(AuthenticationModel):
    ProductPurchaseData = Array(ProductPurchaseModel)
    
class BrandService(ServiceBase):
    
    @srpc(BrandModelList, _returns=Unicode)
    def postBrand(ObjectList):
        try:
            brand_list = [] 
            for brand in ObjectList.BrandData:
                brand_list.append({
                    'brand_id':brand.BRAND_ID, 
                    'brand_name': brand.BRAND_NAME, 
                    'product_type': brand.PRODUCT_TYPE, 
                    'product_name'  : brand.PRODUCT_NAME,                
                })
            brand_obj = BrandProductTypeFeed(data_source  = brand_list)
            brand_obj.import_data()
            return success
        except Exception as ex:
            print "BrandService: {0}".format(ex)
            return failed
            
class DealerService(ServiceBase):
    
    @srpc(DealerModelList, _returns=Unicode)
    def postDealer(ObjectList):
        try:
            dealer_list = []
            for dealer in ObjectList.DealerData:
                dealer_list.append({
                    'dealer_id' : dealer.KUNNR,
                    'address' : dealer.ADDRESS,
                    'service_advisor_id' : dealer.SER_ADV_ID,
                    'name' : dealer.SER_ADV_NAME,
                    'phone_number': dealer.SER_ADV_MOBILE
                })
            dealer_obj = DealerAndServiceAdvisorFeed(data_source  = dealer_list)
            dealer_obj.import_data()
            return success
        except Exception as ex:
            print "DealerService: {0}".format(ex)
            return failed 


class ProductDispatchService(ServiceBase):

    @srpc(ProductDispatchModelList, _returns=Unicode)
    def postProductDispatch(ObjectList):
        try:
            product_dispatch_list = []
            for product in  ObjectList.ProductDispatchData:
                product_dispatch_list.append({
                        'vin' : product.CHASSIS,
                        'product_type': product.PRODUCT_TYPE,
                        'invoice_date': product.VEC_DIS_DT,
                        'dealer_id' : product.KUNNR,
                        'unique_service_coupon' : product.UCN_NO,
                        'valid_days' : product.DAYS_LIMIT_TO,
                        'valid_kms' : product.KMS_TO,
                        'service_type' : product.SERVICE_TYPE
                    })
            dispatch_obj = ProductDispatchFeed(data_source  = product_dispatch_list)
            dispatch_obj.import_data()
            return success
        except Exception as ex:
            print "ProductDispatchService: {0}".format(ex)
            return failed

class ProductPurchaseService(ServiceBase):
    
    @srpc(ProductPurchaseModelList, _returns=Unicode)
    def postProductPurchase(ObjectList):
        try:
            product_purchase_list = []
            for product in ObjectList.ProductPurchaseData:
                product_purchase_list = ({
                        'vin' : product.CHASSIS,
                        'sap_customer_id' : product.CUSTOMER_ID,
                        'customer_phone_number' : product.CUST_MOBILE,
                        'customer_name' : product.CUSTOMER_NAME,
                        'city' : product.CITY,
                        'state' : product.STATE,
                        'pin_no' : product.PIN_NO,
                        'product_purchase_date' : product.VEH_SL_DT,
                })
            purchase_obj = ProductPurchaseFeed(data_source  = product_purchase_list)
            purchase_obj.import_data()
            return success
        except Exception as ex:
            print "ProductPurchaseService: {0}".format(ex)
            return  failed

def _on_method_call(ctx):
    print "============================="
    print "Getting feed with ctx: %s" % ctx
    print ctx.in_object
    print "============================="
    if ctx.in_object is None:
        raise ArgumentError("Request doesn't contain data")
    auth_obj = AuthenticationService(username = ctx.in_object.ObjectList.UserName, password = ctx.in_object.ObjectList.UserName)
    auth_obj.authenticate()
     
BrandService.event_manager.add_listener('method_call', _on_method_call)
DealerService.event_manager.add_listener('method_call', _on_method_call)
ProductDispatchService.event_manager.add_listener('method_call', _on_method_call)
ProductPurchaseService.event_manager.add_listener('method_call', _on_method_call)

all_app = Application([BrandService, DealerService,ProductDispatchService, ProductPurchaseService],
    tns=tns,
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)

brand_app = Application([BrandService],
    tns=tns,
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)

dealer_app = Application([DealerService],
    tns=tns,
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)

dispatch_app = Application([ProductDispatchService],
    tns=tns,
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)

purchase_app = Application([ProductPurchaseService],
    tns=tns,
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)

all_service = csrf_exempt(DjangoApplication(all_app))
brand_service = csrf_exempt(DjangoApplication(brand_app))
dealer_service = csrf_exempt(DjangoApplication(dealer_app))
dispatch_service = csrf_exempt(DjangoApplication(dispatch_app))
purchase_service = csrf_exempt(DjangoApplication(purchase_app))

from django.views.decorators.csrf import csrf_exempt
from spyne.application import Application
from spyne.decorator import srpc
from spyne.model.complex import Array
from spyne.model.complex import ComplexModel
from spyne.model.complex import Iterable
from spyne.model.primitive import Integer,Decimal, Date
from spyne.model.primitive import Unicode, Mandatory
from spyne.protocol.soap import Soap11
from spyne.server.django import DjangoApplication
from spyne.server.wsgi import WsgiApplication
from spyne.service import ServiceBase
from spyne.util.wsgi_wrapper import WsgiMounter

from gladminds.feed import SAPFeed
from gladminds.soap_authentication import AuthenticationService
import logging
from gladminds import settings


logger = logging.getLogger("gladminds")



pattern = r'(\d{4})-(\d{2})-(\d{2})(\d{2})(\d{2})(\d{2})'
tns = "http://api.gladmindsplatform.co/api/v1/bajaj/feed/"
success = "SUCCESS"
failed = "FAILURE"

class AuthenticationModel(ComplexModel):
    __namespace__ = tns
    UserName = Unicode(min_occurs=1, nillable=False)
    Password = Unicode(min_occurs=1, nillable=False)
        
class BrandModel(ComplexModel):
    __namespace__ = tns
    BRAND_ID = Unicode
    BRAND_NAME = Unicode
    PRODUCT_TYPE = Unicode
    PRODUCT_NAME = Unicode
    TIMESTAMP = Unicode(pattern = pattern)

class BrandModelList(ComplexModel):
    __namespace__ = tns
    BrandData = Array(BrandModel)
    
class DealerModel(ComplexModel):
    __namespace__ = tns
    KUNNR = Unicode
    ADDRESS = Unicode
    SER_ADV_ID = Unicode
    SER_ADV_NAME = Unicode
    SER_ADV_MOBILE = Unicode
    ACTIVE_FLAG = Unicode
    TIMESTAMP = Unicode(pattern = pattern)

class DealerModelList(ComplexModel):
    __namespace__ = tns
    DealerData = Array(DealerModel)

class ProductDispatchModel(ComplexModel):
    __namespace__ = tns
    CHASSIS = Unicode
    PRODUCT_TYPE = Unicode 
    VEC_DIS_DT = Date
    KUNNR = Unicode
    UCN_NO = Unicode
    DAYS_LIMIT_FROM = Decimal
    DAYS_LIMIT_TO = Decimal
    KMS_FROM = Decimal
    KMS_TO = Decimal
    SERVICE_TYPE = Unicode
    TIMESTAMP = Unicode(pattern = pattern)

class ProductDispatchModelList(ComplexModel):
    __namespace__ = tns
    ProductDispatchData = Array(ProductDispatchModel)

class ProductPurchaseModel(ComplexModel):
    __namespace__ = tns
    CHASSIS = Unicode
    CUSTOMER_ID = Unicode
    CUST_MOBILE = Unicode
    CUSTOMER_NAME = Unicode
    CITY = Unicode
    STATE = Unicode
    PIN_NO = Unicode
    VEH_SL_DT = Date
    VEH_REG_NO = Unicode
    VEH_SL_DLR = Unicode
    KUNNR = Unicode
    TIMESTAMP = Unicode(pattern = pattern)
    ENGINE = Unicode

class ProductPurchaseModelList(ComplexModel):
    __namespace__ = tns
    ProductPurchaseData = Array(ProductPurchaseModel)
    
class BrandService(ServiceBase):
    __namespace__ = tns
    @srpc(BrandModelList, AuthenticationModel,  _returns=Unicode)
    def postBrand(ObjectList, Credential):
        try:
            brand_list = [] 
            for brand in ObjectList.BrandData:
                brand_list.append({
                    'brand_id':brand.BRAND_ID, 
                    'brand_name': brand.BRAND_NAME, 
                    'product_type': brand.PRODUCT_TYPE, 
                    'product_name'  : brand.PRODUCT_NAME,                
                })
            save_to_db(feed_type = 'brand', data_source = brand_list)
            return success
        except Exception as ex:
            print "BrandService: {0}".format(ex)
            return failed


class DealerService(ServiceBase):
    __namespace__ = tns

    @srpc(DealerModelList, AuthenticationModel,_returns=Unicode)
    def postDealer(ObjectList,Credential):
        try:
            dealer_list = []
            for dealer in ObjectList.DealerData:
                dealer_list.append({
                    'dealer_id' : dealer.KUNNR,
                    'address' : dealer.ADDRESS,
                    'service_advisor_id' : dealer.SER_ADV_ID,
                    'name' : dealer.SER_ADV_NAME,
                    'phone_number': '{0}{1}'.format(settings.MOBILE_NUM_FORMAT, dealer.SER_ADV_MOBILE),
                    'status': dealer.ACTIVE_FLAG
                })
            save_to_db(feed_type = 'dealer', data_source = dealer_list)
            return success
        except Exception as ex:
            print "DealerService: {0}".format(ex)
            return failed 


class ProductDispatchService(ServiceBase):
    __namespace__ = tns
    @srpc(ProductDispatchModelList,AuthenticationModel, _returns=Unicode)
    def postProductDispatch(ObjectList, Credential):
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
                        'service_type' : product.SERVICE_TYPE,
                    })
            save_to_db(feed_type = 'dispatch', data_source = product_dispatch_list)
            return success
        except Exception as ex:
            print "ProductDispatchService: {0}".format(ex)
            return failed

class ProductPurchaseService(ServiceBase):
    __namespace__ = tns
    @srpc(ProductPurchaseModelList,AuthenticationModel, _returns=Unicode)
    def postProductPurchase(ObjectList, Credential):
        try:
            product_purchase_list = []
            for product in ObjectList.ProductPurchaseData:
                product_purchase_list.append({
                        'vin' : product.CHASSIS,
                        'sap_customer_id' : product.CUSTOMER_ID,
                        'customer_phone_number' :'+91'+product.CUST_MOBILE,
                        'customer_name' : product.CUSTOMER_NAME,
                        'city' : product.CITY,
                        'state' : product.STATE,
                        'pin_no' : product.PIN_NO,
                        'product_purchase_date' : product.VEH_SL_DT,
                        'engine' : product.ENGINE
                })
            save_to_db(feed_type = 'purchase', data_source = product_purchase_list)
            return success
        except Exception as ex:
            print "ProductPurchaseService: {0}".format(ex)
            return  failed

def save_to_db(feed_type = None, data_source = []):
    sap_obj = SAPFeed()
    sap_obj.import_to_db(feed_type = feed_type, data_source = data_source)

def _on_method_call(ctx):
    print "Getting feed data: %s" % ctx.in_object
    logger.info("Getting feed data: %s" % ctx.in_object)
    if ctx.in_object is None:
        raise ArgumentError("Request doesn't contain data")
    auth_obj = AuthenticationService(username = ctx.in_object.Credential.UserName, password = ctx.in_object.Credential.UserName)
    auth_obj.authenticate()
     
BrandService.event_manager.add_listener('method_call', _on_method_call)
DealerService.event_manager.add_listener('method_call', _on_method_call)
ProductDispatchService.event_manager.add_listener('method_call', _on_method_call)
ProductPurchaseService.event_manager.add_listener('method_call', _on_method_call)

all_app = Application([BrandService, DealerService, ProductDispatchService, ProductPurchaseService],
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

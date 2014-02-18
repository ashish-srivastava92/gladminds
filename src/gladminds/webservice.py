from django.views.decorators.csrf import csrf_exempt
from spyne.application import Application
from spyne.decorator import srpc
from spyne.model.complex import ComplexModel
from spyne.model.complex import Iterable
from spyne.model.primitive import Integer,DateTime,Decimal
from spyne.model.primitive import Unicode, Mandatory
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from spyne.service import ServiceBase
from spyne.util.wsgi_wrapper import WsgiMounter
from spyne.server.django import DjangoApplication

from gladminds.feed import BrandProductTypeFeed, DealerAndServiceAdvisorFeed, ProductDispatchFeed, ProductPurchaseFeed
from gladminds.soap_authentication import BasicAuthentication


tns = 'gladminds.webservice'
success = "success"
failed = "failed"

class BrandService(ServiceBase):
    __tns__ = 'gladminds.webservice.authentication'
    
    @srpc(Unicode, Unicode, Unicode, Unicode, DateTime, _returns=Unicode)
    def postBrand(BRAND_ID, BRAND_NAME, PRODUCT_TYPE, PRODUCT_NAME, TIMESTAMP):
        try:
            brand_data = [{
                'brand_id':BRAND_ID, 
                'brand_name': BRAND_NAME, 
                'product_type': PRODUCT_TYPE, 
                'product_name': PRODUCT_NAME,
            }]
            brand_obj = BrandProductTypeFeed(data_source  = brand_data)
            brand_obj.import_data()
            return success
        except Exception as ex:
            print "BrandService: {0}".format(ex)
            return failed
            
class DealerService(ServiceBase):
    __tns__ = 'gladminds.webservice.authentication'
    
    @srpc(Unicode, Unicode, Unicode,Unicode, Unicode, DateTime, _returns=Unicode)
    def postDealer(KUNNR, ADDRESS, SER_ADV_ID, SER_ADV_NAME, SER_ADV_MOBILE, TIMESTAMP):
        try:
            dealer_data = [{
                'dealer_id' : KUNNR,
                'address' : ADDRESS,
                'service_advisor_id' : SER_ADV_ID,
                'name' : SER_ADV_NAME,
                'phone_number': SER_ADV_MOBILE
            }]
            dealer_obj = DealerAndServiceAdvisorFeed(data_source  = dealer_data)
            dealer_obj.import_data()
            return success
        except Exception as ex:
            print "DealerService: {0}".format(ex)
            return failed 

class ProductDispatchService(ServiceBase):
    __tns__ = 'gladminds.webservice.authentication'

    @srpc(Unicode, Unicode, DateTime, Unicode, Unicode, Decimal, Decimal, Decimal, Decimal, Unicode, DateTime, _returns=Unicode)
    def postProductDispatch(CHASSIS, PRODUCT_TYPE, VEC_DIS_DT, KUNNR, UCN_NO, DAYS_LIMIT_FROM, DAYS_LIMIT_TO, KMS_FROM, KMS_TO, SERVICE_TYPE, TIMESTAMP):
        try:
            product_dispatch_data = [{
                    'vin' : CHASSIS,
                    'product_type': PRODUCT_TYPE,
                    'invoice_date': VEC_DIS_DT,
                    'dealer_id' : KUNNR,
                    'unique_service_coupon' : UCN_NO,
                    'valid_days' : DAYS_LIMIT_TO,
                    'valid_kms' : KMS_TO,
                    'service_type' : SERVICE_TYPE
                }]
            dispatch_obj = ProductDispatchFeed(data_source  = product_dispatch_data)
            dispatch_obj.import_data()
            return success
        except Exception as ex:
            print "ProductDispatchService: {0}".format(ex)
            return failed

class ProductPurchaseService(ServiceBase):
    __tns__ = 'gladminds.webservice.authentication'
    
    @srpc(Unicode, Unicode, Unicode, Unicode, Unicode, Unicode, Unicode, DateTime, Unicode, Unicode, Unicode, Unicode, DateTime, _returns=Unicode)
    def postProductPurchase(CHASSIS, CUSTOMER_ID, CUST_MOBILE, CUSTOMER_NAME, CITY, STATE, PIN_NO, VEH_SL_DT, VEH_REG_NO, VEH_SL_DLR, ENGINE, KUNNR, TIMESTAMP):
        try:
            product_purchase_data = [{
                    'vin' : CHASSIS,
                    'sap_customer_id' : CUSTOMER_ID,
                    'customer_phone_number' : CUST_MOBILE,
                    'customer_name' : CUSTOMER_NAME,
                    'city' : CITY,
                    'state' : STATE,
                    'pin_no' : PIN_NO,
                    'product_purchase_date' : VEH_SL_DT,
            }]
            purchase_obj = ProductPurchaseFeed(data_source  = product_purchase_data)
            purchase_obj.import_data()
            return success
        except Exception as ex:
            print "ProductPurchaseService: {0}".format(ex)
            return  failed

def _on_method_call(ctx):
    transport = ctx.transport
    auth = transport.req_env.get('HTTP_AUTHORIZATION', None)
    obj_auth = BasicAuthentication(auth = auth)
    obj_auth.is_authenticated()
    
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



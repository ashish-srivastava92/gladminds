from spyne.application import Application
from spyne.decorator import srpc
from spyne.service import ServiceBase
from spyne.model.primitive import Integer,DateTime,Decimal
from spyne.model.primitive import Unicode
from spyne.model.complex import Iterable
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from spyne.util.wsgi_wrapper import WsgiMounter

tns = 'gladminds.webservice'
port = 8000
host = '127.0.0.1'

class BrandService(ServiceBase):
    @srpc(Unicode, Unicode, Unicode,Unicode, _returns=Unicode)
    def postBrand(BRAND_ID, BRAND_NAME, PRODUCT_TYPE, PRODUCT_NAME):
        return BRAND_ID

class DealerService(ServiceBase):
    @srpc(Unicode, Unicode, Unicode,Unicode, Unicode, _returns=Unicode)
    def postDealer(DEALER_ID, ADDRESS, SER_ADV_ID, SER_ADV_NAME, SER_ADV_MOBILE):
        pass

class ProductDispatchService(ServiceBase):
    @srpc(Unicode, Unicode, DateTime, Unicode, Unicode, Decimal, Decimal, Decimal, Decimal, Unicode, _returns=Unicode)
    def postProductDispatch(CHASSIS, PRODUCT_TYPE, VEC_DIS_DT, DEALER_ID, UCN_NO, DAYS_LIMIT_FROM, DAYS_LIMIT_TO, KMS_FROM, KMS_TO, SERVICE_TYPE):
        pass

class ProductPurchaseService(ServiceBase):
    @srpc(Unicode, Unicode, Unicode, Unicode, Unicode, Unicode, Unicode, DateTime, _returns=Unicode)
    def postProductPurchase(CHASSIS, CUSTOMER_ID, CUST_MOBILE, CUSTOMER_NAME, CITY, STATE, PIN_NO, PRODUCT_PURCHASE_DATE):
        pass
            

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

# if __name__ == '__main__':
#     # You can use any Wsgi server. Here, we chose
#     # Python's built-in wsgi server but you're not
#     # supposed to use it in production.
#     from wsgiref.simple_server import make_server
#  
#     wsgi_app = WsgiMounter({
#         'brand-feed': brand_app,
#         'dealer-feed': dealer_app,
#         'dispatch-feed': dispatch_app,
#         'purchase-feed': purchase_app,
#     })
#     server = make_server(host, port, wsgi_app)
#     server.serve_forever()
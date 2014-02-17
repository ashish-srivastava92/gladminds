import os
import sys
from productDispatch_server import *
from brand_server import *
from dealer_server import *
from productPurchase_server import *

from ZSI.twisted.wsgi import (SOAPApplication,
                              soapmethod,
                              SOAPHandlerChainFactory)

class ProductDispatchService(SOAPApplication):
    factory = SOAPHandlerChainFactory
    def __call__(self, env, start_response):
        self.env = env
        return SOAPApplication.__call__(self, env, start_response)

    @soapmethod(GetProductDispatchInput.typecode, 
                GetProductDispatchOutput.typecode, 
                operation='getProductDispatch', 
                soapaction='productDispatchSOAP')
    def soap_getProductDispatch(self, request, response, **kw):
        response.RESPONSE_CODE = "SUCCESS"
        return request, response

class ProductPurchaseService(SOAPApplication):
    factory = SOAPHandlerChainFactory
    
    def __call__(self, env, start_response):
        self.env = env
        return SOAPApplication.__call__(self, env, start_response)

    @soapmethod(GetProductPurchaseInput.typecode, 
                GetProductPurchaseOutput.typecode, 
                operation='getProductPurchase', 
                soapaction='productPurchaseSOAP')
    def soap_getProductPurchase(self, request, response, **kw):
        response.RESPONSE_CODE = "SUCCESS"
        return request, response

class BrandService(SOAPApplication):
    factory = SOAPHandlerChainFactory
    
    def __call__(self, env, start_response):
        self.env = env
        return SOAPApplication.__call__(self, env, start_response)

    @soapmethod(GetBrandInput.typecode, 
                GetBrandOutput.typecode, 
                operation='getBrand', 
                soapaction='brandSOAP')
    def soap_getBrand(self, request, response, **kw):
        response.RESPONSE_CODE = "SUCCESS"
        return request, response

class DealerService(SOAPApplication):
    factory = SOAPHandlerChainFactory
    
    def __call__(self, env, start_response):
        self.env = env
        return SOAPApplication.__call__(self, env, start_response)

    @soapmethod(GetDealerInput.typecode, 
                GetDealerOutput.typecode, 
                operation='getDealer', 
                soapaction='dealerSOAP')
    def soap_getDealer(self, request, response, **kw):
        response.RESPONSE_CODE = "SUCCESS"
        return request, response

def main():
    from wsgiref.simple_server import make_server
    from ZSI.twisted.wsgi import WSGIApplication

    application         = WSGIApplication()
    httpd               = make_server('127.0.0.1', 8000, application)
    application['brand-feed'] = BrandService()
    application['dealer-feed'] = DealerService()
    application['dispatch-feed'] = ProductDispatchService()
    application['purchase-feed'] = ProductPurchaseService()
    print "listening..."
    httpd.serve_forever()
    

if __name__ == '__main__':
    main()

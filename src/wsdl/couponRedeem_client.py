##################################################
# file: couponRedeem_client.py
# 
# client stubs generated by "ZSI.generate.wsdl2python.WriteServiceModule"
#     /usr/bin/wsdl2py -b couponRedeem.wsdl
# 
##################################################

from couponRedeem_types import *
import urlparse, types
from ZSI.TCcompound import ComplexType, Struct
from ZSI import client
from ZSI.schema import GED, GTD
import ZSI
from ZSI.generate.pyclass import pyclass_type

# Locator
class couponRedeemLocator:
    couponRedeemSOAP_address = "http://localhost:8000/"
    def getcouponRedeemSOAPAddress(self):
        return couponRedeemLocator.couponRedeemSOAP_address
    def getcouponRedeemSOAP(self, url=None, **kw):
        return couponRedeemSOAPSOAP(url or couponRedeemLocator.couponRedeemSOAP_address, **kw)

# Methods
class couponRedeemSOAPSOAP:
    def __init__(self, url, **kw):
        kw.setdefault("readerclass", None)
        kw.setdefault("writerclass", None)
        # no resource properties
        self.binding = client.Binding(url=url, **kw)
        # no ws-addressing

    # op: getCouponRedeem
    def getCouponRedeem(self, request, **kw):
        if isinstance(request, GetCouponRedeemInput) is False:
            raise TypeError, "%s incorrect request type" % (request.__class__)
        # no input wsaction
        self.binding.Send(None, None, request, soapaction="http://localhost:8000/productPurchase/GetCouponRedeem", **kw)
        # no output wsaction
        response = self.binding.Receive(GetCouponRedeemOutput.typecode)
        return response

GetCouponRedeemInput = GED("urn:ZSI", "CouponRedeemInput").pyclass

GetCouponRedeemOutput = GED("urn:ZSI", "CouponRedeemOutput").pyclass

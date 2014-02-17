##################################################
# file: dealer_types.py
#
# schema types generated by "ZSI.generate.wsdl2python.WriteServiceModule"
#    /usr/bin/wsdl2py -b dealer.wsdl
#
##################################################

import ZSI
import ZSI.TCcompound
from ZSI.schema import LocalElementDeclaration, ElementDeclaration, TypeDefinition, GTD, GED
from ZSI.generate.pyclass import pyclass_type

##############################
# targetNamespace
# urn:ZSI
##############################

class ns0:
    targetNamespace = "urn:ZSI"

    class dealerInput_Dec(ZSI.TCcompound.ComplexType, ElementDeclaration):
        literal = "dealerInput"
        schema = "urn:ZSI"
        def __init__(self, **kw):
            ns = ns0.dealerInput_Dec.schema
            TClist = [ZSI.TC.String(pname="DEALER_ID", aname="_DEALER_ID", minOccurs=1, maxOccurs=1, nillable=False, typed=False, encoded=kw.get("encoded")), ZSI.TC.String(pname="ADDRESS", aname="_ADDRESS", minOccurs=1, maxOccurs=1, nillable=False, typed=False, encoded=kw.get("encoded")), ZSI.TC.String(pname="SER_ADV_ID", aname="_SER_ADV_ID", minOccurs=1, maxOccurs=1, nillable=False, typed=False, encoded=kw.get("encoded")), ZSI.TC.String(pname="SER_ADV_NAME", aname="_SER_ADV_NAME", minOccurs=1, maxOccurs=1, nillable=False, typed=False, encoded=kw.get("encoded")), ZSI.TC.String(pname="SER_ADV_MOBILE", aname="_SER_ADV_MOBILE", minOccurs=1, maxOccurs=1, nillable=False, typed=False, encoded=kw.get("encoded"))]
            kw["pname"] = ("urn:ZSI","dealerInput")
            kw["aname"] = "_dealerInput"
            self.attribute_typecode_dict = {}
            ZSI.TCcompound.ComplexType.__init__(self,None,TClist,inorder=0,**kw)
            class Holder:
                __metaclass__ = pyclass_type
                typecode = self
                def __init__(self):
                    # pyclass
                    self._DEALER_ID = None
                    self._ADDRESS = None
                    self._SER_ADV_ID = None
                    self._SER_ADV_NAME = None
                    self._SER_ADV_MOBILE = None
                    return
            Holder.__name__ = "dealerInput_Holder"
            self.pyclass = Holder

    class dealerOutput_Dec(ZSI.TCcompound.ComplexType, ElementDeclaration):
        literal = "dealerOutput"
        schema = "urn:ZSI"
        def __init__(self, **kw):
            ns = ns0.dealerOutput_Dec.schema
            TClist = [ZSI.TC.String(pname="RESPONSE_CODE", aname="_RESPONSE_CODE", minOccurs=1, maxOccurs=1, nillable=False, typed=False, encoded=kw.get("encoded"))]
            kw["pname"] = ("urn:ZSI","dealerOutput")
            kw["aname"] = "_dealerOutput"
            self.attribute_typecode_dict = {}
            ZSI.TCcompound.ComplexType.__init__(self,None,TClist,inorder=0,**kw)
            class Holder:
                __metaclass__ = pyclass_type
                typecode = self
                def __init__(self):
                    # pyclass
                    self._RESPONSE_CODE = None
                    return
            Holder.__name__ = "dealerOutput_Holder"
            self.pyclass = Holder

# end class ns0 (tns: urn:ZSI)

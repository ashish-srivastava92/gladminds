import logging

from django.conf import settings
from spyne.application import Application
from spyne.decorator import srpc
from spyne.model.complex import Array
from spyne.model.complex import ComplexModel
from spyne.model.complex import Iterable
from spyne.model.primitive import Integer, Decimal, Date, Time, Unicode, Mandatory, Boolean
from spyne.protocol.soap import Soap11
from spyne.server.django import DjangoApplication
from spyne.server.wsgi import WsgiApplication
from spyne.service import ServiceBase
from spyne.util.wsgi_wrapper import WsgiMounter

from gladminds.core import utils
from gladminds.core.managers.audit_manager import feed_failure_log
from gladminds.core.managers.feed_log_remark import FeedLogWithRemark
from gladminds.core.services.part_change.import_feed import SAPFeed
from gladminds.core.soap_authentication import AuthenticationService


logger = logging.getLogger("gladminds")


pattern = r'(\d{4})-(\d{2})-(\d{2})(\d{2})(\d{2})(\d{2})'
date_pattern = r'(\d{4})-(\d{2})-(\d{2})'
time_pattern = r'(\d{2}):(\d{2}):(\d{2})'
tns = settings.WSDL_TNS
SUCCESS = "SUCCESS"
FAILED = "FAILURE"


class AuthenticationModel(ComplexModel):
    __namespace__ = tns
    UserName = Unicode(min_occurs=1, nillable=False)
    Password = Unicode(min_occurs=1, nillable=False)

######################################MOCK SERVICE################################################

class ItemFieldModel(ComplexModel):
    __namespace__ = tns
    BOM_NUMBER = Unicode
    PART_NUMBER = Unicode
    REVISION_NO = Unicode
    QTY = Unicode
    UOM = Unicode
    VALID_FROM = Date(default=None)
    VALID_TO = Date(default=None)
    PLATE_ID = Unicode
    PLATE_TXT = Unicode
    SERIAL_NUMBER = Unicode
    CHANGE_NUMBER = Unicode
    CHANGE_NUMBER_TO = Unicode
    ITEM = Unicode
    ITEM_ID = Unicode
   
class HeaderFieldModel(ComplexModel):
    __namespace__ = tns
    SKU_CODE = Unicode
    PLANT = Unicode
    BOM_TYPE = Unicode
    BOM_NO = Unicode
    CREATED_ON = Date(default=None)
    VALID_FROM = Date(default=None)
    VALID_TO = Date(default=None)
   
     
class TimeStampModel(ComplexModel):
    __namespace__ = tns
    TIMESTAMP = Unicode(pattern=pattern)

class BOMModel(ComplexModel):
    __namespace__ = tns
    BOMTIMESTAMP = TimeStampModel
    HEADERFIELD = Array(HeaderFieldModel)
    ITEMFIELD = Array(ItemFieldModel)
    
class BillOfMaterialList(ComplexModel):
    __namespace__ = tns
    BOMData = Array(BOMModel)

class EcoReleaseModel(ComplexModel):
    __namespace__ = tns
    ECO_NUMBER  = Unicode
    ECO_REL_DATE = Unicode(default=None)
    ECO_DESCRIP = Unicode
    ACTION = Unicode
    PARENT_PART = Unicode
    ADD_PART = Unicode
    ADD_PART_QTY = Decimal
    ADD_PART_REV = Unicode
    ADD_PART_LOC_CODE = Unicode
    DEL_PART = Unicode
    DEL_PART_QTY = Decimal
    DEL_PART_REV = Decimal
    DEL_PART_LOC_CODE = Unicode
    MODELS_APPLICABLE = Unicode
    SERVICEABILITY = Unicode
    INTERCHANGEABILITY = Unicode
    REASON_FOR_CHANGE = Unicode

class EcoReleaseModelList(ComplexModel):
    __namespace__ = tns
    ECOReleaseData = Array(EcoReleaseModel)
    
class EcoImplementationModel(ComplexModel):
    __namespace__ = tns
    
    CHANGE_NO = Unicode
    CHANGE_DATE = Unicode(default=None)
    CHANGE_TIME = Time(default=None)
    PLANT = Unicode
    ACTION = Unicode
    PARENT_PART = Unicode
    ADDED_PART = Unicode
    ADDED_PART_QTY = Decimal
    DELETED_PART = Unicode
    DELETED_PART_QTY = Decimal
    CHASSIS_NUMBER = Unicode
    ENGINE_NUMBER = Unicode
    ECO_NUMBER = Unicode
    REASON_CODE = Unicode
    REMARKS = Unicode    

class EcoImplementationList(ComplexModel):
    __namespace__ = tns
    EcoImplementationData = Array(EcoImplementationModel)

class ManufactureDataModel(ComplexModel):
    __namespace__ = tns
    CHASSIS  = Unicode
    MATNR = Unicode
    WERKS = Unicode
    VODATE = Date()
    ENGINE = Unicode

class ManufactureDataModelList(ComplexModel):
    __namespace__ = tns
    ManufactureData = Array(ManufactureDataModel)

class ManufactureDataService(ServiceBase):
    __namespace__ = tns

    @srpc(ManufactureDataModelList, AuthenticationModel,  _returns=Unicode)
    def postManufactureData(ObjectList, Credential):
        data_list = []
        feed_remark = FeedLogWithRemark(len(ObjectList.ManufactureData), feed_type='Manufacture data Feed', action='Received', status=True)

        for data_obj in ObjectList.ManufactureData:
            data_list.append({
                            'product_id' : data_obj.CHASSIS,
                            'material_number' : data_obj.MATNR,
                            'plant' : data_obj.WERKS,
                            'engine' : data_obj.ENGINE,
                            'vehicle_off_line_date' : data_obj.VODATE
                            })

        feed_remark = save_to_db(feed_type='manufacture_data', data_source=data_list, feed_remark=feed_remark)
        feed_remark.save_to_feed_log()
        return get_response(feed_remark)

class ECOImplementationService(ServiceBase):
    __namespace__ = tns

    @srpc(EcoImplementationList, AuthenticationModel,  _returns=Unicode)
    def postECOImplementation(ObjectList, Credential):
        eco_list = []
        feed_remark = FeedLogWithRemark(len(ObjectList.EcoImplementationData), feed_type='ECO Implementation Feed', action='Received', status=True)

        for eco_obj in ObjectList.EcoImplementationData:
            eco_list.append({
                            'change_no' :  eco_obj.CHANGE_NO,
                            'change_date' :  eco_obj.CHANGE_DATE,
                            'change_time' :  eco_obj.CHANGE_TIME,
                            'plant' :  eco_obj.PLANT,
                            'action' :  eco_obj.ACTION,
                            'parent_part' :  eco_obj.PARENT_PART,
                            'added_part' :  eco_obj.ADDED_PART,
                            'added_part_qty' :  eco_obj.ADDED_PART_QTY,
                            'deleted_part' :  eco_obj.DELETED_PART,
                            'deleted_part_qty' :  eco_obj.DELETED_PART_QTY,
                            'chassis_number' :  eco_obj.CHASSIS_NUMBER,
                            'engine_number' :  eco_obj.ENGINE_NUMBER,
                            'eco_number' :  eco_obj.ECO_NUMBER,
                            'reason_code' :  eco_obj.REASON_CODE,
                            'remarks' :  eco_obj.REMARKS,
                            })

        feed_remark = save_to_db(feed_type='eco_implementation', data_source=eco_list, feed_remark=feed_remark)
        feed_remark.save_to_feed_log()
        return get_response(feed_remark)
    

class ECOReleaseService(ServiceBase):
    __namespace__ = tns

    @srpc(EcoReleaseModelList, AuthenticationModel,  _returns=Unicode)
    def postECORelease(ObjectList, Credential):
        eco_list = []
        feed_remark = FeedLogWithRemark(len(ObjectList.ECOReleaseData), feed_type='ECO Release Feed', action='Received', status=True)

        for eco_obj in ObjectList.ECOReleaseData:
            eco_list.append({
                            'eco_number' :  eco_obj.ECO_NUMBER,
                            'eco_release_date' :  eco_obj.ECO_REL_DATE,
                            'eco_description' :  eco_obj.ECO_DESCRIP,
                            'action' :  eco_obj.ACTION,
                            'parent_part' :  eco_obj.PARENT_PART,
                            'add_part' :  eco_obj.ADD_PART,
                            'add_part_qty' :  eco_obj.ADD_PART_QTY,
                            'add_part_rev' :  eco_obj.ADD_PART_REV,
                            'add_part_loc_code' :  eco_obj.ADD_PART_LOC_CODE,
                            'del_part' :  eco_obj.DEL_PART,
                            'del_part_qty' :  eco_obj.DEL_PART_QTY,
                            'del_part_rev' :  eco_obj.DEL_PART_REV,
                            'del_part_loc_code' :  eco_obj.DEL_PART_LOC_CODE,
                            'models_applicable' :  eco_obj.MODELS_APPLICABLE,
                            'serviceability' :  eco_obj.SERVICEABILITY,
                            'interchangebility' :  eco_obj.INTERCHANGEABILITY,
                            'reason_for_change' :  eco_obj.REASON_FOR_CHANGE,
                            })

        feed_remark = save_to_db(feed_type='eco_release', data_source=eco_list, feed_remark=feed_remark)
        feed_remark.save_to_feed_log()
        return get_response(feed_remark)

class BillOfMaterialService(ServiceBase):
    __namespace__ = tns
    @srpc(BillOfMaterialList, AuthenticationModel,  _returns=Unicode)
    def postBillOfMaterial(ObjectList, Credential):
        bom_header_list = []
        bom_item_list = []
        header_count = 0 
        item_count = 0
        
        for bom_obj in ObjectList.BOMData:
            header_count = header_count + len(bom_obj.HEADERFIELD)
            item_count = item_count + len(bom_obj.ITEMFIELD)
            
            for bom in bom_obj.HEADERFIELD:
                bom_header_list.append({
                             'sku_code': bom.SKU_CODE,
                             'plant': bom.PLANT,
                             'bom_type': bom.BOM_TYPE,
                             'bom_number_header': bom.BOM_NO,
                             'created_on': bom.CREATED_ON,
                             'valid_from_header': bom.VALID_FROM,
                             'valid_to_header': bom.VALID_TO,
                             })
            
            for bom in bom_obj.ITEMFIELD:
                bom_item_list.append({
                            'bom_number' : bom.BOM_NUMBER, 
                            'part_number' : bom.PART_NUMBER,  
                            'revision_number' : bom.REVISION_NO, 
                            'quantity' : bom.QTY,
                            'uom' :bom.UOM,
                            'valid_from' : bom.VALID_FROM,
                            'valid_to' : bom.VALID_TO,
                            'plate_id' : bom.PLATE_ID,
                            'plate_txt' : bom.PLATE_TXT,
                            'serial_number' : bom.SERIAL_NUMBER,
                            'change_number' : bom.CHANGE_NUMBER,
                            'change_number_to' : bom.CHANGE_NUMBER_TO,
                            'item' : bom.ITEM,
                            'item_id' : bom.ITEM_ID,
                            'timestamp':bom_obj.BOMTIMESTAMP.TIMESTAMP
                            })

        feed_remark_header = FeedLogWithRemark(header_count, feed_type='BOM Header Feed', action='Received', status=True)        
        feed_remark_item = FeedLogWithRemark(item_count, feed_type='BOM Item Feed', action='Received', status=True)
        feed_remark_item = save_to_db(feed_type='bomitem', data_source=[bom_item_list, bom_header_list], feed_remark=[feed_remark_item, feed_remark_header])
        feed_remark_item[1].save_to_feed_log()
        feed_remark_item[0].save_to_feed_log()
        item_log = get_response(feed_remark_item[0])
        header_log = get_response(feed_remark_item[1])
        
        if item_log == SUCCESS and  item_log == header_log:
            return SUCCESS
        else:
            return FAILED

def get_response(feed_remark):
    if feed_remark.failed_feeds > 0:
        remarks = feed_remark.remarks.elements()
        for remark in remarks:
            feed_failure_log(brand=settings.BRAND, feed_type=feed_remark.feed_type, reason=remark)
        return FAILED
    else:
        return SUCCESS

def save_to_db(feed_type=None, data_source=[], feed_remark=None):
    sap_obj = SAPFeed()
    return sap_obj.import_to_db(feed_type=feed_type, data_source=data_source,
                                 feed_remark=feed_remark)


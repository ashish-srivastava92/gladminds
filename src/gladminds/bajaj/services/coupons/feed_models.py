from django.views.decorators.csrf import csrf_exempt
from spyne.application import Application
from spyne.decorator import srpc
from spyne.model.complex import Array
from spyne.model.complex import ComplexModel
from spyne.model.complex import Iterable
from spyne.model.primitive import Integer, Decimal, Date, Time
from spyne.model.primitive import Unicode, Mandatory, Boolean
from spyne.protocol.soap import Soap11
from spyne.server.django import DjangoApplication
from spyne.server.wsgi import WsgiApplication
from spyne.service import ServiceBase
from spyne.util.wsgi_wrapper import WsgiMounter

from gladminds.bajaj.services.coupons.import_feed import SAPFeed
from gladminds.core.soap_authentication import AuthenticationService
import logging
from django.conf import settings
import json
from gladminds.core import utils
from gladminds.core.managers.feed_log_remark import FeedLogWithRemark
from gladminds.core.managers.audit_manager import feed_failure_log


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
"""
    Mock service is created to give WSDL File to BAJAJ. 
    There is not other use of it.
"""


class ASCRegistrationModel(ComplexModel):
    __namespace__ = tns
    ASC_NAME = Unicode
    ASC_MOBILE = Unicode
    ASC_EMAIL = Unicode
    ASC_ADDRESS = Unicode
    ASC_ADDRESS_PINCODE = Unicode
    KUNNAR = Unicode


class SARegistrationModel(ComplexModel):
    __namespace__ = tns
    SER_ADV_NAME = Unicode
    SER_ADV_MOBILE = Unicode
    ADDRESS = Unicode
    ACTIVE_FLAG = Unicode
    KUNNR = Unicode
    ASC_ID = Unicode


class CustomerRegistrationModel(ComplexModel):
    __namespace__ = tns
    CUST_MOBILE = Unicode
    VEH_SL_DT = Date
    CHASSIS = Unicode
    CUSTOMER_NAME = Unicode
    CITY = Unicode
    STATE = Unicode
    PIN_NO = Unicode
    VEH_REG_NO = Unicode
    VEH_SL_DLR = Unicode
    KUNNR = Unicode
    ENGINE = Unicode
    ASC_ID = Unicode


class ASCRegisterationService(ServiceBase):
    __namespace__ = tns

    @srpc(ASCRegistrationModel, AuthenticationModel, _returns=Unicode)
    def ascRegistration(ObjectList, Credential):
        pass


class SARegisterationService(ServiceBase):
    __namespace__ = tns

    @srpc(SARegistrationModel, AuthenticationModel, _returns=Unicode)
    def saRegistration(ObjectList, Credential):
        pass


class CustomerRegisterationService(ServiceBase):
    __namespace__ = tns

    @srpc(CustomerRegistrationModel, AuthenticationModel, _returns=Unicode)
    def customerRegistration(ObjectList, Credential):
        pass

mock_app = Application([ASCRegisterationService, SARegisterationService, CustomerRegisterationService],
                      tns=tns,
                      in_protocol=Soap11(validator='lxml'),
                      out_protocol=Soap11()
                      )

mock_service = csrf_exempt(DjangoApplication(mock_app))

######################################MOCK SERVICE################################################


class BrandModel(ComplexModel):
    __namespace__ = tns
    BRAND_ID = Unicode
    BRAND_NAME = Unicode
    PRODUCT_TYPE = Unicode
    PRODUCT_NAME = Unicode
    TIMESTAMP = Unicode(pattern=pattern)


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
    TIMESTAMP = Unicode(pattern=pattern)
    CDMS_FLAG = Boolean

class DealerModelList(ComplexModel):
    __namespace__ = tns
    DealerData = Array(DealerModel)
    
class ASCModel(ComplexModel):
    __namespace__ = tns
    ASC_ID = Unicode
    ASC_NAME = Unicode
    ASC_MOBILE = Unicode
    ASC_EMAIL = Unicode
    ASC_ADDRESS = Unicode
    KUNNAR = Unicode


class ASCModelList(ComplexModel):
    __namespace__ = tns
    ASCData = Array(ASCModel)    


class ProductDispatchModel(ComplexModel):
    __namespace__ = tns
    CHASSIS = Unicode
    PRODUCT_TYPE = Unicode
    VEC_DIS_DT = Date
    KUNNR = Unicode
    UCN_NO = Unicode(default=None)
    DAYS_LIMIT_FROM = Decimal
    DAYS_LIMIT_TO = Decimal
    KMS_FROM = Decimal
    KMS_TO = Decimal
    SERVICE_TYPE = Unicode
    #UCN_Status = Unicode
    TIMESTAMP = Unicode(pattern=pattern)
#     SKU_CODE = Unicode
#     ENGINE = Unicode

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
    TIMESTAMP = Unicode(pattern=pattern)
    ENGINE = Unicode


class ProductPurchaseModelList(ComplexModel):
    __namespace__ = tns
    ProductPurchaseData = Array(ProductPurchaseModel)
    
class OldFscItem(ComplexModel):
    __namespace__ = tns
    KUNNAR = Unicode
    CHASSIS = Unicode
    CHARG = Unicode
    MATNR = Unicode
    SERVICE = Unicode

class OldFscStatusModel(ComplexModel):
    __namespace__ = tns
    STATUS = Unicode
    TIMESTAMP = Unicode(pattern=pattern)
    
class OldFSCModel(ComplexModel):
    __namespace__ = tns
    GT_OLD_FSC = Array(OldFscItem)
    GT_STATUS = OldFscStatusModel

class OldFSCModelList(ComplexModel):
    __namespace__ = tns
    OldFSCData = OldFSCModel

class CreditNoteModel(ComplexModel):
    __namespace__ = tns
    CHASSIS = Unicode
    GCP_KUNNR = Unicode
    GCP_KMS = Unicode(default=None)
    GCP_UCN_NO = Unicode
    SERVICE_TYPE = Unicode
    SER_AVL_DT = Date(default=None)
    GCPDATA_RECV_DT = Date(default=None)
    CREDIT_NOTE = Unicode(default=None)
    CREDIT_DATE = Date(default=None)
    CDMS_DOC_NO = Unicode(default=None)
    CDMS_DT = Date(default=None)
#    CLOSED_DATE = Date(default=None)

class CreditNoteModelList(ComplexModel):
    __namespace__ = tns
    CreditNoteData = Array(CreditNoteModel)

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
    

class ContainerTrackerModel(ComplexModel):
    __namespace__ = tns

    ZIB_INDENT_NUM = Unicode
    CONSIGNMENT_ID = Unicode
    TRUCK_NO = Unicode
    TRANSPORTER_ID = Unicode
    LR_NUMBER = Unicode
    LR_DATE = Unicode(default=None)
    DO_NUM = Unicode
    GATEIN_TIME = Time(default=None)
    GATEIN_DATE = Unicode(default=None)
    TRANS_NAME = Unicode
    
class ContainerTrackerModelList(ComplexModel):
    __namespace__ = tns
    ContainerTrackerData = Array(ContainerTrackerModel)

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
    
class ContainerTrackerService(ServiceBase):
    __namespace__ = tns
    @srpc(ContainerTrackerModelList, AuthenticationModel,  _returns=Unicode)
    def postContainerTracker(ObjectList, Credential):
        tracker_list = []
        feed_remark = FeedLogWithRemark(len(ObjectList.ContainerTrackerData),
                                        feed_type='ContainerTracker Feed',
                                        action='Received', status=True)

        for tracker_obj in ObjectList.ContainerTrackerData:
            tracker_list.append({
                                'zib_indent_num' :  tracker_obj.ZIB_INDENT_NUM ,
                                'consignment_id' :  tracker_obj.CONSIGNMENT_ID ,
                                'truck_no' :  tracker_obj.TRUCK_NO,
                                'transporter_id' : tracker_obj.TRANSPORTER_ID,
                                'lr_number' :  tracker_obj.LR_NUMBER,
                                'lr_date' :  tracker_obj.LR_DATE,
                                'do_num' :  tracker_obj.DO_NUM,
                                'gatein_date' :  tracker_obj.GATEIN_DATE,
                                'gatein_time' :  tracker_obj.GATEIN_TIME,
                                'tranporter_name' : tracker_obj.TRANS_NAME,
                            })

        feed_remark = save_to_db(feed_type='container_tracker', data_source=tracker_list, feed_remark=feed_remark)
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
        feed_remark_header = save_to_db(feed_type='bomheader', data_source=bom_header_list, feed_remark=feed_remark_header)
        feed_remark_header.save_to_feed_log()
        header_log = get_response(feed_remark_header)
        
        feed_remark_item = FeedLogWithRemark(item_count, feed_type='BOM Item Feed', action='Received', status=True)
        feed_remark_item = save_to_db(feed_type='bomitem', data_source=bom_item_list, feed_remark=feed_remark_item)
        feed_remark_item.save_to_feed_log()
        item_log = get_response(feed_remark_item)
        
        if item_log == SUCCESS and  item_log == header_log:
            return SUCCESS
        else:
            return FAILED

class BrandService(ServiceBase):
    __namespace__ = tns

    @srpc(BrandModelList, AuthenticationModel,  _returns=Unicode)
    def postBrand(ObjectList, Credential):
        try:
            brand_list = []
            for brand in ObjectList.BrandData:
                brand_list.append({
                    'brand_id': brand.BRAND_ID,
                    'brand_name': brand.BRAND_NAME,
                    'product_type': brand.PRODUCT_TYPE,
                    'product_name': brand.PRODUCT_NAME,
                })
            save_to_db(feed_type='brand', data_source=brand_list)
            return SUCCESS
        except Exception as ex:
            return FAILED


class DealerService(ServiceBase):
    __namespace__ = tns

    @srpc(DealerModelList, AuthenticationModel, _returns=Unicode)
    def postDealer(ObjectList, Credential):
        dealer_list = []
        feed_remark = FeedLogWithRemark(len(ObjectList.DealerData),
                                        feed_type='Dealer Feed',
                                        action='Received', status=True)
        for dealer in ObjectList.DealerData:
            try:
                dealer_list.append({
                    'id': dealer.KUNNR,
                    'address': dealer.ADDRESS,
                    'service_advisor_id': dealer.SER_ADV_ID,
                    'name': dealer.SER_ADV_NAME,
                    'phone_number': utils.mobile_format(dealer.SER_ADV_MOBILE),
                    'status': dealer.ACTIVE_FLAG,
                    'cdms_flag':dealer.CDMS_FLAG
                })
            except Exception as ex:
                ex = "DealerService: {0}  Error on Validating {1}".format(dealer, ex)
                feed_remark.fail_remarks(ex)
                logger.error(ex)
        feed_remark = save_to_db(feed_type='dealer', data_source=dealer_list,
                              feed_remark=feed_remark)

        feed_remark.save_to_feed_log()
        return get_response(feed_remark)
    
class ASCService(ServiceBase):
    __namespace__ = tns

    @srpc(ASCModelList, AuthenticationModel, _returns=Unicode)
    def postASC(ObjectList, Credential):
        asc_list = []
        feed_remark = FeedLogWithRemark(len(ObjectList.ASCData),
                                        feed_type='ASC Feed',
                                        action='Received', status=True)
        for asc_element in ObjectList.ASCData:
            try:
                asc_list.append({
                    'asc_id': asc_element.ASC_ID,
                    'name': asc_element.ASC_NAME,
                    'phone_number': utils.mobile_format(asc_element.ASC_MOBILE),
                    'address': asc_element.ASC_ADDRESS,
                    'email': asc_element.ASC_EMAIL,
                    'dealer_id': asc_element.KUNNAR
                })
            except Exception as ex:
                ex = "ASCService: {0}  Error on Validating {1}".format(asc_element, ex)
                feed_remark.fail_remarks(ex)
                logger.error(ex)
        feed_remark = save_to_db(feed_type='ASC', data_source=asc_list,
                              feed_remark=feed_remark)
        feed_remark.save_to_feed_log()
        return get_response(feed_remark)    


class ProductDispatchService(ServiceBase):
    __namespace__ = tns

    @srpc(ProductDispatchModelList, AuthenticationModel, _returns=Unicode)
    def postProductDispatch(ObjectList, Credential):
        feed_remark = FeedLogWithRemark(len(ObjectList.ProductDispatchData),
                                        feed_type='Dispatch Feed',
                                        action='Received', status=True)
        product_dispatch_list = []
        for product in ObjectList.ProductDispatchData:
            try:
                product_dispatch_list.append({
                    'vin': product.CHASSIS,
                    'product_type': product.PRODUCT_TYPE,
                    'invoice_date': product.VEC_DIS_DT,
                    'dealer_id': product.KUNNR,
                    'unique_service_coupon': product.UCN_NO,
                    'valid_days': product.DAYS_LIMIT_TO,
                    'valid_kms': product.KMS_TO,
                    'service_type': product.SERVICE_TYPE,
                    'coupon_status': settings.DEFAULT_COUPON_STATUS,
#                     'sku_code':product.SKU_CODE
#                     'engine':product.ENGINE,
                })
            except Exception as ex:
                ex = "ProductDispatchService: {0}  Error on Validating {1}".format(product, ex)
                feed_remark.fail_remarks(ex)
                logger.error(ex)

        feed_remark = save_to_db(
            feed_type='dispatch', data_source=product_dispatch_list,
                                        feed_remark=feed_remark)
        feed_remark.save_to_feed_log()
        return get_response(feed_remark)


class ProductPurchaseService(ServiceBase):
    __namespace__ = tns

    @srpc(ProductPurchaseModelList, AuthenticationModel, _returns=Unicode)
    def postProductPurchase(ObjectList, Credential):
        feed_remark = FeedLogWithRemark(len(ObjectList.ProductPurchaseData),
                                        feed_type='Purchase Feed',
                                        action='Received', status=True)
        product_purchase_list = []
        for product in ObjectList.ProductPurchaseData:
            try:
                product_purchase_list.append({
                    'vin': product.CHASSIS,
                    'sap_customer_id': product.CUSTOMER_ID,
                    'customer_phone_number': utils.mobile_format(product.CUST_MOBILE),
                    'customer_name': product.CUSTOMER_NAME,
                    'city': product.CITY,
                    'state': product.STATE,
                    'pin_no': product.PIN_NO,
                    'product_purchase_date': product.VEH_SL_DT,
                    'engine': product.ENGINE,
                    'veh_reg_no': product.VEH_REG_NO
                })
            except Exception as ex:
                ex = "ProductPurchaseService: {0}  Error on Validating {1}".format(product, ex)
                feed_remark.fail_remarks(ex)
                logger.error(ex)

        feed_remark = save_to_db(
            feed_type='purchase', data_source=product_purchase_list,
                                                 feed_remark=feed_remark)
        feed_remark.save_to_feed_log()
        return get_response(feed_remark)

class OldFscService(ServiceBase):
    __namespace__ = tns

    @srpc(OldFSCModelList, AuthenticationModel, _returns=Unicode)
    def postOldFsc(ObjectList, Credential):
        feed_remark = FeedLogWithRemark(len(ObjectList.OldFSCData.GT_OLD_FSC),
                                        feed_type='Old Fsc Feed',
                                        action='Received', status=True)
        old_fsc_list = []
        for fsc in ObjectList.OldFSCData.GT_OLD_FSC:
            try:
                old_fsc_list.append({
                    'vin': fsc.CHASSIS,
                    'dealer': fsc.KUNNAR,
                    'material_number': fsc.MATNR,
                    'charge': fsc.CHARG,
                    'service': fsc.SERVICE
                })
              
            except Exception as ex:
                ex = "OldFscUpdateService: {0}  Error on Validating {1}".format(fsc, ex)
                feed_remark.fail_remarks(ex)
                logger.error(ex)
        feed_remark = save_to_db(
            feed_type='old_fsc', data_source=old_fsc_list,
                                                 feed_remark=feed_remark)
        feed_remark.save_to_feed_log()
        return get_response(feed_remark)
    
class CreditNoteService(ServiceBase):
    __namespace__ = tns

    @srpc(CreditNoteModelList, AuthenticationModel, _returns=Unicode)
    def postCreditNote(ObjectList, Credential):
        feed_remark = FeedLogWithRemark(len(ObjectList.CreditNoteData),
                                        feed_type='Credit Note Feed',
                                        action='Received', status=True)
        cdms_feed_remark = FeedLogWithRemark(len(ObjectList.CreditNoteData),
                                        feed_type='CDMS Feed',
                                        action='Received', status=True)
        credit_note_list = []
        for credit_note in ObjectList.CreditNoteData:
            try:
                credit_note_list.append({
                    'vin': credit_note.CHASSIS,
                    'dealer': credit_note.GCP_KUNNR,
                    'actual_kms': credit_note.GCP_KMS,
                    'unique_service_coupon': credit_note.GCP_UCN_NO,
                    'service_type': credit_note.SERVICE_TYPE,
                    'actual_service_date': credit_note.SER_AVL_DT,
                    'received_date': credit_note.GCPDATA_RECV_DT,
                    'credit_note': credit_note.CREDIT_NOTE,
                    'credit_date': credit_note.CREDIT_DATE,
                    'cdms_doc_number': credit_note.CDMS_DOC_NO,
                    'cdms_date': credit_note.CDMS_DT
#                    'closed_date': credit_note.CLOSED_DATE
                })

            except Exception as ex:
                ex = "CreditNoteService: {0} Error on Validating {1}".format(credit_note, ex)
                feed_remark.fail_remarks(ex)
                logger.error(ex)
        if credit_note.CDMS_DOC_NO:
            feed_remark = save_to_db(
                                    feed_type='credit_note', data_source=credit_note_list,
                                        feed_remark=cdms_feed_remark)
        else:
            feed_remark = save_to_db(
            feed_type='credit_note', data_source=credit_note_list,
                                        feed_remark=feed_remark)
        feed_remark.save_to_feed_log()
        return get_response(feed_remark)

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


def _on_method_call(ctx):
    if ctx.in_object is None:
        raise ArgumentError("Request doesn't contain data")
    auth_obj = AuthenticationService(
                                username=ctx.in_object.Credential.UserName,
                                password=ctx.in_object.Credential.Password)
    auth_obj.authenticate()

BrandService.event_manager.add_listener('method_call', _on_method_call)
DealerService.event_manager.add_listener('method_call', _on_method_call)
ProductDispatchService.event_manager.add_listener(
    'method_call', _on_method_call)
ProductPurchaseService.event_manager.add_listener(
    'method_call', _on_method_call)

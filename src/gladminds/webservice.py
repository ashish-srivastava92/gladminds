from django.views.decorators.csrf import csrf_exempt
from spyne.application import Application
from spyne.decorator import srpc
from spyne.model.complex import Array
from spyne.model.complex import ComplexModel
from spyne.model.complex import Iterable
from spyne.model.primitive import Integer, Decimal, Date
from spyne.model.primitive import Unicode, Mandatory
from spyne.protocol.soap import Soap11
from spyne.server.django import DjangoApplication
from spyne.server.wsgi import WsgiApplication
from spyne.service import ServiceBase
from spyne.util.wsgi_wrapper import WsgiMounter

from gladminds.feed import SAPFeed
from gladminds.soap_authentication import AuthenticationService
import logging
from django.conf import settings
import json
from gladminds import utils
from gladminds.aftersell.feed_log_remark import FeedLogWithRemark


logger = logging.getLogger("gladminds")


pattern = r'(\d{4})-(\d{2})-(\d{2})(\d{2})(\d{2})(\d{2})'
tns = "http://api.gladmindsplatform.co/api/v1/bajaj/feed/"
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
    UCN_NO = Unicode
    SERVICE_TYPE = Unicode
    CREDIT_NOTE = Unicode
    CREDIT_DATE = Date

class CreditNoteModelList(ComplexModel):
    __namespace__ = tns
    CreditNoteData = Array(CreditNoteModel)

class BrandService(ServiceBase):
    __namespace__ = tns

    @srpc(BrandModelList, AuthenticationModel, _returns=Unicode)
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
                    'dealer_id': dealer.KUNNR,
                    'address': dealer.ADDRESS,
                    'service_advisor_id': dealer.SER_ADV_ID,
                    'name': dealer.SER_ADV_NAME,
                    'phone_number': utils.mobile_format(dealer.SER_ADV_MOBILE),
                    'status': dealer.ACTIVE_FLAG
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
                })
            except Exception as ex:
                ex = "ProductDispatchService: {0}  Error on Validating {1}".format(product, ex)
                feed_remark.fail_remarks(ex)
                logger.error(ex)

        feed_remark = save_to_db(feed_type='dispatch', data_source=product_dispatch_list, feed_remark=feed_remark)
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
            feed_type='purchase', data_source=product_purchase_list, feed_remark=feed_remark)
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
        credit_note_list = []
        for credit_note in ObjectList.CreditNoteData:
            try:
                credit_note_list.append({
                    'vin': credit_note.CHASSIS,
                    'unique_service_coupon': credit_note.UCN_NO,
                    'service_type': credit_note.SERVICE_TYPE,
                    'credit_note': credit_note.CREDIT_NOTE,
                    'credit_date': credit_note.CREDIT_DATE,
                })

            except Exception as ex:
                ex = "CreditNoteService: {0} Error on Validating {1}".format(credit_note, ex)
                feed_remark.fail_remarks(ex)
                logger.error(ex)

        feed_remark = save_to_db(
            feed_type='credit_note', data_source=credit_note_list,
                                        feed_remark=feed_remark)
        feed_remark.save_to_feed_log()
        return get_response(feed_remark)

def get_response(feed_remark):
    return FAILED if feed_remark.failed_feeds > 0 else SUCCESS


def save_to_db(feed_type=None, data_source=[], feed_remark=None):
    sap_obj = SAPFeed()
    return sap_obj.import_to_db(feed_type=feed_type, data_source=data_source,
                                feed_remark=feed_remark)


def _on_method_call(ctx):
    if ctx.in_object is None:
        raise ArgumentError("Request doesn't contain data")
    auth_obj = AuthenticationService(username=ctx.in_object.Credential.UserName,
                                     password=ctx.in_object.Credential.Password)
    auth_obj.authenticate()

BrandService.event_manager.add_listener('method_call', _on_method_call)
DealerService.event_manager.add_listener('method_call', _on_method_call)
ProductDispatchService.event_manager.add_listener(
    'method_call', _on_method_call)
ProductPurchaseService.event_manager.add_listener(
    'method_call', _on_method_call)

all_app = Application([BrandService, DealerService, ProductDispatchService,
                       ProductPurchaseService, ASCService,
                       OldFscService, CreditNoteService],
                      tns=tns,
                      in_protocol=Soap11(validator='lxml'),
                      out_protocol=Soap11())
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

asc_app = Application([ASCService],
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

old_fsc_app = Application([OldFscService],
                           tns=tns,
                           in_protocol=Soap11(validator='lxml'),
                           out_protocol=Soap11()
                           )

credit_note_app = Application([CreditNoteService],
                           tns=tns,
                           in_protocol=Soap11(validator='lxml'),
                           out_protocol=Soap11()
                           )

all_service = csrf_exempt(DjangoApplication(all_app))
brand_service = csrf_exempt(DjangoApplication(brand_app))
dealer_service = csrf_exempt(DjangoApplication(dealer_app))
asc_service = csrf_exempt(DjangoApplication(asc_app))
dispatch_service = csrf_exempt(DjangoApplication(dispatch_app))
purchase_service = csrf_exempt(DjangoApplication(purchase_app))
old_fsc_service = csrf_exempt(DjangoApplication(old_fsc_app))
credit_note_service = csrf_exempt(DjangoApplication(credit_note_app))

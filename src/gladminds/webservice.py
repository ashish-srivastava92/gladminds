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
    ASC_ADDRESS_PINCODE = Unicode
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
        print ObjectList.DealerData
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
                ex = "DealerService: {0}  Error on Validating ".format(ex)
                logger.error("DealerService: {0} Object list element is {1}"
                             .format(ex, dealer))
                logger.error(dealer)
                feed_remark.fail_remarks(ex)
        feed_remark = save_to_db(feed_type='dealer', data_source=dealer_list,
                              feed_remark=feed_remark)

        feed_remark.save_to_feed_log()
        return get_response(feed_remark)
    
class ASCService(ServiceBase):
    __namespace__ = tns

    @srpc(ASCModelList, AuthenticationModel, _returns=Unicode)
    def postASC(ObjectList, Credential):
        asc_list = []
        feed_remark = FeedLogWithRemark(len(ObjectList.ascData),
                                        feed_type='ASC Feed',
                                        action='Received', status=True)
        print ObjectList.ascData
        for asc_element in ObjectList.ascData:
            try:
                asc_list.append({
                    'asc_id': asc_element.ASC_ID,
                    'name': asc_element.ASC_NAME,
                    'phone_number': utils.mobile_format(asc_element.ASC_MOBILE),
                    'address': asc_element.ASC_ADDRESS,
                    'email': asc_element.ASC_EMAIL,
                    'pincode': asc_element.ASC_ADDRESS_PINCODE,
                    'dealer_id': asc_element.KUNNR
                })
            except Exception as ex:
                ex = "ASCService: {0}  Error on Validating ".format(ex)
                logger.error("DealerService: {0} Object list element is {1}"
                             .format(ex, asc_element))
                logger.error(asc_element)
                feed_remark.fail_remarks(ex)
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
                ex = "ProductDispatchService: {0}  Error on Validating"\
                                                        .format(ex)
                feed_remark.fail_remarks(ex)
                logger.error("ProductDispatchService: {0} Object List is {1}"
                             .format(ex, product))

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
                    'engine': product.ENGINE
                })
            except Exception as ex:
                ex = "ProductPurchaseService: {0}  Error on Validating "\
                                                            .format(ex)
                logger.error("ProductPurchaseService: {0} Object List is {1}"
                             .format(ex, product))
                feed_remark.fail_remarks(ex)

        feed_remark = save_to_db(
            feed_type='purchase', data_source=product_purchase_list,
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

all_app = Application([BrandService, DealerService, ProductDispatchService, ProductPurchaseService, ASCService],
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

all_service = csrf_exempt(DjangoApplication(all_app))
brand_service = csrf_exempt(DjangoApplication(brand_app))
dealer_service = csrf_exempt(DjangoApplication(dealer_app))
asc_service = csrf_exempt(DjangoApplication(asc_app))
dispatch_service = csrf_exempt(DjangoApplication(dispatch_app))
purchase_service = csrf_exempt(DjangoApplication(purchase_app))
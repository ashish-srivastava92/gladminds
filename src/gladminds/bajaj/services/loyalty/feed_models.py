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

from gladminds.bajaj.services.loyalty.import_feed import LoyaltyFeed
from gladminds.core.soap_authentication import AuthenticationService
import logging
from django.conf import settings
import json
from gladminds.core import utils
from gladminds.core.managers.feed_log_remark import FeedLogWithRemark
from gladminds.core.managers.audit_manager import feed_failure_log


logger = logging.getLogger("gladminds")


pattern = r'(\d{4})-(\d{2})-(\d{2})(\d{2})(\d{2})(\d{2})'
tns = settings.WSDL_TNS
SUCCESS = "SUCCESS"
FAILED = "FAILURE"


class AuthenticationModel(ComplexModel):
    __namespace__ = tns
    UserName = Unicode(min_occurs=1, nillable=False)
    Password = Unicode(min_occurs=1, nillable=False)

class PartMasterModel(ComplexModel):
    __namespace__ = tns
    PART_NUMBER = Unicode
    PART_MODEL = Unicode
    PART_TYPE = Unicode
    DESCRIPTION = Unicode
    CATEGORY = Unicode
    SEGMENT = Unicode
    SUPPLIER = Unicode

class PartMasterModelList(ComplexModel):
    __namespace__ = tns
    PartMasterData = Array(PartMasterModel)


class PartUPCModel(ComplexModel):
    __namespace__ = tns
    PART_NUMBER = Unicode
    PART_UPC = Unicode


class PartUPCModelList(ComplexModel):
    __namespace__ = tns
    PartUPCData = Array(PartUPCModel)
    
class PartPointModel(ComplexModel):
    __namespace__ = tns
    PART_NUMBER = Unicode
    POINTS = Unicode
    PRICE = Unicode
    MRP = Unicode
    VALID_FROM = Date
    VALID_TILL = Date
    TERRITORY = Unicode


class PartPointModelList(ComplexModel):
    __namespace__ = tns
    PartPointData = Array(PartPointModel)    


class DistributorModel(ComplexModel):
    __namespace__ = tns
    DISTRIBUTOR_ID = Unicode
    NAME = Unicode
    EMAIL = Unicode
    PHONE_NUMBER = Unicode
    CITY = Unicode
    ASM_ID = Unicode

class DistributorModelList(ComplexModel):
    __namespace__ = tns
    DistributorData = Array(DistributorModel)

class MechanicModel(ComplexModel):
    __namespace__ = tns
    MECH_ID = Unicode
    FIRST_NAME = Unicode
    LAST_NAME = Unicode(default=None)
    PHONE_NUMBER = Unicode
    DOB = Date
    SHOP_NAME = Unicode
    DISTRICT = Unicode
    STATE = Unicode
    PINCODE = Unicode
    DIST_ID = Unicode

class MechanicModelList(ComplexModel):
    __namespace__ = tns
    MechanicData = Array(MechanicModel)

class NSMModel(ComplexModel):
    __namespace__ = tns
    NAME = Unicode
    EMAIL = Unicode
    PHONE_NUMBER = Unicode
    TERRITORY = Unicode

class NSMModelList(ComplexModel):
    __namespace__ = tns
    NSMData = Array(NSMModel)

class ASMModel(ComplexModel):
    __namespace__ = tns
    NAME = Unicode
    EMAIL = Unicode
    PHONE_NUMBER = Unicode
    STATE = Unicode
    TERRITORY = Unicode

class ASMModelList(ComplexModel):
    __namespace__ = tns
    ASMData = Array(ASMModel)

class PartMasterService(ServiceBase):
    __namespace__ = tns

    @srpc(PartMasterModelList, AuthenticationModel,  _returns=Unicode)
    def postPartMaster(ObjectList, Credential):
        try:
            part_master_list = []
            feed_remark = FeedLogWithRemark(len(ObjectList.PartMasterData),
                                        feed_type='Part Master Feed',
                                        action='Received', status=True)

            for part in ObjectList.PartMasterData:
                part_master_list.append({
                    'part_number': part.PART_NUMBER,
                    'part_model': part.PART_MODEL,
                    'part_type': part.PART_TYPE,
                    'category': part.CATEGORY,
                    'description': part.DESCRIPTION,
                    'segment': part.SEGMENT,
                    'supplier': part.SUPPLIER,
                })
        except Exception as ex:
            ex = "PartMasterService: {0}  Error on Validating {1}".format(part, ex)
            feed_remark.fail_remarks(ex)
            logger.error(ex)
        feed_remark = save_to_db(feed_type='part_master', data_source=part_master_list,
                          feed_remark=feed_remark)

        feed_remark.save_to_feed_log()
        return get_response(feed_remark)


class PartUPCService(ServiceBase):
    __namespace__ = tns

    @srpc(PartUPCModelList, AuthenticationModel, _returns=Unicode)
    def postPartUPC(ObjectList, Credential):
        part_point_list = []
        feed_remark = FeedLogWithRemark(len(ObjectList.PartUPCData),
                                        feed_type='Part UPC Feed',
                                        action='Received', status=True)
        for part in ObjectList.PartUPCData:
            try:
                part_point_list.append({
                    'part_number': part.PART_NUMBER,
                    'UPC': part.PART_UPC,
                })
            except Exception as ex:
                ex = "PartUPCService: {0}  Error on Validating {1}".format(part, ex)
                feed_remark.fail_remarks(ex)
                logger.error(ex)
        feed_remark = save_to_db(feed_type='part_upc', data_source=part_point_list,
                              feed_remark=feed_remark)

        feed_remark.save_to_feed_log()
        return get_response(feed_remark)
       
class PartPointService(ServiceBase):
    __namespace__ = tns

    @srpc(PartPointModelList, AuthenticationModel, _returns=Unicode)
    def postPartPoint(ObjectList, Credential):
        part_upc_list = []
        feed_remark = FeedLogWithRemark(len(ObjectList.PartPointData),
                                        feed_type='Part points Feed',
                                        action='Received', status=True)
        for part in ObjectList.PartPointData:
            try:
                part_upc_list.append({
                    'part_number': part.PART_NUMBER,
                    'points': part.POINTS,
                    'price': part.PRICE,
                    'mrp': part.MRP,
                    'valid_from': part.VALID_FROM,
                    'valid_to': part.VALID_TILL,
                    'territory': part.TERRITORY,
                })
            except Exception as ex:
                ex = "PartPointService: {0}  Error on Validating {1}".format(part, ex)
                feed_remark.fail_remarks(ex)
                logger.error(ex)
        feed_remark = save_to_db(feed_type='part_point', data_source=part_upc_list,
                              feed_remark=feed_remark)

        feed_remark.save_to_feed_log()
        return get_response(feed_remark)
    
class DistributorService(ServiceBase):
    __namespace__ = tns

    @srpc(DistributorModelList, AuthenticationModel, _returns=Unicode)
    def postDistributor(ObjectList, Credential):
        distributor_list = []
        feed_remark = FeedLogWithRemark(len(ObjectList.DistributorData),
                                        feed_type='Distributor Feed',
                                        action='Received', status=True)
        for distributor in ObjectList.DistributorData:
            try:
                distributor_list.append({
                    'id': distributor.DISTRIBUTOR_ID.upper(),
                    'name': distributor.NAME.upper(),
                    'email': distributor.EMAIL,
                    'mobile': utils.mobile_format(distributor.PHONE_NUMBER),
                    'city': distributor.CITY.upper(),
                    'asm_id': distributor.ASM_ID
                })
            except Exception as ex:
                ex = "DistributorService: {0}  Error on Validating {1}".format(distributor, ex)
                feed_remark.fail_remarks(ex)
                logger.error(ex)
        feed_remark = save_to_db(feed_type='distributor', data_source=distributor_list,
                              feed_remark=feed_remark)

        feed_remark.save_to_feed_log()
        return get_response(feed_remark)
    
class MechanicService(ServiceBase):
    __namespace__ = tns

    @srpc(MechanicModelList, AuthenticationModel, _returns=Unicode)
    def postMechanic(ObjectList, Credential):
        mechanic_list = []
        feed_remark = FeedLogWithRemark(len(ObjectList.MechanicData),
                                        feed_type='Mechanic Feed',
                                        action='Received', status=True)
        for mechanic in ObjectList.MechanicData:
            try:
                mechanic_list.append({
                    'mechanic_id': mechanic.MECH_ID.upper(),
                    'first_name': mechanic.FIRST_NAME.upper(),
                    'last_name': mechanic.LAST_NAME.upper(),
                    'mobile': utils.mobile_format(mechanic.PHONE_NUMBER),
                    'shop_name': mechanic.SHOP_NAME.upper(),
                    'dob': mechanic.DOB,
                    'district': mechanic.DISTRICT.upper(),
                    'state': mechanic.STATE.upper(),
                    'pincode': mechanic.PINCODE,
                    'dist_id': mechanic.DIST_ID
                })
            except Exception as ex:
                ex = "MechanicService: {0}  Error on Validating {1}".format(mechanic, ex)
                feed_remark.fail_remarks(ex)
                logger.error(ex)
        feed_remark = save_to_db(feed_type='mechanic', data_source=mechanic_list,
                              feed_remark=feed_remark)

        feed_remark.save_to_feed_log()
        return get_response(feed_remark)

class NSMService(ServiceBase):
    __namespace__ = tns

    @srpc(NSMModelList, AuthenticationModel, _returns=Unicode)
    def postNSM(ObjectList, Credential):
        nsm_list = []
        feed_remark = FeedLogWithRemark(len(ObjectList.NSMData),
                                        feed_type='NSM Feed',
                                        action='Received', status=True)
        for nsm in ObjectList.NSMData:
            try:
                nsm_list.append({
                    'name':nsm.NAME, 
                    'email':nsm.EMAIL,
                    'phone_number': utils.mobile_format(nsm.PHONE_NUMBER),
                    'territory':nsm.TERRITORY
                })
            except Exception as ex:
                ex = "NSMService: {0}  Error on Validating {1}".format(nsm, ex)
                feed_remark.fail_remarks(ex)
                logger.error(ex)
        feed_remark = save_to_db(feed_type='nsm', data_source=nsm_list,
                              feed_remark=feed_remark)

        feed_remark.save_to_feed_log()
        return get_response(feed_remark)


class ASMService(ServiceBase):
    __namespace__ = tns

    @srpc(ASMModelList, AuthenticationModel, _returns=Unicode)
    def postASM(ObjectList, Credential):
        asm_list = []
        feed_remark = FeedLogWithRemark(len(ObjectList.ASMData),
                                        feed_type='ASM Feed',
                                        action='Received', status=True)
        for asm in ObjectList.ASMData:
            try:
                asm_list.append({
                    'name':asm.NAME, 
                    'email':asm.EMAIL,
                    'phone_number': utils.mobile_format(asm.PHONE_NUMBER),
                    'state':asm.STATE,
                    'territory':asm.TERRITORY
                })
            except Exception as ex:
                ex = "ASMService: {0}  Error on Validating {1}".format(asm, ex)
                feed_remark.fail_remarks(ex)
                logger.error(ex)
        feed_remark = save_to_db(feed_type='asm', data_source=asm_list,
                              feed_remark=feed_remark)

        feed_remark.save_to_feed_log()
        return get_response(feed_remark)


def get_response(feed_remark):
    if feed_remark.failed_feeds > 0:
        remarks = feed_remark.remarks.elements()
        for remark in remarks:
            feed_failure_log(feed_type=feed_remark.feed_type, reason=remark)
        return FAILED
    else:
        return SUCCESS

def save_to_db(feed_type=None, data_source=[], feed_remark=None):
    loyalty_feed_obj = LoyaltyFeed()
    return loyalty_feed_obj.import_to_db(feed_type=feed_type, data_source=data_source,
                                 feed_remark=feed_remark)


def _on_method_call(ctx):
    if ctx.in_object is None:
        raise ArgumentError("Request doesn't contain data")
    auth_obj = AuthenticationService(
                                username=ctx.in_object.Credential.UserName,
                                password=ctx.in_object.Credential.Password)
    auth_obj.authenticate()

PartMasterService.event_manager.add_listener('method_call', _on_method_call)
PartUPCService.event_manager.add_listener('method_call', _on_method_call)
PartPointService.event_manager.add_listener('method_call', _on_method_call)
DistributorService.event_manager.add_listener('method_call', _on_method_call)

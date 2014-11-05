import logging
from datetime import datetime, timedelta
from authentication import AccessTokenAuthentication

from django.conf.urls import url
from django.core.exceptions import ObjectDoesNotExist
from django.db import models, transaction
from django.forms.models import model_to_dict
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings
from django.db.models import Q

from gladminds import smsparser, utils, audit, message_template as templates
from gladminds.models import common
from gladminds.decorator import log_time
from gladminds.feed import BaseFeed
from gladminds.aftersell.models import common as aftersell_common
from gladminds.sqs_tasks import send_registration_detail, send_service_detail, \
    send_coupon_detail_customer, send_coupon, \
    send_brand_sms_customer, send_close_sms_customer, send_invalid_keyword_message, \
    customer_detail_recovery
from tastypie import fields
from tastypie.http import HttpBadRequest, HttpUnauthorized
from tastypie.resources import Resource, ModelResource
from tastypie.utils.urls import trailing_slash
from tastypie import http
from tastypie.exceptions import ImmediateHttpResponse

from django.db.models import Q
import logging
from gladminds.utils import mobile_format, format_message,\
    get_phone_number_format
from django.utils import timezone
from django.conf import settings
from gladminds.utils import get_task_queue
from gladminds.settings import COUPON_VALID_DAYS
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.contrib.auth.models import User
from authentication import AccessTokenAuthentication

from gladminds import smsparser, utils, audit, message_template as templates
from gladminds.models import common
from gladminds.aftersell.models import common as aftersell_common
from gladminds.sqs_tasks import send_registration_detail, send_service_detail, \
    send_coupon_detail_customer, send_coupon, \
    send_brand_sms_customer, send_close_sms_customer, send_invalid_keyword_message
from gladminds.utils import mobile_format, format_message, get_task_queue, create_context
from gladminds.feed import BaseFeed
from gladminds.settings import COUPON_VALID_DAYS
from gladminds.mail import send_feedback_received,send_servicedesk_feedback

logger = logging.getLogger('gladminds')
json = utils.import_json()


__all__ = ['GladmindsTaskManager']
AUDIT_ACTION = 'SEND TO QUEUE'
angular_format = lambda x: x.replace('{', '<').replace('}', '>')


class GladmindsResources(Resource):

    class Meta:
        resource_name = 'messages'

    def base_urls(self):
        return [
            url(r"^messages", self.wrap_view('dispatch_gladminds'))
        ]

    def dispatch_gladminds(self, request, **kwargs):
        sms_dict = {}
        if request.POST.get('text'):
            message = request.POST.get('text')
            phone_number = request.POST.get('phoneNumber')
        elif request.GET.get('cli'):
            message = request.GET.get('msg')
            phone_number = request.GET.get('cli')
        elif request.POST.get("advisorMobile"):
            phone_number = request.POST.get('advisorMobile')
            customer_id = request.POST.get('customerId')
            if request.POST.get('action') == 'validate':
                logger.info('Validating the service coupon for customer {0}'.format(customer_id))
                odo_read = request.POST.get('odoRead')
                service_type = request.POST.get('serviceType')
                message = '{3} {0} {1} {2}'.format(customer_id, odo_read, service_type, settings.ALLOWED_KEYWORDS['check'].upper())
                logger.info('Message to send: ' + message)
            else:
                ucn = request.POST.get('ucn')
                logger.info('Terminating the service coupon {0}'.format(ucn))
                message = '{2} {0} {1}'.format(customer_id, ucn, settings.ALLOWED_KEYWORDS['close'].upper())
                logger.info('Message to send: ' + message)
        phone_number = utils.get_phone_number_format(phone_number)
        message = format_message(message)
        audit.audit_log(action='RECIEVED', sender=phone_number, reciever='+1 469-513-9856', message=message, status='success')
        logger.info('Recieved Message from phone number: {0} and message: {1}'.format(phone_number, message))
        try:
            sms_dict = smsparser.sms_parser(message=message)
        except smsparser.InvalidKeyWord as ink:
            message = ink.template
            if settings.ENABLE_AMAZON_SQS:
                task_queue = get_task_queue()
                task_queue.add("send_invalid_keyword_message", {"phone_number":phone_number, "message":message, "sms_client":settings.SMS_CLIENT})
            else:
                send_invalid_keyword_message.delay(phone_number=phone_number, message=message, sms_client=settings.SMS_CLIENT)

            audit.audit_log(reciever=phone_number, action=AUDIT_ACTION, message=message)
            raise ImmediateHttpResponse(HttpBadRequest(ink.message))
        except smsparser.InvalidMessage as inm:
            message = inm.template
            if settings.ENABLE_AMAZON_SQS:
                task_queue = get_task_queue()
                task_queue.add("send_invalid_keyword_message", {"phone_number":phone_number, "message":message, "sms_client":settings.SMS_CLIENT})
            else:
                send_invalid_keyword_message.delay(phone_number=phone_number, message=message, sms_client=settings.SMS_CLIENT)
            audit.audit_log(reciever=phone_number, action=AUDIT_ACTION, message=message)
            raise ImmediateHttpResponse(HttpBadRequest(inm.message))
        except smsparser.InvalidFormat as inf:
            message = angular_format('CORRECT FORMAT: ' + inf.template)
            if settings.ENABLE_AMAZON_SQS:
                task_queue = get_task_queue()
                task_queue.add("send_invalid_keyword_message", {"phone_number":phone_number, "message":message, "sms_client":settings.SMS_CLIENT})
            else:
                send_invalid_keyword_message.delay(phone_number=phone_number, message=message, sms_client=settings.SMS_CLIENT)
            audit.audit_log(reciever=phone_number, action=AUDIT_ACTION, message=message)
            raise ImmediateHttpResponse(HttpBadRequest(inf.message))
        handler = getattr(self, sms_dict['handler'], None)
        try:
            with transaction.atomic():
                to_be_serialized = handler(sms_dict, mobile_format(phone_number))
        except Exception as ex:
            logger.info("The database failed to perform {0}:{1}".format(request.POST.get('action'), ex))
        return self.create_response(request, data=to_be_serialized)

    @log_time
    def register_customer(self, sms_dict, phone_number):
        customer_name = sms_dict['name']
        email_id = sms_dict['email_id']
        try:
            object = common.GladMindUsers.objects.get(phone_number=phone_number)
            gladmind_customer_id = object.gladmind_customer_id
            customer_name = object.customer_name
        except ObjectDoesNotExist as odne:
            gladmind_customer_id = utils.generate_unique_customer_id()
            registration_date = datetime.now()
            user_feed = BaseFeed()
            user = user_feed.register_user('customer', username=gladmind_customer_id)
            customer = common.GladMindUsers(
                user=user, gladmind_customer_id=gladmind_customer_id, phone_number=phone_number,
                customer_name=customer_name, email_id=email_id,
                registration_date=registration_date)
            customer.save()
        # Please update the template variable before updating the keyword-argument
        message = smsparser.render_sms_template(status='send', keyword=sms_dict['keyword'], customer_id=gladmind_customer_id)
        phone_number = utils.get_phone_number_format(phone_number)
        logger.info("customer is registered with message %s" % message)
        if settings.ENABLE_AMAZON_SQS:           
            task_queue = get_task_queue()
            task_queue.add("send_registration_detail", {"phone_number":phone_number, "message":message, "sms_client":settings.SMS_CLIENT})
        else:
            send_registration_detail.delay(phone_number=phone_number, message=message, sms_client=settings.SMS_CLIENT)
        audit.audit_log(reciever=phone_number, action=AUDIT_ACTION, message=message)
        return True

    @log_time
    def send_customer_detail(self, sms_dict, phone_number):
        keyword = sms_dict['params']
        value = sms_dict['message']
        kwargs = {}
        kwargs['customer_phone_number__phone_number__endswith'] = get_phone_number_format(phone_number)
        if value and len(value)>5 and keyword in ['vin', 'id']:
            if keyword == 'id':
                kwargs['sap_customer_id'] = value
                model_key = 'vin'
                search_key = 'vin'
            else:
                kwargs['vin__endswith'] = value
                model_key = 'id'
                search_key = 'sap_customer_id'
                
            try:
                product_object = common.ProductData.objects.get(**kwargs)
                if product_object.sap_customer_id:
                    message = templates.get_template('SEND_CUSTOMER_DETAILS').format(model_key, getattr(product_object, search_key))
                else:
                    message = templates.get_template('INVALID_RECOVERY_MESSAGE').format(keyword)
            
            except Exception as ex:
                logger.info('Details not found with message %s' % ex)
                message = templates.get_template('INVALID_RECOVERY_MESSAGE').format(keyword)
        else:
            message = templates.get_template('SEND_INVALID_MESSAGE')
        
        if settings.ENABLE_AMAZON_SQS:
            task_queue = get_task_queue()
            task_queue.add("customer_detail_recovery", {"phone_number":phone_number, "message":message, "sms_client":settings.SMS_CLIENT})
        else:
            customer_detail_recovery.delay(phone_number=phone_number, message=message, sms_client=settings.SMS_CLIENT)
        audit.audit_log(reciever=phone_number, action=AUDIT_ACTION, message=message)
        return {'status': True, 'message': message}

    @log_time
    def customer_service_detail(self, sms_dict, phone_number):
        sap_customer_id = sms_dict.get('sap_customer_id', None)
        message = None
        try:
            customer_product_data = common.CouponData.objects.select_related \
                                        ('vin', 'customer_phone_number__phone_number').\
                                        filter(vin__customer_phone_number__phone_number=phone_number, \
                                        vin__sap_customer_id=sap_customer_id).\
                                        order_by('vin', 'valid_days') if sap_customer_id else \
                                        common.CouponData.objects.select_related('vin', 'customer_phone_number__phone_number').\
                                        filter(vin__customer_phone_number__phone_number=phone_number).\
                                        order_by('vin', 'valid_days')
            logger.info(customer_product_data)
            valid_product_data = []
            for data in customer_product_data:
                if data.status == 1 or data.status == 4:
                    valid_product_data.append(data)
            valdata = [valid_product_data[0]]
            service_list = map(lambda object: {'vin': object.vin.vin, 'usc': object.unique_service_coupon, 'valid_days': object.valid_days, 'valid_kms':object.valid_kms}, valdata)
            template = templates.get_template('SEND_CUSTOMER_SERVICE_DETAIL')
            msg_list = [template.format(**key_args) for key_args in service_list]
            if not msg_list:
                raise Exception()
            message = ', '.join(msg_list)
        except Exception as ex:
            message = smsparser.render_sms_template(status='invalid', keyword=sms_dict['keyword'], sap_customer_id=sap_customer_id)
        logger.info("Send Service detail %s" % message)
        phone_number = utils.get_phone_number_format(phone_number)
        if settings.ENABLE_AMAZON_SQS:
            task_queue = get_task_queue()
            task_queue.add("send_service_detail", {"phone_number":phone_number, "message":message, "sms_client":settings.SMS_CLIENT})
        else:
            send_service_detail.delay(phone_number=phone_number, message=message, sms_client=settings.SMS_CLIENT)
        audit.audit_log(reciever=phone_number, action=AUDIT_ACTION, message=message)
        return True

    def get_customer_phone_number_from_vin(self, vin):
        product_obj = common.ProductData.objects.filter(vin=vin).select_related('customer_phone_number__phone_number')
        return product_obj[0].customer_phone_number.phone_number


    def update_higher_range_coupon(self, kms, vin):
        '''
            Update those coupon have higher value than the least in progress
            coupon. These case existed because some time user add higher value
            of kilometer.
        '''
        updated_coupon = common.CouponData.objects\
                        .filter(Q(status=4) | Q(status=5), vin=vin, valid_kms__gt=kms)\
                        .update(status=1, sa_phone_number=None, actual_kms=None,
                                actual_service_date=None, servicing_dealer=None)
        logger.info("%s have higher KMS range" % updated_coupon)

    def update_exceed_limit_coupon(self, actual_kms, vin):
        '''
            Exceed Limit those coupon whose kms limit is small then actual kms limit
        '''
        exceed_limit_coupon = common.CouponData.objects\
            .filter(Q(status=1) | Q(status=4), vin=vin, valid_kms__lt=actual_kms)\
            .update(status=5, actual_kms=actual_kms)
        logger.info("%s are exceed limit coupon" % exceed_limit_coupon)

    def get_vin(self, sap_customer_id):
        try:
            sap_customer_id = utils.get_updated_customer_id(sap_customer_id)
            product_data=common.ProductData.objects.get(sap_customer_id=sap_customer_id)
            return product_data
        except Exception as ax:
            logger.error("Vin is not in customer_product_data Error %s " % ax)

    def update_coupon(self, valid_coupon, actual_kms, dealer_data, status,\
                                                 update_time):
        valid_coupon.actual_kms = actual_kms
        valid_coupon.actual_service_date = update_time
        valid_coupon.extended_date = update_time + timedelta(days=COUPON_VALID_DAYS)
        valid_coupon.status = status
        valid_coupon.sa_phone_number = dealer_data.service_advisor_id
        valid_coupon.servicing_dealer = dealer_data.dealer_id
        valid_coupon.save()
        
    def update_inprogress_coupon(self, coupon, actual_kms, dealer_data):
        logger.info("Expired on %s" % coupon.mark_expired_on)
        logger.info("Extended on %s" % coupon.extended_date)
        expiry_date = coupon.mark_expired_on
        if coupon.extended_date < expiry_date:
            coupon.extended_date = expiry_date
            coupon.save()
        
        validity_date = coupon.extended_date
        today = timezone.now()
        current_time = datetime.now()
        if expiry_date >= today:
            coupon.extended_date = current_time + timedelta(days=COUPON_VALID_DAYS)
            self.update_coupon(coupon, actual_kms, dealer_data, 4, current_time)
        elif validity_date >= today and expiry_date < today:
            coupon.actual_service_date = current_time
            coupon.save()
    
    def get_requested_coupon_status(self, vin, service_type):
        requested_coupon = common.CouponData.objects.filter(vin=vin,
                                                    service_type=service_type) 
        if not requested_coupon:
            status = "not available"
        else:
            status = common.STATUS_CHOICES[requested_coupon[0].status - 1][1]
        return status
    
    @log_time
    def validate_coupon(self, sms_dict, phone_number):
        actual_kms = int(sms_dict['kms'])
        service_type = sms_dict['service_type']
        dealer_message = None
        customer_message = None
        customer_phone_number = None
        customer_message_countdown = settings.DELAY_IN_CUSTOMER_UCN_MESSAGE
        sap_customer_id = sms_dict.get('sap_customer_id', None)
        dealer_data = self.validate_dealer(phone_number)
        if not dealer_data:
            return {'status': False, 'message': templates.get_template('UNAUTHORISED_SA')}
        if not self.is_valid_data(customer_id=sap_customer_id, sa_phone=phone_number):
            return {'status': False, 'message': templates.get_template('SEND_SA_WRONG_CUSTOMER_UCN')}
        try:
            vin = self.get_vin(sap_customer_id)
            self.update_exceed_limit_coupon(actual_kms, vin)
            valid_coupon = common.CouponData.objects.filter(Q(status=1) | Q(status=4) | Q(status=5), vin=vin,
                            valid_kms__gte=actual_kms, service_type=service_type) \
                           .select_related('vin', 'customer_phone_number__phone_number').order_by('service_type')
            logger.info(valid_coupon)
            if len(valid_coupon) > 0:
                self.update_higher_range_coupon(valid_coupon[0].valid_kms, vin)
                valid_coupon = valid_coupon[0]
                coupon_sa_obj = common.ServiceAdvisorCouponRelationship.objects.filter(unique_service_coupon=valid_coupon\
                                                                                       ,service_advisor_phone=dealer_data.service_advisor_id\
                                                                                       ,dealer_id=dealer_data.dealer_id)
                logger.info('Coupon_sa_obj exists: %s' % coupon_sa_obj)
                if not len(coupon_sa_obj):
                    coupon_sa_obj = common.ServiceAdvisorCouponRelationship(unique_service_coupon=valid_coupon\
                                                                            ,service_advisor_phone=dealer_data.service_advisor_id\
                                                                            ,dealer_id=dealer_data.dealer_id)
                    coupon_sa_obj.save()
                    logger.info('Coupon obj created: %s' % coupon_sa_obj)

            in_progress_coupon = common.CouponData.objects.filter(vin=vin, valid_kms__gte=actual_kms, status=4) \
                                 .select_related ('vin', 'customer_phone_number__phone_number') \
                                 .order_by('service_type')
            try:
                customer_phone_number = vin.customer_phone_number.phone_number
            except Exception as ax:
                logger.error('Customer Phone Number is not stored in DB %s' % ax)
            if len(in_progress_coupon) > 0:
                self.update_inprogress_coupon(in_progress_coupon[0], actual_kms, dealer_data)
                logger.info("Validate_coupon: in_progress_coupon")
                dealer_message = templates.get_template('COUPON_ALREADY_INPROGRESS').format(
                                                    service_type=in_progress_coupon[0].service_type,
                                                    customer_id=sap_customer_id)
                customer_message = templates.get_template('SEND_CUSTOMER_VALID_COUPON').format(
                                                    coupon=in_progress_coupon[0].unique_service_coupon,
                                                    service_type=in_progress_coupon[0].service_type)
            elif valid_coupon:
                logger.info("Validate_coupon: valid_coupon")
                self.update_coupon(valid_coupon, actual_kms, dealer_data, 4, datetime.now())
                dealer_message = templates.get_template('SEND_SA_VALID_COUPON').format(
                                                    service_type=valid_coupon.service_type,
                                                    customer_id=sap_customer_id)

                customer_message = templates.get_template('SEND_CUSTOMER_VALID_COUPON').format(
                                            coupon=valid_coupon.unique_service_coupon,
                                            service_type=valid_coupon.service_type)
            else:
                requested_coupon_status = self.get_requested_coupon_status(vin, service_type)
                dealer_message = templates.get_template('SEND_SA_OTHER_VALID_COUPON').format(
                                            req_service_type=service_type,
                                            req_status=requested_coupon_status,                                                     
                                            customer_id=sap_customer_id)
                logger.info("Validate_coupon: ELSE PART")
                customer_message_countdown = 10
                requested_coupon = common.CouponData.objects.get(vin=vin, service_type=service_type)
                customer_message = templates.get_template('SEND_CUSTOMER_EXPIRED_COUPON').format(service_type=requested_coupon.service_type)
            if settings.ENABLE_AMAZON_SQS:
                task_queue = get_task_queue()
                task_queue.add("send_coupon_detail_customer", {"phone_number":utils.get_phone_number_format(customer_phone_number), "message":customer_message, "sms_client":settings.SMS_CLIENT}, delay_seconds=customer_message_countdown)
            else:
                send_coupon_detail_customer.apply_async( kwargs={ 'phone_number': utils.get_phone_number_format(customer_phone_number), 'message':customer_message, "sms_client":settings.SMS_CLIENT}, countdown=customer_message_countdown)
            audit.audit_log(reciever=customer_phone_number, action=AUDIT_ACTION, message=customer_message)
        except IndexError as ie:
            dealer_message = templates.get_template('SEND_INVALID_VIN_OR_FSC')
        except ObjectDoesNotExist as odne:
            dealer_message = templates.get_template('SEND_INVALID_SERVICE_TYPE').format(service_type=service_type)
        except Exception as ex:
            logger.info(ex)
            dealer_message = templates.get_template('SEND_INVALID_MESSAGE')
        finally:
            logger.info("validate message send to SA %s" % dealer_message)
            phone_number = utils.get_phone_number_format(phone_number)
            if settings.ENABLE_AMAZON_SQS:
                task_queue = get_task_queue()
                task_queue.add("send_service_detail", {"phone_number":phone_number, "message":dealer_message, "sms_client":settings.SMS_CLIENT})
            else:
                send_service_detail.delay(phone_number=phone_number, message=dealer_message, sms_client=settings.SMS_CLIENT)
            audit.audit_log(reciever=phone_number, action=AUDIT_ACTION, message=dealer_message)
        return {'status': True, 'message': dealer_message}

    @log_time
    def close_coupon(self, sms_dict, phone_number):
        dealer_sa_object = self.validate_dealer(phone_number)
        unique_service_coupon = sms_dict['usc']
        sap_customer_id = sms_dict.get('sap_customer_id', None)
        message = None
        if not dealer_sa_object:
            return {'status': False, 'message': templates.get_template('UNAUTHORISED_SA')}
        if not self.is_valid_data(customer_id=sap_customer_id, coupon=unique_service_coupon, sa_phone=phone_number):
            return {'status': False, 'message': templates.get_template('SEND_SA_WRONG_CUSTOMER_UCN')}
        if not self.is_sa_initiator(unique_service_coupon, dealer_sa_object, phone_number):
            return {'status': False, 'message': "SA is not the coupon initiator."}
        try:
            vin = self.get_vin(sap_customer_id)
            coupon_object = common.CouponData.objects.filter(vin=vin, unique_service_coupon=unique_service_coupon).select_related ('vin', 'customer_phone_number__phone_number')[0]
            if coupon_object.status == 2 or coupon_object.status == 6:
                message=templates.get_template('COUPON_ALREADY_CLOSED')
            elif coupon_object.status == 4:
                customer_phone_number = coupon_object.vin.customer_phone_number.phone_number
                coupon_object.status = 2
                coupon_object.sa_phone_number=dealer_sa_object.service_advisor_id
                coupon_object.servicing_dealer=dealer_sa_object.dealer_id
                coupon_object.closed_date = datetime.now()
                coupon_object.save()
#                 common.CouponData.objects.filter(Q(status=1) | Q(status=4), vin__vin=vin, service_type__lt=coupon_object.service_type).update(status=3)
                message = templates.get_template('SEND_SA_CLOSE_COUPON').format(customer_id=sap_customer_id, usc=unique_service_coupon)
            else:
                message = templates.get_template('SEND_SA_WRONG_CUSTOMER_UCN')
        except Exception as ex:
            logger.error("[Exception_coupon_close]".format(ex))
            message = templates.get_template('SEND_INVALID_MESSAGE')
        finally:
            logger.info("Close coupon with message %s" % message)
            phone_number = utils.get_phone_number_format(phone_number)
            if settings.ENABLE_AMAZON_SQS:
                task_queue = get_task_queue()
                task_queue.add("send_coupon", {"phone_number":phone_number, "message": message, "sms_client":settings.SMS_CLIENT})
            else:
                send_coupon.delay(phone_number=phone_number, message=message, sms_client=settings.SMS_CLIENT)
            audit.audit_log(reciever=phone_number, action=AUDIT_ACTION, message=message)
        return {'status': True, 'message': message}

    def validate_dealer(self, phone_number):
        all_sa_dealer_obj = aftersell_common.ServiceAdvisorDealerRelationship.objects.filter(service_advisor_id__phone_number = phone_number, status = u'Y')
        if len(all_sa_dealer_obj) == 0:
            message=templates.get_template('UNAUTHORISED_SA')
            sa_phone = utils.get_phone_number_format(phone_number)
            if settings.ENABLE_AMAZON_SQS:
                task_queue = get_task_queue()
                task_queue.add("send_invalid_keyword_message", {"phone_number":sa_phone, "message": message, "sms_client":settings.SMS_CLIENT})
            else:
                send_invalid_keyword_message.delay(phone_number=sa_phone, message=message, sms_client=settings.SMS_CLIENT)
            return None
        service_advisor_obj = all_sa_dealer_obj[0]
        return service_advisor_obj

    def is_sa_initiator(self, coupon_id, dealer_sa_data, phone_number):
        coupon_data = common.CouponData.objects.filter(unique_service_coupon = coupon_id)
        coupon_sa_obj = common.ServiceAdvisorCouponRelationship.objects.filter(unique_service_coupon=coupon_data\
                                                                                   ,service_advisor_phone=dealer_sa_data.service_advisor_id\
                                                                                   ,dealer_id=dealer_sa_data.dealer_id)
        if len(coupon_sa_obj)>0:
            return True
        else:
            sa_phone = utils.get_phone_number_format(phone_number)
            message = "SA is not the coupon initiator."
            if settings.ENABLE_AMAZON_SQS:
                task_queue = get_task_queue()
                task_queue.add("send_invalid_keyword_message", {"phone_number":sa_phone, "message": message, "sms_client":settings.SMS_CLIENT})
            else:
                send_invalid_keyword_message.delay(phone_number=sa_phone, message=message, sms_client=settings.SMS_CLIENT)
        return False
        
    
    def is_valid_data(self, customer_id=None, coupon=None, sa_phone=None):
        '''
            Error During wrong entry of Customer ID or UCN (message to the service advisor)
            -    "Wrong Customer ID or UCN"
        '''
        coupon_obj = customer_obj = message = None
        if coupon: coupon_obj = common.CouponData.objects.filter(unique_service_coupon=coupon)
        if customer_id:
            customer_id = utils.get_updated_customer_id(customer_id) 
            customer_obj = common.ProductData.objects.filter(sap_customer_id=customer_id)

        if ((customer_obj and coupon_obj and coupon_obj[0].vin.vin != customer_obj[0].vin) or\
            (not customer_obj and not coupon_obj)):
            message=templates.get_template('SEND_SA_WRONG_CUSTOMER_UCN')

        elif customer_id and not customer_obj:
            message=templates.get_template('SEND_SA_WRONG_CUSTOMER_UCN')
        elif coupon and not coupon_obj:
            message=templates.get_template('SEND_SA_WRONG_CUSTOMER_UCN')

        if message:
            sa_phone = utils.get_phone_number_format(sa_phone)
            if settings.ENABLE_AMAZON_SQS:
                task_queue = get_task_queue()
                task_queue.add("send_invalid_keyword_message", {"phone_number":sa_phone, "message": message, "sms_client":settings.SMS_CLIENT})
            else:
                send_invalid_keyword_message.delay(phone_number=sa_phone, message=message, sms_client=settings.SMS_CLIENT)
            audit.audit_log(reciever=sa_phone, action=AUDIT_ACTION, message=message)
            logger.info("Message sent to SA : " + message)
            return False
        return True


    def get_brand_data(self, sms_dict, phone_number):
        brand_id = sms_dict['brand_id']
        try:
            product_data = common.ProductData.objects.select_related('product_type__brand_id').filter(customer_phone_number__phone_number=phone_number, product_type__brand_id__brand_id=brand_id)
            if product_data:
                product_list = map(lambda object: {'sap_customer_id':object.sap_customer_id, 'vin': object.vin}, product_data)
                template = templates.get_template('SEND_BRAND_DATA')
                msg_list = [template.format(**key_args) for key_args in product_list]
                message = ', '.join(msg_list)
            else: 
                raise Exception
        except Exception as ex:
            message = templates.get_template('SEND_INVALID_MESSAGE')
        send_brand_sms_customer.delay(phone_number=phone_number, message=message)
        audit.audit_log(reciever=phone_number, action=AUDIT_ACTION, message=message)
        return True

    def determine_format(self, request):
        return 'application/json'

    def get_complain_data(self, sms_dict, phone_number, with_detail=False):
        ''' Save the feedback or complain from SA and sends SMS for successfully receive '''
        try:
            role = self.check_role_of_initiator(phone_number)
            if with_detail:
                sa_name = aftersell_common.ServiceAdvisor.objects.filter(phone_number=phone_number)
                gladminds_feedback_object = aftersell_common.Feedback(reporter=phone_number,
                                                                priority=sms_dict['priority'] , type=sms_dict['type'], 
                                                                subject=sms_dict['subject'], message=sms_dict['message'],
                                                                status="Open", created_date=datetime.now(),
                                                                role=role, reporter_name=sa_name[0].name
                                                                )
            else:
                gladminds_feedback_object = aftersell_common.Feedback(reporter=phone_number,
                                                                message=sms_dict['message'], status="Open",
                                                                created_date=datetime.now(),
                                                                role=role
                                                                )
            gladminds_feedback_object.save()
            message = templates.get_template('SEND_RCV_FEEDBACK').format(type=gladminds_feedback_object.type)
        except Exception as ex:
            message = templates.get_template('SEND_INVALID_MESSAGE')
        finally:
            logger.info("Send complain message received successfully with %s" % message)
            phone_number = utils.get_phone_number_format(phone_number)
            if settings.ENABLE_AMAZON_SQS:
                task_queue = get_task_queue()
                task_queue.add("send_coupon", {"phone_number":phone_number, "message": message})
            else:
                send_coupon.delay(phone_number=phone_number, message=message)
            gladminds_feedback_object = aftersell_common.Feedback.objects.get(id=gladminds_feedback_object.id)
            context = create_context('FEEDBACK_DETAIL_TO_ADIM',  gladminds_feedback_object)
            send_feedback_received(context)
            if gladminds_feedback_object.reporter_email_id:
                context = create_context('FEEDBACK_CONFIRMATION',  gladminds_feedback_object)
                send_servicedesk_feedback(context, gladminds_feedback_object)
            else:
                logger.info("Reporter emailId not found.")
            audit.audit_log(reciever=phone_number, action=AUDIT_ACTION, message = message)
        return {'status': True, 'message': message}

    def check_role_of_initiator(self, phone_number):
        active_sa = self.validate_dealer(phone_number)
        if  active_sa:
            return "SA"
        else:
            check_customer_obj = common.GladMindUsers.objects.filter(
                                                    phone_number=phone_number)
            if check_customer_obj:
                return "Customer"
            else:
                return "other"



#########################AfterBuy Resources############################################
class GladmindsBaseResource(ModelResource):
    def determine_format(self, request):
        return 'application/json'


class UserResources(GladmindsBaseResource):
    products = fields.ListField()
    class Meta:
        queryset = common.GladMindUsers.objects.all()
        resource_name = 'users'
        authentication = AccessTokenAuthentication()

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/otp%s" % (self._meta.resource_name, trailing_slash()), self.wrap_view('process_otp'), name="validate_otp"),
            url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/products%s" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_products'), name="api_get_products"),
        ]    
        
    def obj_get(self, bundle, **kwargs):
        request = bundle.request
        customer_id = kwargs['pk']
        try:
            customer_detail = common.GladMindUsers.objects.get(gladmind_customer_id=customer_id)
            return customer_detail
        except:
            raise ImmediateHttpResponse(response=http.HttpBadRequest())
    
    def obj_create(self, bundle, **kwargs):
        """
        A ORM-specific implementation of ``obj_create``.
        """
#        bundle.obj = self._meta.object_class()
#        for key, value in kwargs.items():
#            setattr(bundle.obj, key, value)
#
#        bundle = self.full_hydrate(bundle)
#        return self.save(bundle)
        return bundle
    
    def get_products(self, request, **kwargs):
        user_id = kwargs['pk']
        products = common.ProductData.objects.filter(customer_phone_number__gladmind_customer_id=user_id).select_related('customer_phone_number')
        products = [model_to_dict(product) for product in products]
        to_be_serialized = {"products": products}
        return self.create_response(request, data=to_be_serialized)
    
    def dehydrate(self, bundle):
        products = common.ProductData.objects.filter(customer_phone_number__id=bundle.data['id']).select_related('customer_phone_number')
        bundle.data['products'] = [model_to_dict(product) for product in products]
        return bundle
    
    def process_otp(self, bundle, **kwargs):
        if bundle.GET.get('otp', None) and bundle.GET.get('user_id', None):
            try:
                customer_phone = common.ProductData.objects.filter(sap_customer_id=bundle.GET['user_id'])[0]
                http_class=HttpResponse
                data={'status':True}
            except:
                http_class=HttpResponseBadRequest
                data={'message':'User does not exist.'}
        elif bundle.GET.get('user_id', None):
            try:
                #TODO: Implement real API
                customer_phone = common.ProductData.objects.filter(sap_customer_id=bundle.GET['user_id'])[0]
                http_class=HttpResponse
                data={'message':'OTP has been sent to user mobile.'}
            except:
                http_class=HttpResponseBadRequest
                data={'message':'User does not exist.'}
        else:
            http_class=HttpResponseBadRequest
            data={'message': 'Invalid OTP or User.'}
        
        return self.create_response(bundle, response_class=http_class, data=data)
        

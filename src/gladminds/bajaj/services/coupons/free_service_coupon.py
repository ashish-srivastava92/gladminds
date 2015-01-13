'''Handlers for free service coupon logic'''

import logging
from datetime import datetime, timedelta

from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.conf import settings
from django.db.models import Q

from gladminds.core.managers import sms_parser
from gladminds.core.managers.audit_manager import sms_log
from gladminds.core.services import message_template as templates
from gladminds.bajaj import models
from gladminds.sqs_tasks import send_registration_detail, send_service_detail, \
    send_coupon_detail_customer, send_coupon, \
    send_brand_sms_customer, send_invalid_keyword_message,\
    customer_detail_recovery
from gladminds.core import utils
from gladminds.bajaj.services.coupons.import_feed import BaseFeed
from gladminds.settings import COUPON_VALID_DAYS
from gladminds.core.base_models import STATUS_CHOICES
from gladminds.core.cron_jobs.queue_utils import send_job_to_queue
from gladminds.core.core_utils.utils import log_time

LOG = logging.getLogger('gladminds')
json = utils.import_json()


__all__ = ['GladmindsTaskManager']
AUDIT_ACTION = 'SEND TO QUEUE'


@log_time
def register_customer(sms_dict, phone_number):
    customer_name = sms_dict['name']
    email_id = sms_dict['email_id']
    try:
        object = models.UserProfile.objects.get(phone_number=phone_number)
        gladmind_customer_id = object.gladmind_customer_id
        customer_name = object.customer_name
    except ObjectDoesNotExist as odne:
        gladmind_customer_id = utils.generate_unique_customer_id()
        registration_date = datetime.now()
        user_feed = BaseFeed()
        user = user_feed.register_user('customer', username=gladmind_customer_id)

#             FIXME: Check this code is getting used or not
#             customer = models.UserProfile(
#                 user=user, gladmind_customer_id=gladmind_customer_id, phone_number=phone_number,
#                 customer_name=customer_name, email_id=email_id,
#                 registration_date=registration_date)
#             customer.save()

    # Please update the template variable before updating the keyword-argument
    message = sms_parser.render_sms_template(status='send', keyword=sms_dict['keyword'], customer_id=gladmind_customer_id)
    phone_number = utils.get_phone_number_format(phone_number)
    LOG.info("customer is registered with message %s" % message)
    sms_log(receiver=phone_number, action=AUDIT_ACTION, message=message)
    send_job_to_queue(send_registration_detail, {"phone_number":phone_number, "message":message, "sms_client":settings.SMS_CLIENT})
    return True


@log_time
def send_customer_detail(sms_dict, phone_number):
    keyword = sms_dict['params']
    value = sms_dict['message']
    kwargs = {}
    kwargs['customer_phone_number__endswith'] = utils.get_phone_number_format(phone_number)
    if value and len(value)>5 and keyword in ['vin', 'id']:
        if keyword == 'id':
            kwargs['customer_id'] = value
            model_key = 'vin'
            search_key = 'product_id'
        else:
            kwargs['product_id__endswith'] = value
            model_key = 'id'
            search_key = 'customer_id'

        try:
            product_object = models.ProductData.objects.get(**kwargs)
            if product_object.customer_id:
                message = templates.get_template('SEND_CUSTOMER_DETAILS').format(model_key, getattr(product_object, search_key))
            else:
                message = templates.get_template('INVALID_RECOVERY_MESSAGE').format(keyword)
        
        except Exception as ex:
            LOG.info('Details not found with message %s' % ex)
            message = templates.get_template('INVALID_RECOVERY_MESSAGE').format(keyword)
    else:
        message = templates.get_template('SEND_INVALID_MESSAGE')

    sms_log(receiver=phone_number, action=AUDIT_ACTION, message=message)
    send_job_to_queue(customer_detail_recovery, {"phone_number":phone_number, "message":message, "sms_client":settings.SMS_CLIENT})
    return {'status': True, 'message': message}


@log_time
def customer_service_detail(sms_dict, phone_number):
    customer_id = sms_dict.get('sap_customer_id', None)
    message = None
    try:
        customer_product_data = models.CouponData.objects.select_related('product').\
                                    filter(product__customer_phone_number=phone_number, \
                                    product__customer_id=customer_id).\
                                    order_by('product', 'valid_days') if customer_id else \
                                    models.CouponData.objects.select_related('product').\
                                    filter(product__customer_phone_number=phone_number).\
                                    order_by('product', 'valid_days')
        LOG.info(customer_product_data)
        valid_product_data = []
        for data in customer_product_data:
            if data.status == 1 or data.status == 4:
                valid_product_data.append(data)
        valdata = [valid_product_data[0]]
        service_list = map(lambda object: {'vin': object.product.product_id, 'usc': object.unique_service_coupon, 'valid_days': object.valid_days, 'valid_kms':object.valid_kms}, valdata)
        template = templates.get_template('SEND_CUSTOMER_SERVICE_DETAIL')
        msg_list = [template.format(**key_args) for key_args in service_list]
        if not msg_list:
            raise Exception()
        message = ', '.join(msg_list)
    except Exception as ex:
        message = sms_parser.render_sms_template(status='invalid', keyword=sms_dict['keyword'], sap_customer_id=customer_id)
    LOG.info("Send Service detail %s" % message)
    phone_number = utils.get_phone_number_format(phone_number)
    sms_log(receiver=phone_number, action=AUDIT_ACTION, message=message)
    send_job_to_queue(send_service_detail, {"phone_number":phone_number, "message":message, "sms_client":settings.SMS_CLIENT})
    return {'status': True, 'message': message}


def get_customer_phone_number_from_vin(vin):
    product_obj = models.ProductData.objects.filter(product_id=vin)
    return product_obj[0].customer_phone_number


def update_higher_range_coupon(kms, product):
    '''
        Update those coupon have higher value than the least in progress
        coupon. These case existed because some time user add higher value
        of kilometer.
    '''
    updated_coupon = models.CouponData.objects\
                    .filter(Q(status=4) | Q(status=5), product=product, valid_kms__gt=kms)\
                    .update(status=1, service_advisor=None, actual_kms=None,
                            actual_service_date=None)
    LOG.info("%s have higher KMS range" % updated_coupon)


def update_exceed_limit_coupon(actual_kms, product):
    '''
        Exceed Limit those coupon whose kms limit is small then actual kms limit
    '''
    exceed_limit_coupon = models.CouponData.objects\
        .filter(Q(status=1) | Q(status=4), product=product, valid_kms__lt=actual_kms)\
        .update(status=5, actual_kms=actual_kms)
    LOG.info("%s are exceed limit coupon" % exceed_limit_coupon)


def get_product(customer_id):
    try:
        customer_id = models.CustomerTempRegistration.objects.get_updated_customer_id(customer_id)
        product_data=models.ProductData.objects.get(customer_id=customer_id)
        return product_data
    except Exception as ax:
        LOG.error("Vin is not in customer_product_data Error %s " % ax)


def update_coupon(valid_coupon, actual_kms, service_advisor, status,\
                                             update_time):
    valid_coupon.actual_kms = actual_kms
    valid_coupon.actual_service_date = update_time
    valid_coupon.extended_date = update_time + timedelta(days=COUPON_VALID_DAYS)
    valid_coupon.status = status
    valid_coupon.service_advisor = service_advisor
    valid_coupon.save()


def update_inprogress_coupon(coupon, actual_kms, service_advisor):
    LOG.info("Expired on %s" % coupon.mark_expired_on)
    LOG.info("Extended on %s" % coupon.extended_date)
    expiry_date = coupon.mark_expired_on
    if coupon.extended_date < expiry_date:
        coupon.extended_date = expiry_date
        coupon.save()

    validity_date = coupon.extended_date
    today = timezone.now()
    current_time = datetime.now()
    if expiry_date >= today:
        coupon.extended_date = current_time + timedelta(days=COUPON_VALID_DAYS)
        update_coupon(coupon, actual_kms, service_advisor, 4, current_time)
    elif validity_date >= today and expiry_date < today:
        coupon.actual_service_date = current_time
        coupon.save()


def get_requested_coupon_status(product, service_type):
    requested_coupon = models.CouponData.objects.filter(product=product,
                                                service_type=service_type) 
    if not requested_coupon:
        status = "not available"
    else:
        status = STATUS_CHOICES[requested_coupon[0].status - 1][1]
    return status


@log_time
def validate_coupon(sms_dict, phone_number):
    actual_kms = int(sms_dict['kms'])
    service_type = sms_dict['service_type']
    dealer_message = None
    customer_message = None
    customer_phone_number = None
    customer_message_countdown = settings.DELAY_IN_CUSTOMER_UCN_MESSAGE
    sap_customer_id = sms_dict.get('sap_customer_id', None)
    service_advisor = validate_service_advisor(phone_number)
    if not service_advisor:
        return {'status': False, 'message': templates.get_template('UNAUTHORISED_SA')}
    if not is_valid_data(customer_id=sap_customer_id, sa_phone=phone_number):
        return {'status': False, 'message': templates.get_template('SEND_SA_WRONG_CUSTOMER_UCN')}
    try:
        product = get_product(sap_customer_id)
        LOG.info("Associated product %s" % product)
        update_exceed_limit_coupon(actual_kms, product)
        valid_coupon = models.CouponData.objects.filter(Q(status=1) | Q(status=4) | Q(status=5), product=product,
                        valid_kms__gte=actual_kms, service_type=service_type) \
                       .select_related('vin', 'customer_phone_number__phone_number').order_by('service_type')
        LOG.info("List of available valid coupons %s" % valid_coupon)
        if len(valid_coupon) > 0:
            update_higher_range_coupon(valid_coupon[0].valid_kms, product)
            valid_coupon = valid_coupon[0]
            LOG.info("valid coupon %s" % valid_coupon)
            coupon_sa_obj = models.ServiceAdvisorCouponRelationship.objects.filter(unique_service_coupon=valid_coupon\
                                                                                   ,service_advisor=service_advisor)
            LOG.info('Coupon_sa_obj exists: %s' % coupon_sa_obj)
            if not len(coupon_sa_obj):
                coupon_sa_obj = models.ServiceAdvisorCouponRelationship(unique_service_coupon=valid_coupon\
                                                                        ,service_advisor=service_advisor)
                coupon_sa_obj.save()
                LOG.info('Coupon obj created: %s' % coupon_sa_obj)

        in_progress_coupon = models.CouponData.objects.filter(product=product, valid_kms__gte=actual_kms, status=4) \
                             .select_related ('product').order_by('service_type')
        try:
            customer_phone_number = product.customer_phone_number
        except Exception as ax:
            LOG.error('Customer Phone Number is not stored in DB %s' % ax)
        if len(in_progress_coupon) > 0:
            update_inprogress_coupon(in_progress_coupon[0], actual_kms, service_advisor)
            LOG.info("Validate_coupon: Already in progress coupon")
            dealer_message = templates.get_template('COUPON_ALREADY_INPROGRESS').format(
                                                service_type=in_progress_coupon[0].service_type,
                                                customer_id=sap_customer_id)
            customer_message = templates.get_template('SEND_CUSTOMER_VALID_COUPON').format(
                                                coupon=in_progress_coupon[0].unique_service_coupon,
                                                service_type=in_progress_coupon[0].service_type)
        elif valid_coupon:
            LOG.info("Validate_coupon: valid coupon")
            update_coupon(valid_coupon, actual_kms, service_advisor, 4, datetime.now())
            dealer_message = templates.get_template('SEND_SA_VALID_COUPON').format(
                                            service_type=valid_coupon.service_type,
                                            customer_id=sap_customer_id)

            customer_message = templates.get_template('SEND_CUSTOMER_VALID_COUPON').format(
                                        coupon=valid_coupon.unique_service_coupon,
                                        service_type=valid_coupon.service_type)
        else:
            LOG.info("Validate_coupon: No valid or in-progress coupon")
            requested_coupon_status = get_requested_coupon_status(product, service_type)
            dealer_message = templates.get_template('SEND_SA_OTHER_VALID_COUPON').format(
                                        req_service_type=service_type,
                                        req_status=requested_coupon_status,
                                        customer_id=sap_customer_id)

        sms_log(receiver=customer_phone_number, action=AUDIT_ACTION, message=customer_message)
        send_job_to_queue(send_coupon_detail_customer, {"phone_number":utils.get_phone_number_format(customer_phone_number), "message":customer_message, "sms_client":settings.SMS_CLIENT},
                          delay_seconds=customer_message_countdown)

    except Exception as ex:
        LOG.info('[validate_coupon]:Exception : '.format(ex))
        dealer_message = templates.get_template('SEND_INVALID_MESSAGE')
    finally:
        LOG.info("validate message send to SA %s" % dealer_message)
        phone_number = utils.get_phone_number_format(phone_number)
        sms_log(receiver=phone_number, action=AUDIT_ACTION, message=dealer_message)
        send_job_to_queue(send_service_detail, {"phone_number": phone_number,
                                                "message": dealer_message,
                                                "sms_client": settings.SMS_CLIENT})
    return {'status': True, 'message': dealer_message}


@log_time
def close_coupon(sms_dict, phone_number):
    service_advisor = validate_service_advisor(phone_number)
    unique_service_coupon = sms_dict['usc']
    sap_customer_id = sms_dict.get('sap_customer_id', None)
    message = None
    if not service_advisor:
        return {'status': False, 'message': templates.get_template('UNAUTHORISED_SA')}
    if not is_valid_data(customer_id=sap_customer_id, coupon=unique_service_coupon, sa_phone=phone_number):
        return {'status': False, 'message': templates.get_template('SEND_SA_WRONG_CUSTOMER_UCN')}
    if not is_sa_initiator(unique_service_coupon, service_advisor, phone_number):
        return {'status': False, 'message': "SA is not the coupon initiator."}
    try:
        product = get_product(sap_customer_id)
        coupon_object = models.CouponData.objects.filter(product=product,
                        unique_service_coupon=unique_service_coupon).select_related ('product')[0]
        if coupon_object.status == 2 or coupon_object.status == 6:
            message = templates.get_template('COUPON_ALREADY_CLOSED')
        elif coupon_object.status == 4:
            customer_phone_number = coupon_object.product.customer_phone_number
            coupon_object.status = 2
            coupon_object.service_advisor=service_advisor
            coupon_object.closed_date = datetime.now()
            coupon_object.save()
            message = templates.get_template('SEND_SA_CLOSE_COUPON').format(customer_id=sap_customer_id, usc=unique_service_coupon)
        else:
            message = templates.get_template('SEND_SA_WRONG_CUSTOMER_UCN')
    except Exception as ex:
        LOG.error("[Exception_coupon_close] {0}".format(ex))
        message = templates.get_template('SEND_INVALID_MESSAGE')
    finally:
        LOG.info("Close coupon with message %s" % message)
        phone_number = utils.get_phone_number_format(phone_number)
        sms_log(receiver=phone_number, action=AUDIT_ACTION, message=message)
        send_job_to_queue(send_coupon, {"phone_number":phone_number, "message": message, "sms_client":settings.SMS_CLIENT})
    return {'status': True, 'message': message}


def validate_service_advisor(phone_number):
    all_sa_dealer_obj = models.ServiceAdvisor.objects.active(phone_number)
    if len(all_sa_dealer_obj) == 0:
        message=templates.get_template('UNAUTHORISED_SA')
        sa_phone = utils.get_phone_number_format(phone_number)
        sms_log(receiver=sa_phone, action=AUDIT_ACTION, message=message)
        send_job_to_queue(send_service_detail, {"phone_number":sa_phone, "message": message, "sms_client":settings.SMS_CLIENT})
        return None
    service_advisor_obj = all_sa_dealer_obj[0]
    return service_advisor_obj


def is_sa_initiator(coupon_id, service_advisor, phone_number):
    coupon_data = models.CouponData.objects.filter(unique_service_coupon = coupon_id)
    coupon_sa_obj = models.ServiceAdvisorCouponRelationship.objects.filter(unique_service_coupon=coupon_data\
                                                                               ,service_advisor=service_advisor)
    if len(coupon_sa_obj)>0:
        return True
    else:
        sa_phone = utils.get_phone_number_format(phone_number)
        message = "SA is not the coupon initiator."
        sms_log(receiver=sa_phone, action=AUDIT_ACTION, message=message)
        send_job_to_queue(send_invalid_keyword_message, {"phone_number":sa_phone, "message": message, "sms_client":settings.SMS_CLIENT})
    return False


def is_valid_data(customer_id=None, coupon=None, sa_phone=None):
    '''
        Error During wrong entry of Customer ID or UCN (message to the service advisor)
        -    "Wrong Customer ID or UCN"
    '''
    coupon_obj = customer_obj = []
    message = ''
    if coupon: 
        coupon_obj = models.CouponData.objects.filter(unique_service_coupon=coupon)
    if customer_id:
        customer_id = models.CustomerTempRegistration.objects.get_updated_customer_id(customer_id)
        customer_obj = models.ProductData.objects.filter(customer_id=customer_id)
    if ((customer_obj and coupon_obj and coupon_obj[0].product.product_id != customer_obj[0].product_id) or\
        (not customer_obj and not coupon_obj)):
        message = templates.get_template('SEND_SA_WRONG_CUSTOMER_UCN')

    elif customer_id and not customer_obj:
        message = templates.get_template('SEND_SA_WRONG_CUSTOMER_UCN')
    elif coupon and not coupon_obj:
        message = templates.get_template('SEND_SA_WRONG_CUSTOMER_UCN')

    if message:
        sa_phone = utils.get_phone_number_format(sa_phone)
        sms_log(receiver=sa_phone, action=AUDIT_ACTION, message=message)
        send_job_to_queue(send_invalid_keyword_message, {"phone_number":sa_phone, "message": message, "sms_client":settings.SMS_CLIENT})
        LOG.info("Message sent to SA : " + message)
        return False
    return True


def get_brand_data(sms_dict, phone_number):
    product_type = sms_dict['brand_id']
    try:
        product_data = models.ProductData.objects.select_related('product_type').filter(customer_phone_number=phone_number, product_type__product_type=product_type)
        if product_data:
            product_list = map(lambda object: {'sap_customer_id':object.customer_id, 'vin': object.product_id}, product_data)
            template = templates.get_template('SEND_BRAND_DATA')
            msg_list = [template.format(**key_args) for key_args in product_list]
            message = ', '.join(msg_list)
        else: 
            raise Exception
    except Exception as ex:
        message = templates.get_template('SEND_INVALID_MESSAGE')
    sms_log(receiver=phone_number, action=AUDIT_ACTION, message=message)
    send_job_to_queue(send_brand_sms_customer, {"phone_number": phone_number,
                                                "message": message})
    return {'status': True, 'message': message}

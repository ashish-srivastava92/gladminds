'''Handlers for loyalty logic'''

import logging
import json

from django.conf import settings
from django.http.response import HttpResponse
from gladminds.core.managers.audit_manager import sms_log
from gladminds.bajaj.services import message_template as templates
from gladminds.bajaj import models
from gladminds.sqs_tasks import send_point, send_loyalty_sms
from gladminds.core import utils, constants
from gladminds.core.cron_jobs.queue_utils import get_task_queue, send_job_to_queue

LOG = logging.getLogger('gladminds')

__all__ = ['GladmindsTaskManager']
AUDIT_ACTION = 'SEND TO QUEUE'

def send_welcome_sms(mech):
    phone_number=utils.get_phone_number_format(mech.phone_number)
    message=templates.get_template('WELCOME_MESSAGE').format(
                    mechanic_name=mech.first_name,)
    sms_log(receiver=phone_number, action=AUDIT_ACTION, message=message)
    send_job_to_queue(send_loyalty_sms, {'phone_number': phone_number,
                            'message': message, "sms_client": settings.SMS_CLIENT})

def send_welcome_message(request):
    if  (settings.ENV in settings.IGNORE_ENV):
        return HttpResponse(json.dumps({'msg': 'Messages not to be sent in this env'}),
                            content_type='application/json')
    phone_list=[]
    mechanics = models.Mechanic.objects.filter(sent_sms=False)
    for mech in mechanics:
        send_welcome_sms(mech)
        phone_list.append(mech.phone_number)
    mechanics.update(sent_sms=True)
    response = 'Message sent to {0} mechanics with phone numbers {1}'.format(len(phone_list), (', '.join(phone_list)))
    return HttpResponse(json.dumps({'msg': response}), content_type='application/json')


def update_points(mechanic, accumulate=0, redeem=0):
    '''Update the loyalty points of the user'''
    total_points = mechanic.total_points + accumulate -redeem
    mechanic.total_points = total_points
    mechanic.save()
    return total_points

def fetch_catalogue_products(product_codes):
    '''Fetches all the products with given upc'''
    products = models.ProductCatalog.objects.filter(product_id__in=product_codes)
    return products

def accumulate_point(sms_dict, phone_number):
    '''accumulate points with given upc'''
    unique_product_codes = (sms_dict['ucp'].upper()).split()
    valid_ucp=[]
    valid_product_number=[]
    invalid_upcs_message=''
    try:
        if len(unique_product_codes)>constants.MAX_UCP_ALLOWED:
            message=templates.get_template('MAX_ALLOWED_UCP').format(
                                    max_limit=constants.MAX_UCP_ALLOWED)
            raise ValueError('Maximum allowed ucp exceeded')
        mechanic = models.Mechanic.objects.filter(phone_number=utils.mobile_format(phone_number))
        if not mechanic:
            message=templates.get_template('UNREGISERED_USER')
            raise ValueError('Unregistered user')
        accumulation_log=models.AccumulationRequest(member=mechanic[0],
                                                    points=0,total_points=0)
        accumulation_log.save()
        spares = models.SpareUPCData.objects.get_spare_parts(unique_product_codes)
        added_points=0

        for spare in spares:
            valid_product_number.append(spare.part_number)
            valid_ucp.append(spare.unique_part_code)
            accumulation_log.upcs.add(spare)
        spare_points = models.SparePointData.objects.get_part_number(valid_product_number)
        for spare_point in spare_points:
            added_points=added_points+spare_point.points
        total_points=update_points(mechanic[0],accumulate=added_points)
        accumulation_log.points=added_points
        invalid_upcs = list(set(unique_product_codes).difference(valid_ucp))
        if invalid_upcs:
            invalid_upcs_message=' List of invalid part code: {0}.'.format(
                                                    (', '.join(invalid_upcs)))
        message=templates.get_template('SEND_ACCUMULATED_POINT').format(
                        mechanic_name=mechanic[0].first_name,
                        added_points=added_points,
                        total_points=total_points,
                        invalid_upcs=invalid_upcs_message)
        spares.update(is_used=True)
        accumulation_log.total_points=total_points
        accumulation_log.save()
    except Exception as ex:
        LOG.error('[accumulate_point]:{0}:: {1}'.format(phone_number, ex))
    finally:
        phone_number = utils.get_phone_number_format(phone_number)
        sms_log(receiver=phone_number, action=AUDIT_ACTION, message=message)
        send_job_to_queue(send_point, {'phone_number': phone_number,
                        'message': message, "sms_client": settings.SMS_CLIENT})
    return {'status': True, 'message': message}

def redeem_point(sms_dict, phone_number):
    '''redeem points with given upc'''
    product_codes = sms_dict['product_id'].upper().split()
    try:
        mechanic = models.Mechanic.objects.filter(phone_number=utils.mobile_format(phone_number))
        if not mechanic:
            message=templates.get_template('UNREGISERED_USER')
            raise ValueError('Unregistered user')
        products=fetch_catalogue_products(product_codes)
        redeem_points=0

        for product in products:
            redeem_points=redeem_points+product.points
        left_points=mechanic[0].total_points-redeem_points
        if left_points>=0:
            total_points=update_points(mechanic[0],redeem=redeem_points)
            message=templates.get_template('SEND_REDEEM_POINT').format(
                            mechanic_name=mechanic[0].first_name,
                            product_code=sms_dict['product_id'],
                            total_points=total_points)
        else:
            message=templates.get_template('SEND_INSUFFICIENT_POINT').format(
                            shortage_points=abs(left_points))
    except Exception as ex:
        LOG.error('[redeem_point]:{0}:: {1}'.format(phone_number, ex))
    finally:
        phone_number = utils.get_phone_number_format(phone_number)
        if settings.ENABLE_AMAZON_SQS:
            task_queue = get_task_queue()
            task_queue.add("send_point", {"phone_number":phone_number,
                                          "message": message,
                                          "sms_client":settings.SMS_CLIENT})
        else:
            send_point.delay(phone_number=phone_number,
                             message=message,
                             sms_client=settings.SMS_CLIENT)
        sms_log(receiver=phone_number, action=AUDIT_ACTION, message=message)
    return {'status': True, 'message': message}

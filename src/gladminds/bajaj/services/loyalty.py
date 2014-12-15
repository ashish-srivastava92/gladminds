'''Handlers for loyalty logic'''

import logging

from django.conf import settings
from gladminds.core.managers.audit_manager import sms_log
from gladminds.bajaj.services import message_template as templates
from gladminds.bajaj import models
from gladminds.sqs_tasks import send_point
from gladminds.core import utils

LOG = logging.getLogger('gladminds')

__all__ = ['GladmindsTaskManager']
AUDIT_ACTION = 'SEND TO QUEUE'

def update_points(mechanic, accumulate=0, redeem=0):
    '''Update the loyalty points of the user'''
    total_points = mechanic.total_points + accumulate -redeem
    mechanic.total_points = total_points
    mechanic.save()
    return total_points

def fetch_spare_products(spare_product_codes):
    '''Fetches all the spare parts with given upc'''
    spares = models.SparePart.objects.filter(unique_part_code__in=spare_product_codes,
                                             is_used=False)
    return spares

def fetch_catalogue_products(product_codes):
    '''Fetches all the products with given upc'''
    products = models.ProductCatalog.objects.filter(product_id__in=product_codes)
    return products

def get_mechanic(phone_number):
    '''Fetches detail of mechanic with given mobile number'''
    mechanic = models.Mechanic.objects.filter(user__phone_number=phone_number)
    return mechanic

def accumulate_point(sms_dict, phone_number):
    '''accumulate points with given upc'''
    unique_product_codes = sms_dict['ucp'].split()
    valid_ucp=[]
    invalid_upcs_message=''
    try:
        if len(unique_product_codes)>settings.MAX_UCP_ALLOWED:
            message=templates.get_template('MAX_ALLOWED_UCP').format(
                                    max_limit=settings.MAX_UCP_ALLOWED)
            raise ValueError('Maximum allowed ucp exceeded')
        mechanic = get_mechanic(utils.mobile_format(phone_number))
        if not mechanic:
            message=templates.get_template('UNREGISERED_USER')
            raise ValueError('Unregistered user')
        spares=fetch_spare_products(unique_product_codes)
        added_points=0

        for spare in spares:
            added_points=added_points+spare.points
            valid_ucp.append(spare.unique_part_code)
        total_points=update_points(mechanic[0],accumulate=added_points)
        invalid_upcs = list(set(unique_product_codes).difference(valid_ucp))
        if invalid_upcs:
            invalid_upcs_message=' List of invalid part code: {0}.'.format(
                                                    (', '.join(invalid_upcs)))
        message=templates.get_template('SEND_ACCUMULATED_POINT').format(
                        mechanic_name=mechanic[0].user.user.first_name,
                        added_points=added_points,
                        total_points=total_points,
                        invalid_upcs=invalid_upcs_message)
        spares.update(is_used=True)
    except Exception as ex:
        LOG.error('[accumulate_point]:{0}:: {1}'.format(phone_number, ex))
    finally:
        phone_number = utils.get_phone_number_format(phone_number)
        if settings.ENABLE_AMAZON_SQS:
            task_queue = utils.get_task_queue()
            task_queue.add("send_point", {"phone_number":phone_number,
                                          "message": message,
                                          "sms_client":settings.SMS_CLIENT})
        else:
            send_point.delay(phone_number=phone_number,
                             message=message,
                             sms_client=settings.SMS_CLIENT)
        sms_log(receiver=phone_number, action=AUDIT_ACTION, message=message)
    return {'status': True, 'message': message}

def redeem_point(sms_dict, phone_number):
    '''redeem points with given upc'''
    product_codes = sms_dict['product_id'].upper().split()
    try:
        mechanic = get_mechanic(utils.mobile_format(phone_number))
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
                            mechanic_name=mechanic[0].name,
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
            task_queue = utils.get_task_queue()
            task_queue.add("send_point", {"phone_number":phone_number,
                                          "message": message,
                                          "sms_client":settings.SMS_CLIENT})
        else:
            send_point.delay(phone_number=phone_number,
                             message=message,
                             sms_client=settings.SMS_CLIENT)
        sms_log(receiver=phone_number, action=AUDIT_ACTION, message=message)
    return {'status': True, 'message': message}

'''Receives the sms and parse
   it to figure out the handlers'''

import logging

from django.conf.urls import url
from django.db import transaction
from django.conf import settings
from tastypie.http import HttpBadRequest
from tastypie.resources import Resource
from tastypie.exceptions import ImmediateHttpResponse

from gladminds.core.managers import sms_parser
from gladminds.core.managers.audit_manager import sms_log
from gladminds.sqs_tasks import send_invalid_keyword_message
from gladminds.core import utils
from gladminds.core.cron_jobs.queue_utils import send_job_to_queue

LOGGER = logging.getLogger('gladminds')
ANGULAR_FORMAT = lambda x: x.replace('{', '<').replace('}', '>')
AUDIT_ACTION = 'SEND TO QUEUE'

class SMSResources(Resource):

    class Meta:
        resource_name = 'messages'

    def base_urls(self):
        return [
            url(r"^messages", self.wrap_view('render_sms'))
        ]

    def render_sms(self, request, **kwargs):
        sms_dict = {}
        error_template = None
        phone_number = ""
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
                LOGGER.info('Validating the service coupon for customer {0}'.format(customer_id))
                odo_read = request.POST.get('odoRead')
                service_type = request.POST.get('serviceType')
                message = '{3} {0} {1} {2}'.format(customer_id, odo_read,
                    service_type, settings.ALLOWED_KEYWORDS['check'].upper())
                LOGGER.info('Message to send: ' + message)
            else:
                ucn = request.POST.get('ucn')
                LOGGER.info('Terminating the service coupon {0}'.format(ucn))
                message = '{2} {0} {1}'.format(customer_id,
                    ucn, settings.ALLOWED_KEYWORDS['close'].upper())
                LOGGER.info('Message to send: ' + message)
        phone_number = utils.get_phone_number_format(phone_number)
        message = utils.format_message(message)
        sms_log(action='RECEIVED', sender=phone_number,
                receiver='+1 469-513-9856', message=message)
        LOGGER.info('Received Message from phone number: {0} and message: {1}'.format(phone_number, message))
        try:
            sms_dict = sms_parser.sms_parser(message=message)
        except sms_parser.InvalidKeyWord as ink:
            error_template = ink.template
            error_message = ink.message
        except sms_parser.InvalidMessage as inm:
            error_template = inm.template
            error_message = inm.message
        except sms_parser.InvalidFormat as inf:
            error_template = ANGULAR_FORMAT('CORRECT FORMAT: ' + inf.template)
            error_message = inf.message
        if error_template:
            sms_log(receiver=phone_number,
                    action=AUDIT_ACTION, message=error_template)
            send_job_to_queue(send_invalid_keyword_message, {"phone_number":phone_number, "message":error_template, "sms_client":settings.SMS_CLIENT})
            
            raise ImmediateHttpResponse(HttpBadRequest(error_message))
        to_be_serialized = {}
        try:
            handler = utils.get_handler(sms_dict['handler'])
            with transaction.atomic():
                to_be_serialized = handler(sms_dict,
                                utils.mobile_format(phone_number))
        except Exception as ex:
            LOGGER.info("The database failed to perform {0}:{1}".format(
                                            request.POST.get('action'), ex))
        return self.create_response(request, data=to_be_serialized)
    
    def determine_format(self, request):
        return 'application/json'

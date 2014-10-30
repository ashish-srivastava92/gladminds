import os, logging, hashlib, uuid, mimetypes
import boto
from boto.s3.key import Key
import datetime
from dateutil import tz
from random import randint
from django.utils import timezone
from django.conf import settings
from django.template import Context
from gladminds.core import base_models
from django_otp.oath import TOTP

from gladminds.settings import TOTP_SECRET_KEY, OTP_VALIDITY
from gladminds.core.base_models import STATUS_CHOICES
from gladminds.bajaj import models
from gladminds.core.cron_jobs.taskqueue import SqsTaskQueue
from gladminds.core.managers.mail import send_ucn_request_alert
from django.db.models.fields.files import FieldFile
from gladminds.core.constants import FEEDBACK_STATUS, PRIORITY, FEEDBACK_TYPE,\
    TIME_FORMAT
from gladminds.core.base_models import STATUS_CHOICES
from gladminds.core.cron_jobs.taskqueue import SqsTaskQueue
from gladminds.core.managers.mail import send_ucn_request_alert, send_mail_when_vin_does_not_exist


COUPON_STATUS = dict((v, k) for k, v in dict(STATUS_CHOICES).items())
logger = logging.getLogger('gladminds')


def generate_unique_customer_id():
    bytes_str = os.urandom(24)
    unique_str = hashlib.md5(bytes_str).hexdigest()[:10]
    return unique_str.upper()

def import_json():
    try:
        import simplejson as json
    except ImportError:
        try:
            import json
        except ImportError:
            try:
                from django.utils import simplejson as json
            except:
                raise ImportError("Requires either simplejson, Python 2.6 or django.utils!")
    return json


def mobile_format(phone_number):
    '''
        GM store numbers in +91 format
        And when airtel pull message from customer
        or service advisor we will check that number in +91 format'''
    return '+91' + phone_number[-10:]


def format_message(message):
    '''
        This function removes extra spaces from message
    '''
    keywords = message.split(' ')
    return ' '.join([keyword for keyword in keywords if keyword])


def get_phone_number_format(phone_number):
    '''
        This is used when we are sending message through sms client
    '''
    return phone_number[-10:]


def save_otp(user, token, email):
    models.OTPToken.objects.filter(user=user).delete()
    token_obj = models.OTPToken(user=user, token=str(token), request_date=datetime.datetime.now(), email=email)
    token_obj.save()


def get_token(user, phone_number, email=''):
    if email and user.email_id != email:
        raise
    totp = TOTP(TOTP_SECRET_KEY+str(randint(10000, 99999))+str(phone_number))
    totp.time = 30
    token = totp.token()
    save_otp(user, token, email)
    return token


def validate_otp(user, otp, phone):
    token_obj = models.OTPToken.objects.filter(user=user)[0]
    if int(otp) == int(token_obj.token) and (timezone.now()-token_obj.request_date).seconds <= OTP_VALIDITY:
        return True
    elif (timezone.now()-token_obj.request_date).seconds > OTP_VALIDITY:
        token_obj.delete()
    raise

def update_pass(otp, password):
    token_obj = models.OTPToken.objects.filter(token=otp)[0]
    user = token_obj.user
    token_obj.delete()
    user.set_password(password)
    user.save()
    return True

def get_task_queue():
    queue_name = settings.SQS_QUEUE_NAME
    return SqsTaskQueue(queue_name)


def format_product_object(product_obj):
    purchase_date = product_obj.purchase_date.strftime('%d/%m/%Y')
    return {'id': product_obj.customer_id,
            'phone': get_phone_number_format(str(product_obj.customer_details.phone_number)), 
            'name': product_obj.customer_details.user.first_name, 
            'purchase_date': purchase_date,
            'vin': product_obj.product_id}

def get_customer_info(data):
    try:
        product_obj = models.ProductData.objects.select_related('customer_details__user').get(product_id=data['vin'])
    except Exception as ex:
        logger.info(ex)
        message = '''VIN '{0}' does not exist in our records. Please contact customer support: +91-9741775128.'''.format(data['vin'])
        if data['groups'][0] == "dealers":
            data['groups'][0] = "Dealer"
        else:
            data['groups'][0] = "ASC"
        template = get_email_template('VIN DOES NOT EXIST')['body'].format(data['current_user'], data['vin'], data['groups'][0])
        send_mail_when_vin_does_not_exist(data=template)
        return {'message': message, 'status': 'fail'}
    if product_obj.purchase_date:
        product_data = format_product_object(product_obj)
        return product_data
    else:
        message = '''VIN '{0}' has no associated customer. Please register the customer.'''.format(data['vin'])
        return {'message': message}

def get_sa_list(request):
    dealer = models.Dealer.objects.filter(dealer_id=request.user)[0]
    service_advisors = models.ServiceAdvisorDealerRelationship.objects\
                                .filter(dealer_id=dealer, status='Y')
    sa_phone_list = []
    for service_advisor in service_advisors:
        sa_phone_list.append(service_advisor.service_advisor_id)
    return sa_phone_list


def get_sa_list_for_login_dealer(user):
    dealer = aftersell_common.RegisteredDealer.objects.filter(
                dealer_id=user)[0]
    service_advisors = aftersell_common.ServiceAdvisorDealerRelationship.objects\
                                .filter(dealer_id=dealer, status='Y')
    return service_advisors

def get_asc_list_for_login_dealer(user):
    ascs = aftersell_common.RegisteredDealer.objects.filter(
                dependent_on=user)
    asc_list_with_detail = []
    for asc in ascs:
        asc_detail = User.objects.filter(username=asc.dealer_id)
        asc_list_with_detail.append(asc_detail[0])
    return asc_list_with_detail


def recover_coupon_info(data):
    customer_id = data['customerId']
    logger.info('UCN for customer {0} requested by User {1}'.format(customer_id, data['current_user']))
    coupon_data = get_coupon_info(data)
    if coupon_data:
        ucn_recovery_obj = upload_file(data, coupon_data.unique_service_coupon)
        send_recovery_email_to_admin(ucn_recovery_obj, coupon_data)
        message = 'UCN for customer {0} is {1}.'.format(customer_id,
                                                    coupon_data.unique_service_coupon)
        return {'status': True, 'message': message}
    else:
        message = 'No coupon in progress for customerID {0}.'.format(customer_id) 
        return {'status': False, 'message': message}
    
def get_coupon_info(data):
    customer_id = get_updated_customer_id(data['customerId'])
    try:
        coupon_data = common.CouponData.objects.get(vin__sap_customer_id=customer_id, status=4)
        coupon_data.special_case = True
        coupon_data.save()
    except Exception as ex:
        coupon_data = None
        logger.error('[UCN_RECOVERY_ERROR]:: {0}'.format(ex))
    return coupon_data

def upload_file(data, unique_service_coupon):
    user_obj = data['current_user']
    file_obj = data['job_card']
    customer_id = data['customerId']
    reason = data['reason']
    file_obj.name = get_file_name(data, file_obj)
    #TODO: Include Facility to get brand name here
    destination = settings.JOBCARD_DIR.format('bajaj')
    path = uploadFileToS3(destination=destination, file_obj=file_obj, 
                          bucket=settings.JOBCARD_BUCKET, logger_msg="JobCard")
    ucn_recovery_obj = aftersell_common.UCNRecovery(reason=reason, user=user_obj,
                                        sap_customer_id=customer_id, file_location=path,
                                        unique_service_coupon=unique_service_coupon)
    ucn_recovery_obj.save()
    return ucn_recovery_obj

def get_file_name(data, file_obj):
    requester = data['current_user']
    if 'dealers' in requester.groups.all():
        filename_prefix = requester
    else:
        #TODO: Implement dealerId in prefix when we have Dealer and ASC relationship
        filename_prefix = requester
    filename_suffix = str(uuid.uuid4())
    ext = file_obj.name.split('.')[-1]
    customer_id = data['customerId']
    return str(filename_prefix)+'_'+customer_id+'_'+filename_suffix+'.'+ext


def get_user_groups(user):
    groups = []
    for group in user.groups.all():
        groups.append(str(group.name))
    return groups

def stringify_groups(user):
    groups = []
    for group in user.groups.all():
        groups.append(str(group.name))
    return groups


def send_recovery_email_to_admin(file_obj, coupon_data):
    file_location = file_obj.file_location
    reason = file_obj.reason
    customer_id = file_obj.sap_customer_id
    requester = str(file_obj.user)
    data = get_email_template('UCN_REQUEST_ALERT').body.format(requester,coupon_data.service_type,
                customer_id, coupon_data.actual_kms, reason, file_location)
    send_ucn_request_alert(data=data)


def uploadFileToS3(awsid=settings.S3_ID, awskey=settings.S3_KEY, bucket=None,
                   destination='', file_obj=None, logger_msg=None, file_mimetype=None):
    '''
    The function uploads the file-object to S3 bucket.
    '''
    
    connection = boto.connect_s3(awsid, awskey)
    s3_bucket = connection.get_bucket(bucket)
    s3_key = Key(s3_bucket)
    if file_mimetype:
        s3_key.content_type = file_mimetype
        
    else:
        s3_key.content_type = mimetypes.guess_type(file_obj.name)[0]
    
    s3_key.key = destination+file_obj.name
    s3_key.set_contents_from_string(file_obj.read())
    s3_key.set_acl('public-read')
    path = s3_key.generate_url(expires_in=0, query_auth=False)
    logger.info('{1}: {0} has been uploaded'.format(s3_key.key, logger_msg))
    return path


def get_email_template(key):
    template_object = models.EmailTemplate.objects.filter(template_key=key).values()
    return template_object[0]


def format_date_string(date_string, date_format='%d/%m/%Y'):
    '''
    This function converts the date from string to datetime format
    '''
    date = datetime.datetime.strptime(date_string, date_format)
    return date


def get_dict_from_object(object):
    temp_dict = {}
    for key in object:
        if isinstance(object[key], datetime.datetime):
            temp_dict[key] = object[key].astimezone(tz.tzutc()).strftime('%Y-%m-%dT%H:%M:%S')
        elif isinstance(object[key], FieldFile):
            temp_dict[key] = None
        else:
            temp_dict[key] = object[key]
    return temp_dict

def get_list_from_set(set_data):
    created_list = []
    for set_object in set_data:
        created_list.append(list(set_object)[1])
    return created_list

def create_feed_data(post_data, product_data, temp_customer_id):
    data = {}
    data['sap_customer_id'] = temp_customer_id
    data['product_purchase_date'] = format_date_string(post_data['purchase-date'])
    data['customer_phone_number'] = mobile_format(post_data['customer-phone'])
    data['customer_name'] = post_data['customer-name']
    data['engine'] = product_data.engine
    data['veh_reg_no'] = product_data.veh_reg_no
    data['vin'] = product_data.product_id
    data['pin_no'] = data['state'] = data['city'] = None
    return data

def create_sa_feed_data(post_data, user_id, temp_sa_id):
    data ={}
    data['dealer_id'] = user_id
    data['phone_number'] = mobile_format(post_data['phone-number'])
    data['service_advisor_id'] = temp_sa_id
    data['name'] = post_data['name'].upper()
    data['status'] = post_data['status']
    data['address'] = None
    return data

def create_context(email_template_name, feedback_obj):
    data = get_email_template(email_template_name)
    data['newsubject'] = data['subject'].format(id = feedback_obj.id)
    data['content'] = data['body'].format(type = feedback_obj.type, reporter = feedback_obj.reporter, 
                                          message = feedback_obj.message, created_date = feedback_obj.created_date, 
                                          assign_to = feedback_obj.assign_to,  priority =  feedback_obj.priority, remark = "",
                                          root_cause = feedback_obj.root_cause, resolution = feedback_obj.resolution, due_date = "")

    return data

def subtract_dates(start_date, end_date): 
    start_date = start_date.strftime("%Y-%m-%d")
    end_date = end_date.strftime("%Y-%m-%d")
    start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d") 
    return start_date - end_date

def search_details(data):
    kwargs = {}
    search_results = []
    if data.has_key('VIN'):
        kwargs[ 'product_id' ] = data['VIN']
    elif data.has_key('Customer-ID'):
        kwargs[ 'customer_id' ] = get_updated_customer_id(data['Customer-ID'])
    elif data.has_key('Customer-Mobile'):
        kwargs[ 'customer_details__phone_number' ] = mobile_format(data['Customer-Mobile'])
    product_obj = models.ProductData.objects.filter(**kwargs)
    if not product_obj or not product_obj[0].purchase_date:
        key = data.keys()
        message = '''{0} '{1}' has no associated customer. Please register the customer.'''.format(key[0], data[key[0]])
        logger.info(message)
        return {'message': message}
    for product in product_obj:
        data = format_product_object(product)
        search_results.append(data)
    return search_results

def get_search_query_params(request, class_self):
    custom_search_enabled = False
    if 'custom_search' in request.GET and 'val' in request.GET:
        class_self.search_fields = ()
        request.GET = request.GET.copy()
        class_self.search_fields = (request.GET.pop("custom_search")[0],)
        search_value = request.GET.pop("val")[0]
        request.GET["q"] = search_value
        request.META['QUERY_STRING'] = 'q=%s'% search_value
        custom_search_enabled = True
    return custom_search_enabled

def get_start_and_end_date(start_date, end_date, format):

    start_date = start_date.strftime(format)
    start_date = datetime.datetime.strptime(start_date, format)
    end_date = end_date.strftime(format)
    end_date = datetime.datetime.strptime(end_date, format)
    return start_date,end_date

def get_min_and_max_filter_date():
    return (datetime.date.today() - datetime.timedelta(6*365/12)).isoformat(), (datetime.date.today()).isoformat()

#TODO Function needs to be refactored
def set_wait_time(feedback_data):
    start_date = feedback_data.pending_from
    end_date = datetime.datetime.now()
    start_date = start_date.strftime(TIME_FORMAT)
    end_date = end_date.strftime(TIME_FORMAT)
    start_date = datetime.datetime.strptime(start_date, TIME_FORMAT)
    end_date = datetime.datetime.strptime(end_date, TIME_FORMAT)
    wait = end_date - start_date
    wait_time = float(wait.days) + float(wait.seconds) / float(86400)
    previous_wait = feedback_data.wait_time
    models.Feedback.objects.filter(id = feedback_data.id).update(wait_time = wait_time+previous_wait)


def services_search_details(data):
    key = data.keys()
    message = '''No Service Details available for {0} '{1}'. Please register the customer.'''.format(key[0], data[key[0]])
    kwargs = {}
    response = {}
    search_results = []
    if data.has_key('VIN'):
        kwargs[ 'vin' ] = data['VIN']
    elif data.has_key('Customer-ID'):
        kwargs[ 'sap_customer_id' ] = get_updated_customer_id(data['Customer-ID'])
    product_obj = common.ProductData.objects.filter(**kwargs)
    if len(product_obj) == 1:
        if not product_obj[0].product_purchase_date:
            return {'message': message}
        try:
            coupon_obj = common.CouponData.objects.filter(vin=product_obj[0]).order_by('service_type')
            if len(coupon_obj) > 0:
                for coupon in coupon_obj:
                    temp = {}
                    temp['service_type'] = coupon.service_type
                    temp['status'] = STATUS_CHOICES[coupon.status - 1][1]
                    search_results.append(temp)
                response['search_results'] = search_results
                response['other_details'] = {'vin': product_obj[0].vin, 'customer_id': product_obj[0].sap_customer_id,\
                                             'customer_name': product_obj[0].customer_phone_number.customer_name}
                return response
            else:
                return {'message': message}
        except Exception as ex:
            logger.log(ex)
            return {'message': ex}
    else:
        return {'message': message}
    
def get_updated_customer_id(customer_id):
    if customer_id and customer_id.find('T') == 0:
        try:
            temp_customer_obj = common.CustomerTempRegistration.objects.select_related('product_data').\
                                       get(temp_customer_id=customer_id)
            customer_id = temp_customer_obj.product_data.sap_customer_id
        except Exception as ex:
            logger.info("Temporary ID {0} does not exists: {1}".format(customer_id, ex))
    return customer_id


def service_advisor_search(data):
    dealer_data = models.Dealer.objects.get(
                dealer_id=data['current_user'])
    phone_number = mobile_format(data['phone_number'])
    message = phone_number + ' is active under another dealer.' 
    sa_details = models.ServiceAdvisor.objects.filter(user__phone_number=phone_number, dealer=dealer_data)
    sa_mobile_active = models.ServiceAdvisor.objects.filter(
                                user__phone_number=phone_number,
                                status='Y').exclude(dealer=dealer_data)
    if not sa_details and not sa_mobile_active:
        message = 'Service advisor is not associated, Please register the service advisor.'
        return {'message': message}
    if sa_details:
        user_details = sa_details[0].user
        service_advisor_details = {'id': sa_details[0].service_advisor_id,
                                   'phone': data['phone_number'],
                                   'name':  user_details.user.first_name, 
                                   'status': sa_details[0].status,
                                   'active':len(sa_mobile_active),
                                   'message':message}
        return service_advisor_details
    return {'message': message, 'status': 'fail'}


def make_tls_property(default=None):
    """Creates a class-wide instance property with a thread-specific value."""
    class TLSProperty(object):
        def __init__(self):
            from threading import local
            self.local = local()

        def __get__(self, instance, cls):
            if not instance:
                return self
            return self.value

        def __set__(self, instance, value):
            self.value = value

        def _get_value(self):
            return getattr(self.local, 'value', default)
        def _set_value(self, value):
            self.local.value = value
        value = property(_get_value, _set_value)

    return TLSProperty()


def get_asc_data():
    asc_data = aftersell_common.RegisteredDealer.objects.filter(role='asc')
    asc_list = []
    for asc in asc_data:
        asc_detail = User.objects.get(username=asc.dealer_id)
        asc_list.append(asc_detail)
    return asc_list


def asc_cuopon_details(asc_id, status_type):
    cuopon_details = common.CouponData.objects.filter(servicing_dealer=asc_id, status=status_type)
    return len(cuopon_details)


def get_state_city(details, address):
    if address == None or address == '':
        details['state'] = 'Null'
        details['city'] = 'Null'
    else:
        addr = address.split(',')
        if len(addr) == 2:
            details['state'] = addr[1]
            details['city'] = addr[0]
        else:
            details['city'] = addr[0]
            details['state'] = 'Null'

    return details

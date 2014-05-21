import os, logging, time, hashlib, uuid, mimetypes
from datetime import datetime
from random import randint
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User
import boto
from boto.s3.key import Key
from gladminds.models.common import STATUS_CHOICES
from gladminds.models import common
from django_otp.oath import TOTP
from gladminds.settings import TOTP_SECRET_KEY, OTP_VALIDITY
from gladminds.taskqueue import SqsTaskQueue
from gladminds import message_template
from gladminds.mail import send_ucn_request_alert

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
        or service advisor we will check that number in +91 format 
    '''
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


def save_otp(token, phone_number, email):
    user = common.RegisteredASC.objects.filter(phone_number=mobile_format(phone_number))[0].user
    if email and user.email_id != email:
        raise
    common.OTPToken.objects.filter(user=user).delete()
    token_obj = common.OTPToken(user=user, token=str(token), request_date=datetime.now(), email=email)
    token_obj.save()

def get_token(phone_number, email=''):
    totp=TOTP(TOTP_SECRET_KEY+str(randint(10000,99999))+str(phone_number))
    totp.time=30
    token = totp.token()
    save_otp(token, phone_number, email)
    return token

def validate_otp(otp, phone):
    asc = common.RegisteredASC.objects.filter(phone_number=mobile_format(phone))[0].user
    token_obj = common.OTPToken.objects.filter(user=asc)[0]
    if int(otp) == int(token_obj.token) and (timezone.now()-token_obj.request_date).seconds <= OTP_VALIDITY:
        return True
    elif (timezone.now()-token_obj.request_date).seconds > OTP_VALIDITY:
        token_obj.delete()
    raise

def update_pass(otp, password):
    token_obj = common.OTPToken.objects.filter(token=otp)[0]
    user = token_obj.user
    token_obj.delete()
    user.set_password(password)
    user.save()
    return True


def get_task_queue():
    queue_name = settings.SQS_QUEUE_NAME
    return SqsTaskQueue(queue_name)

def get_customer_info(data):
    data=data.POST
    try:
        product_obj = common.ProductData.objects.get(vin=data['vin'])
    except Exception as ex:
        logger.info(ex)
        message = '''VIN '{0}' does not exist in our records'''.format(data['vin'])
        return {'message': message}
    purchase_date = product_obj.product_purchase_date.strftime('%d/%m/%Y')
    return {'customer_phone': get_phone_number_format(str(product_obj.customer_phone_number)), 'customer_name': product_obj.customer_phone_number.customer_name, 'purchase_date': purchase_date}

def get_sa_list(request):
    dealer = common.RegisteredDealer.objects.filter(
                dealer_id=request.user)[0]
    service_advisors = common.ServiceAdvisorDealerRelationship.objects\
                                .filter(dealer_id=dealer, status='Y')
    sa_phone_list = []
    for service_advisor in service_advisors:
        sa_phone_list.append(service_advisor.service_advisor_id)
    return sa_phone_list

def recover_coupon_info(request):
    coupon_info = get_coupon_info(request)
    upload_file(request)
    return coupon_info
    
def get_coupon_info(request):
    data=request.POST
    customer_id = data['customerId']
    logger.info('UCN for customer {0} requested by User {1}'.format(customer_id, request.user))
    product_data = common.ProductData.objects.filter(sap_customer_id=customer_id)[0]
    coupon_data = common.CouponData.objects.filter(vin=product_data, status=4)[0]
    message = 'UCN for customer {0} is {1}.'.format(product_data.sap_customer_id, coupon_data.unique_service_coupon)
    return {'status': True, 'message': message}

def upload_file(request):
    data = request.POST
    user_obj = request.user
    file_obj = request.FILES['jobCard']
    customer_id = data['customerId']
    reason = data['reason']
    customer_id = request.POST['customerId']
    file_obj.name = get_file_name(request, file_obj)
    #TODO: Include Facility to get brand name here
    destination = settings.JOBCARD_DIR.format('bajaj')
    path = uploadFileToS3(destination=destination, file_obj=file_obj)
    ucn_recovery_obj = common.UCNRecovery(reason=reason, user=user_obj, sap_customer_id=customer_id, file_location=path)
    ucn_recovery_obj.save()
    send_recovery_email_to_admin(ucn_recovery_obj)

def get_file_name(request, file_obj):
    requester = request.user
    if 'dealers' in requester.groups.all():
        filename_prefix = requester
    else:
        #TODO: Implement dealerId in prefix when we have Dealer and ASC relationship
        filename_prefix = requester
    filename_suffix = str(uuid.uuid4())
    ext = file_obj.name.split('.')[-1]
    customer_id = request.POST['customerId']
    return str(filename_prefix)+'_'+customer_id+'_'+filename_suffix+'.'+ext
    
def stringify_groups(user):
    groups = []
    for group in user.groups.all():
        groups.append(str(group.name))
    return groups

def send_recovery_email_to_admin(file_obj):
    file_location = file_obj.file_location
    reason = file_obj.reason
    customer_id = file_obj.sap_customer_id
    requester = str(file_obj.user)
    data = get_email_template('UCN_REQUEST_ALERT').body.format(requester, customer_id, reason, file_location)
    send_ucn_request_alert(data=data)

def uploadFileToS3(awsid=settings.S3_ID, awskey=settings.S3_KEY, bucket=settings.JOBCARD_BUCKET,
                   destination='', file_obj=None):
    '''
    The function uploads the file-object to S3 bucket.
    '''
    connection = boto.connect_s3(awsid, awskey)
    s3_bucket = connection.get_bucket(bucket)
    s3_key = Key(s3_bucket)
    s3_key.content_type = mimetypes.guess_type(file_obj.name)[0]
    s3_key.key = destination+file_obj.name
    s3_key.set_contents_from_string(file_obj.read())
    s3_key.set_acl('public-read')
    path = s3_key.generate_url(expires_in=0, query_auth=False)
    logger.info('Jobcard: {0} has been uploaded'.format(s3_key.key))
    return path
    
def get_email_template(key):
    template_object = common.EmailTemplate.objects.get(template_key = key)
    return template_object

def format_date_string(date_string):
    '''
    This function converts the date from string to datetime format
    '''
    date = datetime.fromtimestamp(time.mktime(time.strptime(date_string, "%d/%m/%Y")))
    return date
    
import os, logging
from datetime import datetime
from gladminds.models.common import STATUS_CHOICES
from gladminds.models import common
from django_otp.oath import TOTP
from gladminds.settings import TOTP_SECRET_KEY, OTP_VALIDITY
from random import randint

import hashlib
from django.utils import timezone

from gladminds.taskqueue import SqsTaskQueue
from gladminds import message_template
import boto
from boto.s3.key import Key
from django.conf import settings
import mimetypes
from gladminds.mail import send_ucn_request_alert
from django.contrib.auth.models import User
from django.http.response import HttpResponse
import json

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
    if otp == token_obj.token and (timezone.now()-token_obj.request_date).seconds <= OTP_VALIDITY:
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
    queue_name = "gladminds-prod"
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
    send_email_to_admin(request)
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
    file_obj = request.FILES['jobCard']
    customer_id = request.POST['customerId']
    ext = file_obj.name.split('.')[-1]
    file_obj.name = str(datetime.now().date())+customer_id+'.'+ext
    destination = settings.JOBCARD_DIR
    uploadFileToS3(destination=destination, file_obj=file_obj)

def send_email_to_admin(request):
    data = request.POST
    file_obj = request.FILES['jobCard']
    customer_id = data['customerId']
    reason = data['reason']
    user = str(request.user)
    ext = file_obj.name.split('.')[-1]
    user_obj = User.objects.filter(username=user)[0]
    filename = settings.JOBCARD_DIR+str(datetime.now().date())+customer_id+'.'+ext
    data = get_email_template('UCN_REQUEST_ALERT').body.format(request.user, customer_id, reason, filename)
    ucn_recovery_obj = common.UCNRecovery(reason=reason, user=user_obj, sap_customer_id=customer_id, file_location=filename)
    ucn_recovery_obj.save()
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
    logger.info('Jobcard: {0} has been uploaded'.format(s3_key.key))
    
def get_email_template(key):
    template_object = common.EmailTemplate.objects.get(template_key = key)
    return template_object

def format_return_message(data):
    return HttpResponse(json.dumps({"status": data}), content_type="application/json")
    
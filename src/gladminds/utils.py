import os
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

COUPON_STATUS = dict((v, k) for k, v in dict(STATUS_CHOICES).items())


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
    product_obj = common.ProductData.objects.filter(vin=data['vin'])[0]
    return {'customer_phone': str(product_obj.customer_phone_number), 'customer_id': product_obj.sap_customer_id}

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
    product_data = common.ProductData.objects.filter(sap_customer_id=customer_id)
    coupon_data = common.CouponData.objects.filter(vin=product_data, status=4)[0]
    message = message_template.get_template('SEND_CUSTOMER_VALID_COUPON').format(coupon=coupon_data.unique_service_coupon, service_type=coupon_data.service_type)
    return {'status': True, 'message': message}

def upload_file(request):
    file_obj = request.FILES['jobCard']
    destination = settings.JOBCARD_DIR
    uploadFileToS3(destination=destination, file_obj=file_obj)
    
def uploadFileToS3(awsid=settings.S3_ID, awskey=settings.S3_KEY, bucket=settings.JOBCARD_BUCKET,
                   destination=None, file_obj=None):
    '''
    The function uploads the file-object to S3 bucket.
    '''
    connection = boto.connect_s3(awsid, awskey)
    s3_bucket = connection.get_bucket(bucket)
    s3_key = Key(s3_bucket)
    s3_key.content_type = mimetypes.guess_type(file_obj.name)[0]
    s3_key.key = file_obj.name
    s3_key.set_contents_from_string(file_obj.read())
    
    
    
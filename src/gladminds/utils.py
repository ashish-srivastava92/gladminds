import os
import hashlib
from tastypie.serializers import Serializer
from datetime import datetime
from gladminds.models.common import STATUS_CHOICES
from gladminds.models import common
from django_otp.oath import TOTP
from gladminds.settings import TOTP_SECRET_KEY
from random import randint
from gladminds import message_template
import hashlib

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
    m=hashlib.md5()
    m.update(str(token))
    user = common.GladMindUsers.objects.filter(phone_number=phone_number)
    token_obj = common.OTPToken(phone_number=user, token=m.digest(), request_date=datetime.now(), email=email)
    token_obj.save()

def get_token(phone_number, email=''):
    totp=TOTP(TOTP_SECRET_KEY+str(randint(10000,99999))+str(phone_number))
    totp.time=30
    token = totp.token()
    message = message_template.get_template('SEND_OTP').format(token)
    save_otp(token, phone_number, email)
    return token


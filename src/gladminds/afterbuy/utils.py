from datetime import datetime
from random import randint
from django.utils import timezone
from gladminds.afterbuy import models as common
from gladminds.afterbuy import models as afterbuy_model
from gladminds.core import base_models as common
from django_otp.oath import TOTP
from gladminds.settings import TOTP_SECRET_KEY, OTP_VALIDITY
from django.contrib.auth.models import User

def save_otp(user, token):
    afterbuy_model.OTPToken.objects.filter(user=user).delete()
    token_obj = afterbuy_model.OTPToken(user=user, token=str(token), request_date=datetime.now(), email=user.user.email)
    token_obj.save()

def get_token(user, phone_number):
    totp=TOTP(TOTP_SECRET_KEY+str(randint(10000,99999))+str(phone_number))
    totp.time=30
    token = totp.token()
    save_otp(user, token)
    return token

def validate_otp(user, otp, phone):
    token_obj = common.OTPToken.objects.filter(user=user)[0]
    if int(otp) == int(token_obj.token) and (timezone.now()-token_obj.request_date).seconds <= OTP_VALIDITY:
        return True
    elif (timezone.now()-token_obj.request_date).seconds > OTP_VALIDITY:
        token_obj.delete()
    raise

def set_user_password(**kwargs):
    if kwargs.get('phone_number'):
        user = User.objects.get(phone_number=kwargs['phone_number'])
    elif kwargs.get('email'):
        user = User.objects.get(email=kwargs['email'])
    user.set_password(kwargs['password'])
    data = {'status': 1, 'message': "password updated successfully"}
    return data

def get_token_by_phone_or_email(**kwargs):
    user = afterbuy_model.Consumer.objects.filter(**kwargs)[0]
    token = get_token(user, user.phone_number)
    return token
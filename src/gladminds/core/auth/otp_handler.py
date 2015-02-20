from datetime import datetime
from django_otp.oath import TOTP
from gladminds.settings import TOTP_SECRET_KEY, OTP_VALIDITY
from random import randint
from django.utils import timezone
from gladminds.core.exceptions import OtpFailedException
from gladminds.core.loaders.module_loader import get_model
from django.template.base import kwarg_re


def save_otp(token, **kwargs):
    OTPToken = get_model('OTPToken')
    if 'user' in kwargs.keys():
        user = get_model('UserProfile').objects.get(user = kwargs.get('user'))
        OTPToken.objects.filter(user=user).delete()
        token_obj = OTPToken(user=user, token=str(token), request_date=datetime.now(), email=user.user.email)
    else:
        phone_number = kwargs.get('phone_number')
        OTPToken.objects.filter(phone_number=phone_number).delete()
        token_obj = OTPToken(token=str(token), request_date=datetime.now(), phone_number=phone_number)
    token_obj.save()


def generate_otp(phone_number):
    totp = TOTP(TOTP_SECRET_KEY+str(randint(10000,99999))+str(phone_number))
    totp.time = 30
    token = totp.token()
    return token


def validate_otp(otp, **kwargs):
    OTPToken = get_model('OTPToken')
    if 'user' in kwargs.keys():
        token_obj = OTPToken.objects.filter(user = kwargs.get('user'))[0]
    else:
        phone_number = kwargs.get('phone_number')
        token_obj = OTPToken.objects.get(phone_number=phone_number)

    if int(otp) == int(token_obj.token) and (timezone.now()-token_obj.request_date).seconds <= OTP_VALIDITY:
        return True
    elif (timezone.now()-token_obj.request_date).seconds > OTP_VALIDITY:
        token_obj.delete()
    raise OtpFailedException("Not an valid otp")


def get_otp(**kwargs):
    if 'user' in kwargs.keys():
        phone_number = get_model('UserProfile').objects.get(user = kwargs.get('user')).phone_number
    else:
        phone_number = kwargs.get('phone_number')
    otp = generate_otp(phone_number)
    save_otp(otp, **kwargs)
    return otp


'''
Helper class which contains custom input fields
'''
import re

from django.utils.translation import gettext as _
from django.db import models
from django.core.validators import RegexValidator
from django.forms.widgets import TextInput
from django.forms import fields
from django.core.exceptions import ValidationError
from django.conf import settings


phone_re = re.compile(r'^\+?1?\d{9,15}$')
validate_phone = RegexValidator(phone_re, _("Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."), 'invalid')


def get_phone_number_format(phone_number):
    '''
    This is used to format phone
    '''
    phone_number = phone_number.strip()
    if phone_number.startswith('+91'):
        phone_number = phone_number[3:]
    numbers = re.compile('\d+(?:\d+)?')
    return '+91' + ''.join(numbers.findall(phone_number))


class PhoneInput(TextInput):
    input_type = 'phone'


class PhoneNoField(fields.CharField):
    widget = PhoneInput
    default_validators = [validate_phone]

    def clean(self, value):
        value = self.to_python(value).strip()
        value = get_phone_number_format(value)
        return super(PhoneNoField, self).clean(value)


class PhoneField(models.CharField):
    default_validators = [validate_phone]
    description = _("Phone Field")

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = kwargs.get('max_length', 15)
        models.CharField.__init__(self, *args, **kwargs)

    def formfield(self, **kwargs):
        # As with CharField, this will cause email validation to be performed
        # twice.
        defaults = {
            'form_class': PhoneNoField,
        }
        defaults.update(kwargs)
        return super(PhoneField, self).formfield(**defaults)


def validate_image(fieldfile_obj):
        filesize = fieldfile_obj.file.size
        megabyte_limit = settings.MAX_UPLOAD_IMAGE_SIZE
        if filesize > megabyte_limit*1024*1024:
            raise ValidationError("Image size cannot exceed %sMB" % str(megabyte_limit))

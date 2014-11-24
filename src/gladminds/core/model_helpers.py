'''
Helper class which contains custom input fields
'''
import re

from django.utils.translation import gettext as _
from django.db import models
from django.core.validators import RegexValidator
from django.forms.widgets import TextInput
from django.forms import fields


phone_re = re.compile(r'^\+?1?\d{9,15}$')
validate_phone = RegexValidator(phone_re, _("Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."), 'invalid')


class PhoneInput(TextInput):
    input_type = 'phone'


class PhoneNoField(fields.CharField):
    widget = PhoneInput
    default_validators = [validate_phone]

    def clean(self, value):
        value = self.to_python(value).strip()
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

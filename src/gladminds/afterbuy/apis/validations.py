from datetime import datetime

from tastypie.validation import Validation
from gladminds.core.auth_helper import AFTERBUY_ADMIN_GROUPS
from gladminds.afterbuy.utils import get_date_from_string

try:
    from django.utils.timezone import now as datetime_now
except ImportError:
    datetime_now = datetime.now

from django.forms.util import from_current_timezone


class ConsumerValidation(Validation):
    def is_valid(self, bundle, request=None):
        if not bundle.data:
            return {'__all__': 'Data should be present'}

        errors = {}

        for key, value in bundle.data.items():
            if 'phone_number' in key:
                errors[key] = ['You cannot update phone number']
            if 'is_email_verified' in key \
            and not request.user.groups.filter(name__in=AFTERBUY_ADMIN_GROUPS).exists():
                errors[key] = ['You cannot update is_email_verified ..only admin can']

        return errors


class UserValidation(Validation):
    def is_valid(self, bundle, request=None):
        if not bundle.data:
            return {'__all__': 'Data should be present'}

        errors = {}

        for key, value in bundle.data.items():
            if 'email' in key:
                errors['email'] = ['You cannot update email.']

        return errors


class ProductValidation(Validation):
    def is_valid(self, bundle, request=None):
        if not bundle.data:
            return {'__all__': 'Data should be present'}

        errors = {}
        for key, value in bundle.data.items():
            if 'purchase_date' in key and datetime_now() < from_current_timezone(get_date_from_string(value)):
                errors['purchase_date'] = ['Purchase date cannot be more than current date']

        return errors

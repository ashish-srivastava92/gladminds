import datetime
import hashlib
import random
import re

from django.db import models
from django.core.mail import send_mail

try:
    from django.utils.timezone import now as datetime_now
except ImportError:
    datetime_now = datetime.datetime.now


SHA1_RE = re.compile('^[a-f0-9]{40}$')


class EmailTokenManager(models.Manager):
    """
    Custom manager for the ``RegistrationProfile`` model.
    The methods defined here provide shortcuts for account creation
    and activation (including generation and emailing of activation
    keys), and for cleaning out expired inactive accounts.
    """
    def activate_user(self, activation_key):
        """
        Validate an activation key and activate the corresponding
        ``User`` if valid.
        If the key is valid and has not expired, return the ``User``
        after activating.
        If the key is not valid or has expired, return ``False``.
        If the key is valid but the ``User`` is already active,
        return ``False``.
        To prevent reactivation of an account which has been
        deactivated by site administrators, the activation key is
        reset to the string constant ``RegistrationProfile.ACTIVATED``
        after successful activation.
        """
        # Make sure the key we're trying conforms to the pattern of a
        # SHA1 hash; if it doesn't, no point trying to look it up in
        # the database.
        if SHA1_RE.search(activation_key):
            try:
                profile = self.get(activation_key=activation_key)
                print profile
            except self.model.DoesNotExist:
                return False
            if not profile.activation_key_expired():
                user_profile = profile.user
                user_profile.is_email_verified = True
                user_profile.save()
                profile.activation_key = self.model.ACTIVATED
                profile.save()
                return user_profile
        return False

    def create_email_token(self, user_profile, reciever_email ,site,send_email=True):
        salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
        username = user_profile.user.username
        if isinstance(username, unicode):
            username = username.encode('utf-8')
        activation_key = hashlib.sha1(salt+username).hexdigest()
        email_token = self.create(user=user_profile,
                           activation_key=activation_key)

        if send_email:
            print "mail"
            email_token.send_activation_email(reciever_email,site)

        return email_token


    def delete_expired_users(self):
        """
        Remove expired instances of ``RegistrationProfile`` and their
        associated ``User``s.
        Accounts to be deleted are identified by searching for
        instances of ``RegistrationProfile`` with expired activation
        keys, and then checking to see if their associated ``User``
        instances have the field ``is_active`` set to ``False``; any
        ``User`` who is both inactive and has an expired activation
        key will be deleted.
        
        It is recommended that this method be executed regularly as
        part of your routine site maintenance; this application
        provides a custom management command which will call this
        method, accessible as ``manage.py cleanupregistration``.
        
        Regularly clearing out accounts which have never been
        activated serves two useful purposes:
        
        1. It alleviates the ocasional need to reset a
           ``RegistrationProfile`` and/or re-send an activation email
           when a user does not receive or does not act upon the
           initial activation email; since the account will be
           deleted, the user will be able to simply re-register and
           receive a new activation key.
        
        2. It prevents the possibility of a malicious user registering
           one or more accounts and never activating them (thus
           denying the use of those usernames to anyone else); since
           those accounts will be deleted, the usernames will become
           available for use again.
        
        If you have a troublesome ``User`` and wish to disable their
        account while keeping it in the database, simply delete the
        associated ``RegistrationProfile``; an inactive ``User`` which
        does not have an associated ``RegistrationProfile`` will not
        be deleted.
        
        """
        pass
#         for profile in self.all():
#             try:
#                 if profile.activation_key_expired():
#                     user_profile = profile.user
#                     if not user_profile.is_email_verified:
#                         user_profile.delete()
#                         profile.delete()
#             except User.DoesNotExist:
#                 profile.delete()
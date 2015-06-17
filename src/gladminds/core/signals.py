from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch.dispatcher import receiver
from gladminds.core.auth_helper import add_user_to_group, GmApps, Roles


@receiver(post_save, sender=User)
def add_group(sender, **kwargs):
    app = kwargs['using']
    user = kwargs['instance']
    is_created = kwargs['created']
    if is_created and app in [GmApps.AFTERBUY]:
        add_user_to_group(app, user.id, Roles.USERS)

from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group
from django.dispatch.dispatcher import receiver


@receiver(post_save, sender=User)
def add_group(sender, **kwargs):
    app = kwargs['using']
    user = kwargs['instance']
    print user.groups.all()
    is_created = kwargs['created']
    if is_created and app in ['afterbuy']:
        g = Group.objects.using(app).get(name='USERS')
        if not user.groups.filter(name='USERS').exists():
            user.groups.add(g)
            user.save(using=app)

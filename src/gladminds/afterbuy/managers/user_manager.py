from django.db import models

class ConsumerManager(models.Manager):
    def get_active_consumers_with_phone(self, phone_number):
        return super(ConsumerManager, self).get_queryset().get(phone_number=phone_number,
                                                               user__is_active=True)
        
    def get_active_consumers_with_email(self, email):
        return super(ConsumerManager, self).select_related('user').get(user__email=email,
                                                               user__is_active=True)
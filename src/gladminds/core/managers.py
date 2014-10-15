from django.db import models


class RegisteredDealerManager(models.Manager):
    def active(self):
        result_list = []
        return result_list
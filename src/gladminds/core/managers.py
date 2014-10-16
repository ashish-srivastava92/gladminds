from django.db import models


class DealerManager(models.Manager):
    def active(self):
        result_list = []
        return result_list
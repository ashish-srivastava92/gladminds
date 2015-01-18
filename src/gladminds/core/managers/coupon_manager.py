from django.db import models


class CouponDataManager(models.Manager):
    def expired_count(self):
        return super(CouponDataManager, self).get_query_set().filter(status=3).count()

    def inprogress_count(self):
        return super(CouponDataManager, self).get_query_set().filter(status=4).count()

    def closed_count(self):
        return super(CouponDataManager, self).get_query_set().filter(status=2).count()

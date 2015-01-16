from django.db import models


class FeedbackManager(models.Manager):
    def raised_count(self):
        return super(FeedbackManager, self).get_query_set().all().count()

    def inprogress_count(self):
        return super(FeedbackManager, self).get_query_set().filter(status="In Progress").count()

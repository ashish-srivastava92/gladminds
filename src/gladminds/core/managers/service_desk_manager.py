from django.db import models


class FeedbackManager(models.Manager):
    def raised_count(self):
        return super(FeedbackManager, self).get_query_set().all().count()

    def inprogress_count(self):
        return super(FeedbackManager, self).get_query_set().filter(status="In Progress").count()
    
    def open_count(self):
        return super(FeedbackManager, self).get_query_set().filter(status="Open").count()
    
    def pending_count(self):
        return super(FeedbackManager, self).get_query_set().filter(status="Pending").count()
    
    def resolved_count(self):
        return super(FeedbackManager, self).get_query_set().filter(status="Resolved").count()
    
    def closed_count(self):
        return super(FeedbackManager, self).get_query_set().filter(status="Closed").count()
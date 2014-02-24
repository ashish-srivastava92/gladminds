from django.db import models
from datetime import datetime

class AuditLog(models.Model):
    date=models.DateTimeField()
    action=models.CharField(max_length=250)
    message=models.CharField(max_length=250)
    sender =models.CharField(max_length=250)
    reciever=models.CharField(max_length=250)
    status=models.CharField(max_length=250)
    class Meta:
        app_label="gladminds"

class DataFeedLog(models.Model):
    data_feed_id = models.AutoField(primary_key=True)
    feed_type = models.CharField(max_length=50, null=False)
    total_data_count = models.IntegerField(null=False)
    failed_data_count = models.IntegerField(null=False)
    success_data_count = models.IntegerField(null=False)
    action = models.CharField(max_length=50, null=False)
    status = models.BooleanField(null=False)
    timestamp = models.DateTimeField(default=datetime.now())
    class Meta:
        app_label="gladminds"
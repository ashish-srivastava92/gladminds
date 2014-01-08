from django.db import models

class AuditLog(models.Model):
    date=models.DateTimeField()
    action=models.CharField(max_length=250)
    message=models.CharField(max_length=250)
    sender =models.CharField(max_length=250)
    reciever=models.CharField(max_length=250)
    status=models.CharField(max_length=250)
    class Meta:
        app_label="gladminds"
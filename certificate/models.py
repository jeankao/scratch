# -*- coding: UTF-8 -*-
from django.db import models

from django.contrib.auth.models import User
from django.utils import timezone

def upload_path_handler(instance, filename):
    return "static/certificate/0/user_{id}/{filename}".format(id=instance.student_id, filename=filename)

# Hour of code證書
class Certificate(models.Model):
    picture = models.ImageField(upload_to = upload_path_handler, default = '/static/certificate/null.jpg')
    student_id= models.IntegerField(default=0)
    publish = models.DateTimeField(default=timezone.now)
    
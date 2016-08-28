# -*- coding: UTF-8 -*-
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

def upload_path_handler(instance, filename):
    return "static/show/{id}/{filename}".format(id=instance.id, filename=filename)


# 分組作品
class ShowGroup(models.Model):
    name = models.CharField(max_length=30)
    classroom_id = models.IntegerField(default=0)
	
    title = models.CharField(max_length=250)
    number = models.CharField(max_length=30)    
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    picture = models.ImageField(upload_to = upload_path_handler, default = '/static/show/null.jpg')
    done = models.BooleanField(default=False)
    open =  models.BooleanField(default=False)

# 評分
class ShowReview(models.Model):
    show_id = models.IntegerField(default=0)
    student_id = models.IntegerField(default=0)
    score1 = models.IntegerField(default=0)
    score2 = models.IntegerField(default=0)
    score3 = models.IntegerField(default=0)
    comment = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    done = models.BooleanField(default=False)	
	
    @property        
    def student(self):
        return User.objects.get(id=self.student_id)      
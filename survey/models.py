# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

# Pre-test survey
class PreSurvey(models.Model):
  ''' student_id: 學生id '''
  student_id = models.IntegerField(default=0)
  ''' 前測問卷填寫時間 '''
  fill_time = models.DateTimeField(auto_now_add=True)
  p = models.IntegerField(default=0)
  p_t = models.TextField()
  p1 = models.IntegerField(default=0)
  p2 = models.IntegerField(default=0)
  p3 = models.IntegerField(default=0)
  p4 = models.IntegerField(default=0)
  p5 = models.IntegerField(default=0)
  p6 = models.IntegerField(default=0)
  p7 = models.IntegerField(default=0)
  p8 = models.IntegerField(default=0)
  p9 = models.IntegerField(default=0)
  p10 = models.IntegerField(default=0)
	
  @property
  def student(self):
    return User.objects.get(id=self.student_id)         

class PostSurvey(models.Model):
  ''' 學生 ID '''
  student_id = models.IntegerField(default=0)
  ''' 後測問卷填寫時間 '''
  fill_time = models.DateTimeField(auto_now_add=True)
  ''' 第壹大題前 25 題回答 '''
  p1 = models.IntegerField(default=0)
  p2 = models.IntegerField(default=0)
  p3 = models.IntegerField(default=0)
  p4 = models.IntegerField(default=0)
  p5 = models.IntegerField(default=0)	
  p6 = models.IntegerField(default=0)
  p7 = models.IntegerField(default=0)
  p8 = models.IntegerField(default=0)
  p9 = models.IntegerField(default=0)
  p10 = models.IntegerField(default=0)	
  p11 = models.IntegerField(default=0)
  p12 = models.IntegerField(default=0)
  p13 = models.IntegerField(default=0)
  p14 = models.IntegerField(default=0)
  p15 = models.IntegerField(default=0)	
  p16 = models.IntegerField(default=0)
  p17 = models.IntegerField(default=0)
  p18 = models.IntegerField(default=0)
  p19 = models.IntegerField(default=0)
  p20 = models.IntegerField(default=0)	
  p21 = models.IntegerField(default=0)
  p22 = models.IntegerField(default=0)
  p23 = models.IntegerField(default=0)
  p24 = models.IntegerField(default=0)
  p25 = models.IntegerField(default=0)		
  ''' 第貳大題第1題，覺得最棒的3件事 '''
  p2_1 = models.TextField()
  ''' 第貳大題第2題，覺得最困難的3件事 '''
  p2_2 = models.TextField()
  ''' 第貳大題第3題，學習經驗 '''
  p2_3 = models.TextField()
	
  @property
  def student(self):
    return User.objects.get(id=self.student_id)         
	
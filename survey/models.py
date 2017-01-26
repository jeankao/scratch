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
	'''p1 = 回答|學過的語言
		例：
			0|
			1|C++,PHP,Javascript
	'''
	p1 = models.CharField(max_length=128)
	''' p2，每題一個字元
		4=非常同意,3=同意,2=不同意,1=非常不同意,0=無作答
	'''
	p2 = models.CharField(max_length=10)

	@property
	def student(self):
		return User.objects.get(id=self.student_id)         

class PostSurvey(models.Model):
	''' 學生 ID '''
	student_id = models.IntegerField(default=0)
	''' 後測問卷填寫時間 '''
	fill_time = models.DateTimeField(auto_now_add=True)
	''' 第壹大題前 25 題回答 '''
	p1 = models.CharField(max_length=25)
	''' 第貳大題第1題，覺得最棒的3件事 '''
	p2_1 = models.TextField
	''' 第貳大題第2題，覺得最困難的3件事 '''
	p2_2 = models.TextField
	''' 第貳大題第3題，學習經驗 '''
	p2_3 = models.TextField
	
	@property
	def student(self):
		return User.objects.get(id=self.student_id)         
	
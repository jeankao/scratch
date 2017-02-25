# -*- coding: UTF-8 -*-
from django.db import models
from django.contrib.auth.models import User
from teacher.models import Classroom
from django.utils import timezone

# 學生選課資料
class Enroll(models.Model):
    # 學生序號
    student_id = models.IntegerField(default=0)
    # 班級序號
    classroom_id = models.IntegerField(default=0)
    # 座號
    seat = models.IntegerField(default=0)
    # 組別
    group = models.IntegerField(default=0)
    # 創意秀組別
    group_show = models.IntegerField(default=0)
    # 12堂課證書
    certificate1 = models.BooleanField(default=False)
    certificate1_date = models.DateTimeField(default=timezone.now)
    # 實戰入門證書
    certificate2 = models.BooleanField(default=False) 
    certificate2_date = models.DateTimeField(default=timezone.now)	
    # 實戰進擊證書
    certificate3 = models.BooleanField(default=False)
    certificate3_date = models.DateTimeField(default=timezone.now)
    # 實戰高手證書
    certificate4 = models.BooleanField(default=False)
    certificate4_date = models.DateTimeField(default=timezone.now)
    # 12堂課 成績
    score_memo1 = models.IntegerField(default=0)
    # 實戰入門成績
    score_memo2 = models.IntegerField(default=0)
    # 實戰進擊成績
    score_memo3 = models.IntegerField(default=0)
    # 實戰高手成績
    score_memo4 = models.IntegerField(default=0)
	
    @property
    def classroom(self):
        return Classroom.objects.get(id=self.classroom_id)  

    @property        
    def student(self):
        return User.objects.get(id=self.student_id)      

    def __str__(self):
        return str(self.id)    

    class Meta:
        unique_together = ('student_id', 'classroom_id',)		
    
# 學生組別    
class EnrollGroup(models.Model):
    name = models.CharField(max_length=30)
    classroom_id = models.IntegerField(default=0)

def upload_path_handler(instance, filename):
    return "static/works/user_{id}/{filename}".format(id=instance.student_id, filename=filename)

class Work(models.Model):
    user_id = models.IntegerField(default=0) 
    index = models.IntegerField()
    file = models.FileField(upload_to = upload_path_handler)
    memo = models.TextField()
    publication_date = models.DateTimeField(default=timezone.now)
    score = models.IntegerField(default=-1)
    scorer = models.IntegerField(default=0)
    
    def __unicode__(self):
        user = User.objects.filter(id=self.user_id)[0]
        index = self.index
        return user.first_name+"("+str(index)+")"

class WorkFile(models.Model):
    work_id = models.IntegerField(default=0) 
    filename = models.TextField()
    upload_date = models.DateTimeField(default=timezone.now)
		
# 小老師        
class Assistant(models.Model):
    student_id = models.IntegerField(default=0)
    classroom_id = models.IntegerField(default=0)
    lesson = models.IntegerField(default=0)
    
    @property        
    def student(self):
        return User.objects.get(id=self.student_id)         

    class Meta:
        unique_together = ('student_id', 'classroom_id', 'lesson', )		        
	
# 測驗卷
class Exam(models.Model):
    exam_id = models.IntegerField(default=0)
    student_id = models.IntegerField(default=0)
    answer = models.CharField(max_length=10)
    score = models.IntegerField(default=0)
    publication_date = models.DateTimeField(default=timezone.now)	
    
# Bug求救
class Bug(models.Model):
    title = models.CharField(max_length=250)
    file = models.FileField()
    author_id = models.IntegerField(default=0)
    classroom_id = models.IntegerField(default=0)
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)

    @property
    def author(self):
        return User.objects.get(id=self.author_id)
									
    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

# 除錯							 
class Debug(models.Model):
    bug_id = models.IntegerField(default=0)
    author_id = models.IntegerField(default=0)
    file = models.FileField()	
    body = models.TextField()
    publish = models.DateTimeField(auto_now_add=True)
    reward = models.IntegerField(default=-1)
    reward_date = models.DateTimeField(auto_now_add=True) 
	
    @property
    def author(self):
        return User.objects.get(id=self.author_id)
		
    @property
    def bug_author_id(self):
        return self.bug.author_id

    @property
    def bug(self):
        return Bug.objects.get(id=self.bug_id)

		
    class Meta:
        ordering = ('-publish',)    

    def __str__(self):
        return 'Comment by {} on {}'.format(self.author_id, self.bug)
        

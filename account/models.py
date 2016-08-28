# -*- coding: UTF-8 -*-
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User


# 個人檔案資料
class Profile(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL,related_name="profile")
	#user_id = models.IntegerField(default=0)
	# 12堂課進度
	lock = models.IntegerField(default=1)
	# 積分：上傳作業
	work = models.IntegerField(default=0)
	# 積分：擔任小老師
	assistant = models.IntegerField(default=0)
	# 積分：除錯
	debug = models.IntegerField(default=0)
	# 積分：創意秀
	creative = models.IntegerField(default=0)
	# 大頭貼等級
	avatar = models.IntegerField(default=0)
	# 訪客人次
	visitor_count = models.IntegerField(default=0)
	# 開站時間
	open_time = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return str(self.user_id)
	
# 積分記錄 
class PointHistory(models.Model):
    # 使用者序號
	user_id = models.IntegerField(default=0)
	# 積分類別 1:上傳作業 2:小老師 3:除錯 4:創意秀
	kind = models.IntegerField(default=0)
	# 積分項目
	message = models.CharField(max_length=100)
	# 將積分項目超連結到某個頁面
	url = models.CharField(max_length=100)
	# 記載時間 
	publish = models.DateTimeField(default=timezone.now)

	def __unicode__(self):
		return str(self.user_id)
		
# 系統記錄
class Log(models.Model):
    # 使用者序號
    user_id = models.IntegerField(default=0)
    # 事件內容
    event = models.CharField(max_length=100)
	# 發生時間 
    publish = models.DateTimeField(default=timezone.now)

    @property
    def user(self):
        return User.objects.get(id=self.user_id)
	
	def __unicode__(self):
		return str(self.user_id)+'--'.self.event

# 大廳訊息	
class Message(models.Model):
    author_id = models.IntegerField(default=0)
    classroom_id = models.IntegerField(default=0)
    title = models.CharField(max_length=250)
    content = models.TextField(default='')
    url = models.CharField(max_length=250)
    time = models.DateTimeField(auto_now_add=True)

    #def __str__(self):
    #    return self.title
		
    @classmethod
    def create(cls, title, url, time):
        message = cls(title=title, url=url, time=time)
        return message

# 訊息    
class MessagePoll(models.Model):
    message_id = models.IntegerField(default=0)
    reader_id = models.IntegerField(default=0)
    classroom_id = models.IntegerField(default=0)
    read = models.BooleanField(default=False)
    
    @property
    def message(self):
        return Message.objects.get(id=self.message_id)
        
    @classmethod
    def create(cls, message_id, reader_id):
        messagepoll = cls(message_id=message_id, reader_id=reader_id)
        return messagepoll
        
# 訪客 
class Visitor(models.Model):
    date = models.IntegerField(default=0)
    count = models.IntegerField(default=0)
    
# 訪客記錄
class VisitorLog(models.Model):
    visitor_id = models.IntegerField(default=0)    
    user_id = models.IntegerField(default=0)
    IP = models.CharField(max_length=20, default="")
    time = models.DateTimeField(auto_now_add=True)
    
class Note(models.Model):
    user_id = models.IntegerField(default=0) 
    classroom_id = models.IntegerField(default=0)
    lesson = models.CharField(max_length=5)
    memo = models.TextField()
    publication_date = models.DateTimeField(default=timezone.now)
 
    def __unicode__(self):
        user = User.objects.get(id=self.user_id)
        classroom_id = self.classroom_id
        return user.first_name+"("+str(classroom_id)+")<"+self.lesson+'>'
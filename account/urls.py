# -*- coding: UTF-8 -*-
from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # post views
    url(r'^$',  views.MessageListView.as_view(), name='dashboard'),    
    #登入
    url(r'^login/$', views.user_login, name='login'),
    #登出
    url(r'^logout/$',auth_views.logout),
    url(r'^suss_logout/(?P<user_id>\d+)/$', views.suss_logout),    
    #列出所有帳號
    url(r'^userlist/$', views.UserListView.as_view()),      
    #註冊帳號
    url(r'^register/$', views.register, name='register'),   
    #個人檔案
    url(r'^profile/(?P<user_id>\d+)/$', views.profile),    
    #修改密碼
    url(r'^password-change/$', auth_views.password_change, name='password_change'),
    url(r'^password-change/done/$', auth_views.password_change_done, name='password_change_done'),    
    url(r'^password/(?P<user_id>\d+)/$', views.password),
    #修改真實姓名
    url(r'^realname/(?P<user_id>\d+)/$', views.adminrealname),    
    url(r'^realname/$', views.realname, name='realname'), 
    #修改學校
    url(r'^school/$', views.adminschool),     
    #修改信箱
    url(r'^email/$', views.adminemail),    
    #積分記錄
    url(r'^log/(?P<kind>\d+)/(?P<user_id>\d+)/$', views.LogListView.as_view()),	    
    #設定教師
    url(r'^teacher/make/$', views.make, name='make'),    
    # 列所出有圖像
    url(r'^avatar/$', views.avatar),  
    # 讀取訊息
    url(r'^message/(?P<messagepoll_id>\d+)/$', views.message),
    # 私訊
    url(r'^line/(?P<classroom_id>\d+)/$', views.LineListView.as_view()),    
    url(r'^line/class/(?P<classroom_id>\d+)/$', views.LineClassListView.as_view()),        
    url(r'^line/add/(?P<classroom_id>\d+)/(?P<user_id>\d+)/$', views.LineCreateView.as_view()),
    url(r'^line/detail/(?P<classroom_id>\d+)/(?P<message_id>\d+)/$', views.line_detail),
    #訪客
    url(r'^visitor/$', views.VisitorListView.as_view()),    
    url(r'^visitorlog/(?P<visitor_id>\d+)/$', views.VisitorLogListView.as_view()),       
    
    #手冊
    url(r'^manual/student/$', views.manual_student),    
    url(r'^manual/teacher/$', views.manual_teacher),   
    url(r'^manual/windows/$', views.manual_windows),   
    url(r'^manual/ubuntu/$', views.manual_ubuntu),   
    url(r'^manual/heroku/$', views.manual_heroku),      
    
    #好文分享
    url(r'^article/$', views.article),    

    #系統事件記錄
    url(r'^event/(?P<user_id>\d+)/$', views.EventListView.as_view()),
    url(r'^event12/(?P<user_id>\d+)/$', views.Event12ListView.as_view()),	
    url(r'^event/admin/$', views.EventAdminListView.as_view()),
    url(r'^event/admin/classroom/(?P<classroom_id>\d+)/$', views.EventAdminClassroomListView.as_view()),
    url(r'^event/calendar/(?P<user_id>\d+)/$', views.EventCalendarView.as_view()),	  
    url(r'^event/timeline/(?P<user_id>\d+)/$', views.EventTimeLineView.as_view()), 
    url(r'^event/timelog/(?P<user_id>\d+)/(?P<hour>\d+)/$', views.EventTimeLogView.as_view()),   
    url(r'^event/video/(?P<classroom_id>\d+)/$', views.EventVideoView.as_view()),   
    #筆記
    url(r'^note/add/$', views.note_add),  
    url(r'^note/get/$', views.note_get),  
    
    #影片
    url(r'^video/log/$', views.videolog),    

    #作者
    url(r'^author/$', views.author),      
]
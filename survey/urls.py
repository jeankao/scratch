# -*- coding: UTF-8 -*-
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    url(r'^pre_survey/$', views.pre_survey),
    url(r'^post_survey/$', views.post_survey),  
    url(r'^pre_result/(?P<classroom_id>\d+)/$', views.pre_result),
    url(r'^post_result/(?P<classroom_id>\d+)/$', views.post_result),  
    url(r'^pre_survey/teacher/(?P<classroom_id>\d+)/$', views.pre_teacher),  
    url(r'^post_survey/teacher/(?P<classroom_id>\d+)/$', views.post_teacher),    
]
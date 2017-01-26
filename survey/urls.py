# -*- coding: UTF-8 -*-
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    url(r'^pre_survey/$', views.pre_survey),
    url(r'^post_survey/$', views.post_survey),
]
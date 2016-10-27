# -*- coding: UTF-8 -*-
from django import template
from django.contrib.auth.models import User
from account.models import MessagePoll
from teacher.models import Classroom
from student.models import Enroll
from django.contrib.auth.models import Group
from django.utils import timezone
from django.utils.safestring import mark_safe
from datetime import datetime
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ObjectDoesNotExist

register = template.Library()

@register.filter()
def to_int(value):
    return int(value)
    
@register.filter()
def name(user_id):
    if user_id > 0 :
        user = User.objects.get(id=user_id)
        return user.first_name
    else : 
        return "匿名"
    
@register.filter()
def teacher_id(classroom_id):
    if classroom_id > 0 :
        teacher_id = Classroom.objects.get(id=classroom_id).teacher_id
        return teacher_id
    else : 
        return 0
        
@register.filter()
def reader_name(message_id):
    try:
        poll = MessagePoll.objects.get(message_id=message_id)
        user = User.objects.get(id=poll.reader_id)
        if poll.read :
            return user.first_name+u"(已讀)"
        else :
            return user.first_name
    except :
        return "noname"
        
@register.filter()
def show_member(show_id):
    members = Enroll.objects.filter(group_show=show_id)
    name = ""
    for member in members:
        name = name + '<' + member.student.first_name + '>'
    return name
    
@register.filter(name='has_group') 
def has_group(user, group_name):
    try:
        group =  Group.objects.get(name=group_name) 
    except ObjectDoesNotExist:
        group = None
    return group in user.groups.all()
    
@register.filter(name='unread') 
def unread(user_id):
    return MessagePoll.objects.filter(reader_id=user_id, read=False).count()
    
@register.filter(name="img")
def img(title):
    if title.startswith(u'[私訊]'):
        return "line"
    elif title.startswith(u'[公告]'):
        return "announce"
    elif u'擔任小老師' in title:
        return "assistant"
    elif u'設您為教師' in title:
        return "teacher"
    elif u'核發了一張證書給你' in title:
        return "certificate"
    else :
        return ""

@register.filter(name='week') 
def week(date_number):
    year = date_number / 10000
    month = (date_number - year * 10000) / 100
    day = date_number - year * 10000 - month * 100
    now = datetime(year, month, day, 8, 0, 0)
    return now.strftime("%A")
    
@register.filter(name='is_classmate') 
def is_classmate(user_id, request):
    enrolls = Enroll.objects.filter(student_id=request.user.id)
    for enroll in enrolls:
            members = Enroll.objects.filter(classroom_id=enroll.classroom_id, student_id=user_id)
            if len(members) > 0: 
                return True
    return False
	
@register.filter(name='td_range')
def td_range(num, val):
    return range(val - (num % val))

@register.filter(name='event')
def event(user):
    enrolls = Enroll.objects.filter(student_id=user.id)
    for enroll in enrolls:
        classroom = Classroom.objects.get(id=enroll.classroom_id)
        if classroom.event_open or classroom.event_video_open:
            return True
    return False
	
@register.filter
def modulo(num, val):
    return num % val

@register.filter('get_value_from_dict')
def get_value_from_dict(dict_data, key):
    """
    usage example {{ your_dict|get_value_from_dict:your_key }}
    """
    if key:
        return dict_data.get(key)
# -*- coding: UTF-8 -*-
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth import authenticate, login
from django.db.models import *
from forms import LoginForm, UserRegistrationForm, PasswordForm, RealnameForm, LineForm, SchoolForm, EmailForm
from django.contrib.auth.models import User
from account.models import Profile, PointHistory, Log, Message, MessagePoll, Visitor, VisitorLog, Note
from student.models import Enroll, Work, Assistant
from teacher.models import Classroom
from certificate.models import Certificate
from django.core.exceptions import ObjectDoesNotExist
from account.templatetags import tag 
from django.views.generic import ListView, CreateView
from django.contrib.auth.models import Group
from django.http import JsonResponse
import sys, os
from django.http import HttpResponse
from mimetypes import MimeTypes
from student.lesson import *
from student.video import *
import StringIO
import xlsxwriter
import datetime
from django.utils import timezone
from django.utils.timezone import localtime
from datetime import datetime
from django.utils import timezone
from django.apps import apps
import json
import urllib
from django.db.models import Q
from itertools import groupby
from collections import OrderedDict
# 判斷是否開啟事件記錄
def is_event_open(request):
        enrolls = Enroll.objects.filter(student_id=request.user.id)
        for enroll in enrolls:
            classroom = Classroom.objects.get(id=enroll.classroom_id)
            if classroom.event_open:
                return True
        return False

# 判斷是否開啟課程事件記錄
def is_event_video_open(request):
        enrolls = Enroll.objects.filter(student_id=request.user.id)
        for enroll in enrolls:
            classroom = Classroom.objects.get(id=enroll.classroom_id)
            if classroom.event_video_open:
                return True
        return False
        
# 判斷是否為任教學生
def is_student(user_id, request):
    classrooms = Classroom.objects.filter(teacher_id=request.user.id)
    for classroom in classrooms:
        if Enroll.objects.filter(classroom_id=classroom.id, student_id=user_id).exists(): 
            return True
    return False
    
# 判斷是否為本班同學
def is_classmate(user_id, classroom_id):
    return Enroll.objects.filter(student_id=user_id, classroom_id=classroom_id).exists()

# 網站首頁
def homepage(request):
    models = apps.get_models()
    row_count = 0
    for model in models:
        row_count = row_count + model.objects.count()
    users = User.objects.all()
    try :
        admin_user = User.objects.get(id=1)
        admin_profile = Profile.objects.get(user=admin_user)
        admin_profile.home_count = admin_profile.home_count + 1
        admin_profile.save()
    except ObjectDoesNotExist:
        admin_profile = ""
    return render_to_response('homepage.html', {'row_count':row_count, 'user_count':len(users), 'admin_profile': admin_profile}, context_instance=RequestContext(request))

# 作者
def author(request):
    return render_to_response('account/author.html', context_instance=RequestContext(request))

	
	
# 使用者登入功能
def user_login(request):
        message = None
        test = ""
        if request.method == "POST":
                form = LoginForm(request.POST)
                if form.is_valid():
                        username = request.POST['username']
                        password = request.POST['password']
                        user = authenticate(username=username, password=password)
                        if user is not None:
                                if user.is_active:
                                        if user.id == 1:
                                            if user.first_name == "": 
                                                user.first_name = "管理員"
                                                user.save()
                                                # create Message
                                                title = "請修改您的姓名"
                                                url = "/account/realname"
                                                message = Message.create(title=title, url=url, time=timezone.now())
                                                message.save()                        
                    
                                                # message for group member
                                                messagepoll = MessagePoll.create(message_id = message.id,reader_id=1)
                                                messagepoll.save()                                                             
                                        # 登入成功，導到大廳
                                        login(request, user)
                                        # 記錄系統事件
                                        log = Log(user_id=request.user.id, event='登入系統')
                                        log.save()
                                        # 記錄訪客資訊
                                        admin_user = User.objects.get(id=1)
                                        try:
                                            profile = Profile.objects.get(user=admin_user)
                                        except ObjectDoesNotExist:
                                            profile = Profile(user=admin_user)
                                            profile.save()
                                        profile.visitor_count = profile.visitor_count + 1
                                        profile.save()
                                        
                                        year = localtime(timezone.now()).year
                                        month =  localtime(timezone.now()).month
                                        day =  localtime(timezone.now()).day
                                        date_number = year * 10000 + month*100 + day
                                        try:
                                            visitor = Visitor.objects.get(date=date_number)
                                        except ObjectDoesNotExist:
                                            visitor = Visitor(date=date_number)
                                        visitor.count = visitor.count + 1
                                        visitor.save()
                                        
                                        visitorlog = VisitorLog(visitor_id=visitor.id, user_id=user.id, IP=request.META.get('REMOTE_ADDR'))
                                        visitorlog.save()
                                        
                                        return redirect('dashboard')
                                else:
                                        message = "Your user is inactive"
                        else:
                            # 記錄系統事件
                            if is_event_open(request) :                            
                                log = Log(user_id=0, event='登入失敗')
                                log.save()                                
                            message = "無效的帳號或密碼!"
        else:
                form = LoginForm()
        return render_to_response('registration/login.html', {'test': test, 'message': message, 'form': form}, context_instance=RequestContext(request))

# 記錄登出
def suss_logout(request, user_id):
    # 記錄系統事件
    if is_event_open(request) :    
        log = Log(user_id=user_id, event='登出系統')
        log.save()    
    return redirect('/account/login/')

# 訊息
class MessageListView(ListView):
    context_object_name = 'messages'
    paginate_by = 20
    template_name = 'account/dashboard.html'

    def get_queryset(self):    
        # 記錄系統事件
        if is_event_open(self.request) :           
            log = Log(user_id=self.request.user.id, event='查看訊息')
            log.save()          
        query = []
        messagepolls = MessagePoll.objects.filter(reader_id=self.request.user.id).order_by('-message_id')
        for messagepoll in messagepolls:
            query.append([messagepoll, messagepoll.message])
        return query
        
# 註冊帳號                  
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = form.save(commit=False)
            # Set the chosen password                 
            new_user.set_password(
                form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            profile = Profile(user=new_user)
            profile.save()
            # 記錄系統事件
            if is_event_open(request) :   
                log = Log(user_id=new_user.id, event='註冊帳號成功')
                log.save()                
        
            # create Message
            title = "請洽詢任課教師課程名稱及選課密碼"
            url = "/student/classroom/add"
            message = Message.create(title=title, url=url, time=timezone.now())
            message.save()                        
                    
            # message for group member
            messagepoll = MessagePoll.create(message_id = message.id,reader_id=new_user.id)
            messagepoll.save()               
            return render(request,
                          'account/register_done.html',
                          {'new_user': new_user})
    else:
        form = UserRegistrationForm()
    return render(request,
                  'account/register.html',
                  {'form': form})
      
# 顯示個人檔案
def profile(request, user_id):
    user = User.objects.get(id=user_id)
    enrolls = Enroll.objects.filter(student_id=user_id)
    try: 
        profile = Profile.objects.get(user=user)
    except ObjectDoesNotExist:
        profile = Profile(user=user)
        profile.save()

    try:
        hour_of_code = Certificate.objects.get(student_id=user_id)
    except ObjectDoesNotExist:
        hour_of_code = None

    del lesson_list[:]
    reset()
    works = Work.objects.filter(user_id=user_id)
    for work in works:
        lesson_list[work.index-1].append(work.score)
        lesson_list[work.index-1].append(work.publication_date)
        if work.score > 0 :
            score_name = User.objects.get(id=work.scorer).first_name
            lesson_list[work.index-1].append(score_name)
        else :
            lesson_list[work.index-1].append("null")

    # 計算積分    
    credit = profile.work + profile.assistant + profile.debug + profile.creative
    # 記錄系統事件
    if is_event_open(request) :       
        log = Log(user_id=request.user.id, event='查看個人檔案')
        log.save()        
        
    #檢查是否為教師或同班同學
    user_enrolls = Enroll.objects.filter(student_id=request.user.id)
    for enroll in user_enrolls:
        if is_classmate(user_id, enroll.classroom_id) or request.user.id == 1:
          return render_to_response('account/profile.html',{'hour_of_code':hour_of_code, 'works':works, 'lesson_list':lesson_list, 'enrolls':enrolls, 'profile': profile,'user_id':user_id, 'credit':credit}, context_instance=RequestContext(request))	
    if user_id == str(request.user.id):	
        return render_to_response('account/profile.html',{'hour_of_code':hour_of_code, 'works':works, 'lesson_list':lesson_list, 'enrolls':enrolls, 'profile': profile,'user_id':user_id, 'credit':credit}, context_instance=RequestContext(request))	
    return redirect("/")

	# 修改密碼
def password(request, user_id):
    if request.method == 'POST':
        form = PasswordForm(request.POST)
        if form.is_valid():
            user = User.objects.get(id=user_id)
            user.set_password(request.POST['password'])
            user.save()
            # 記錄系統事件
            if is_event_open(request) :               
                log = Log(user_id=request.user.id, event=u'修改<'+user.first_name+u'>密碼成功')
                log.save()                
            return redirect('homepage')
    else:
        form = PasswordForm()
        user = User.objects.get(id=user_id)

    return render_to_response('account/password.html',{'form': form, 'user':user}, context_instance=RequestContext(request))

# 修改他人的真實姓名
def adminrealname(request, user_id):
    if request.method == 'POST':
        form = RealnameForm(request.POST)
        if form.is_valid():
            user = User.objects.get(id=user_id)
            user.first_name =form.cleaned_data['first_name']
            user.save()
            # 記錄系統事件
            if is_event_open(request) :               
                log = Log(user_id=request.user.id, event=u'修改姓名<'+user.first_name+'>')
                log.save()                
            return redirect('/account/userlist/')
    else:
        user = User.objects.get(id=user_id)
        form = RealnameForm(instance=user)

    return render_to_response('account/realname.html',{'form': form}, context_instance=RequestContext(request))
	
# 修改自己的真實姓名
def realname(request):
    if request.method == 'POST':
        form = RealnameForm(request.POST)
        if form.is_valid():
            user = User.objects.get(id=request.user.id)
            user.first_name =form.cleaned_data['first_name']
            user.save()
            # 記錄系統事件
            if is_event_open(request) :               
                log = Log(user_id=request.user.id, event=u'修改姓名<'+user.first_name+'>')
                log.save()                
            return redirect('/account/profile/'+str(request.user.id))
    else:
        user = User.objects.get(id=request.user.id)
        form = RealnameForm(instance=user)

    return render_to_response('account/realname.html',{'form': form}, context_instance=RequestContext(request))

# 修改學校名稱
def adminschool(request):
    if request.method == 'POST':
        form = SchoolForm(request.POST)
        if form.is_valid():
            user = User.objects.get(id=request.user.id)
            user.last_name =form.cleaned_data['last_name']
            user.save()
            # 記錄系統事件
            if is_event_open(request) :               
                log = Log(user_id=request.user.id, event=u'修改學校名稱<'+user.last_name+'>')
                log.save()                
            return redirect('/account/profile/'+str(request.user.id))
    else:
        user = User.objects.get(id=request.user.id)
        form = SchoolForm(instance=user)

    return render_to_response('account/school.html',{'form': form}, context_instance=RequestContext(request))
    
# 修改信箱
def adminemail(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            user = User.objects.get(id=user_id)
            user.email =form.cleaned_data['email']
            user.save()
            # 記錄系統事件
            if is_event_open(request) :               
                log = Log(user_id=request.user.id, event=u'修改信箱<'+user.first_name+'>')
                log.save()                
            return redirect('/account/profile/'+str(request.user.id))
    else:
        user = User.objects.get(id=request.user.id)
        form = EmailForm(instance=user)

    return render_to_response('account/email.html',{'form': form}, context_instance=RequestContext(request))    

# 記錄積分項目
class LogListView(ListView):
    context_object_name = 'logs'
    paginate_by = 20
    template_name = 'account/log_list.html'
	
    def get_queryset(self):
        # 記錄系統事件
        if self.kwargs['kind'] == "1" :
            log = Log(user_id=self.kwargs['user_id'], event='查看積分--上傳作品')
        elif  self.kwargs['kind'] == "2" :
            log = Log(user_id=self.kwargs['user_id'], event='查看積分--小老師')      
        elif  self.kwargs['kind'] == "3" :
            log = Log(user_id=self.kwargs['user_id'], event='查看積分--除錯')            
        elif  self.kwargs['kind'] == "4" :
            log = Log(user_id=self.kwargs['user_id'], event='查看積分--創意秀')
        else :
            log = Log(user_id=self.kwargs['user_id'], event='查看全部積分')                        
        if is_event_open(self.request) :               
            log.save()                
        if not self.kwargs['kind'] == "0" :
            queryset = PointHistory.objects.filter(user_id=self.kwargs['user_id'],kind=self.kwargs['kind']).order_by('-id')
        else :
            queryset = PointHistory.objects.filter(user_id=self.kwargs['user_id']).order_by('-id')		
        return queryset

    def get_context_data(self, **kwargs):
        context = super(LogListView, self).get_context_data(**kwargs)
        user_name = User.objects.get(id=self.kwargs['user_id']).first_name
        context.update({'user_name': user_name})
        return context		
        
# 超級管理員可以查看所有帳號
class UserListView(ListView):
    context_object_name = 'users'
    paginate_by = 20
    template_name = 'account/user_list.html'
    
    def get_queryset(self):
        # 記錄系統事件
        if is_event_open(self.request) :           
            log = Log(user_id=1, event='管理員查看帳號')
            log.save()         
        if self.request.GET.get('account') != None:
            keyword = self.request.GET.get('account')
            queryset = User.objects.filter(Q(username__icontains=keyword) | Q(first_name__icontains=keyword)).order_by('-id')
        else :
            queryset = User.objects.all().order_by('-id')				
        return queryset

    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        account = self.request.GET.get('account')
        context.update({'account': account})
        return context	
    
# Ajax 設為教師、取消教師
def make(request):
    user_id = request.POST.get('userid')
    action = request.POST.get('action')
    if user_id and action :
        user = User.objects.get(id=user_id)           
        try :
            group = Group.objects.get(name="teacher")	
        except ObjectDoesNotExist :
            group = Group(name="teacher")
            group.save()
        if action == 'set':            
            # 記錄系統事件
            log = Log(user_id=1, event=u'管理員設為教師<'+user.first_name+'>')
            log.save()                        
            group.user_set.add(user)
            # create Message
            title = "<" + request.user.first_name + u">設您為教師"
            url = "/teacher/classroom"
            message = Message.create(title=title, url=url, time=timezone.now())
            message.save()                        
                    
            # message for group member
            messagepoll = MessagePoll.create(message_id = message.id,reader_id=user_id)
            messagepoll.save()    
        else : 
            # 記錄系統事件
            if is_event_open(request) :               
                log = Log(user_id=1, event=u'取消教師<'+user.first_name+'>')
                log.save()              
            group.user_set.remove(user)  
            # create Message
            title = "<"+ request.user.first_name + u">取消您為教師"
            url = "/"
            message = Message.create(title=title, url=url, time=timezone.now())
            message.save()                        
                    
            # message for group member
            messagepoll = MessagePoll.create(message_id = message.id,reader_id=user_id)
            messagepoll.save()               
        return JsonResponse({'status':'ok'}, safe=False)
    else:
        return JsonResponse({'status':user.first_name}, safe=False)        

def message(request, messagepoll_id):
    messagepoll = MessagePoll.objects.get(id=messagepoll_id)
    messagepoll.read = True
    messagepoll.save()
    message = Message.objects.get(id=messagepoll.message_id)
    return redirect(message.url)
    
# 列出所有私訊
class LineListView(ListView):
    model = Message
    context_object_name = 'messages'
    template_name = 'account/line_list.html'    
    paginate_by = 20
    
    def get_queryset(self):
        # 記錄系統事件
        if is_event_open(self.request) :    
            log = Log(user_id=self.request.user.id, event='查看所有私訊')
            log.save()        
        queryset = Message.objects.filter(author_id=self.request.user.id, classroom_id=0-int(self.kwargs['classroom_id'])).order_by("-id")
        return queryset

    def get_context_data(self, **kwargs):
        context = super(LineListView, self).get_context_data(**kwargs)
        context['classroom_id'] = self.kwargs['classroom_id']
        return context	 
        
# 列出同學以私訊
class LineClassListView(ListView):
    model = Enroll
    context_object_name = 'enrolls'
    template_name = 'account/line_class.html'   
    
    def get_queryset(self):
        # 記錄系統事件
        if is_event_open(self.request) :    
            log = Log(user_id=self.request.user.id, event='列出同學以私訊')
            log.save()        
        queryset = Enroll.objects.filter(classroom_id=self.kwargs['classroom_id']).order_by("seat")
        return queryset
        
    # 限本班同學
    def render_to_response(self, context):
        if not is_classmate(self.request.user.id, self.kwargs['classroom_id']):
            return redirect('/')
        return super(LineClassListView, self).render_to_response(context)            
                
#新增一個私訊
class LineCreateView(CreateView):
    model = Message
    context_object_name = 'messages'    
    form_class = LineForm
    template_name = 'account/line_form.html'     

    def form_valid(self, form):
        self.object = form.save(commit=False)
        user_name = User.objects.get(id=self.request.user.id).first_name
        self.object.title = u"[私訊]" + user_name + ":" + self.object.title
        self.object.author_id = self.request.user.id
        self.object.save()
        self.object.url = "/account/line/detail/" + self.kwargs['classroom_id'] + "/" + str(self.object.id)
        self.object.classroom_id = 0 - int(self.kwargs['classroom_id'])
        self.object.save()
        # 訊息
        messagepoll = MessagePoll(message_id=self.object.id, reader_id=self.kwargs['user_id'], classroom_id=0-int(self.kwargs['classroom_id']))
        messagepoll.save()
        # 記錄系統事件
        if is_event_open(self.request) :            
            log = Log(user_id=self.request.user.id, event=u'新增私訊<'+self.object.title+'>')
            log.save()                
        return redirect("/account/line/"+self.kwargs['classroom_id'])       
        
    def get_context_data(self, **kwargs):
        context = super(LineCreateView, self).get_context_data(**kwargs)
        context['user_id'] = self.kwargs['user_id']
        context['classroom_id'] = self.kwargs['classroom_id']
        messagepolls = MessagePoll.objects.filter(reader_id=self.kwargs['user_id'],  classroom_id=0 - int(self.kwargs['classroom_id'])).order_by('-id')
        messages = []
        for messagepoll in messagepolls:
            message = Message.objects.get(id=messagepoll.message_id)
            if message.author_id == self.request.user.id :
                messages.append([message, messagepoll.read])
        context['messages'] = messages
        return context	 
        
# 查看私訊內容
def line_detail(request, classroom_id, message_id):
    message = Message.objects.get(id=message_id)
    messes = Message.objects.filter(author_id=message.author_id, classroom_id__lt=0).order_by("-id")
    try:
        messagepoll = MessagePoll.objects.get(message_id=message_id)
    except :
        pass
    return render_to_response('account/line_detail.html', {'lists':messes, 'classroom_id':classroom_id, 'message':message, 'messagepoll':messagepoll}, context_instance=RequestContext(request))


# 列出所有日期訪客
class VisitorListView(ListView):
    model = Visitor
    context_object_name = 'visitors'
    template_name = 'account/visitor_list.html'    
    paginate_by = 20
    
    def get_queryset(self):
        # 記錄系統事件
        if is_event_open(self.request) :
            if not self.request.user.is_authenticated():
                user_id = 0
            else :
                user_id = self.request.user.id
            log = Log(user_id=user_id, event='查看所有訪客')
            log.save()        
        visitors = Visitor.objects.all().order_by('-id')
        queryset = []
        for visitor in visitors:
            queryset.append([int(str(visitor.date)[0:4]), int(str(visitor.date)[4:6]),int(str(visitor.date)[6:8]),visitor])
        return queryset
        
# 列出單日日期訪客
class VisitorLogListView(ListView):
    model = VisitorLog
    context_object_name = 'visitorlogs'
    template_name = 'account/visitorlog_list.html'    
    paginate_by = 50
    
    def get_queryset(self):
        # 記錄系統事件
        visitor = Visitor.objects.get(id=self.kwargs['visitor_id'])
        if is_event_open(self.request) :    
            log = Log(user_id=self.request.user.id, event='查看單日訪客<'+str(visitor.date)+'>')
            log.save()        
        queryset = VisitorLog.objects.filter(visitor_id=self.kwargs['visitor_id']).order_by('-id')
        return queryset
        
    def render_to_response(self, context):
        if not self.request.user.is_authenticated():
            return redirect('/')
        return super(VisitorLogListView, self).render_to_response(context)
        
# 顯示學生手冊
def manual_student(request):
    # 記錄系統事件
    if is_event_open(request) :       
        log = Log(user_id=0, event='查看學生手冊')
        log.save()        
    return render_to_response('account/manual_student.html',  context_instance=RequestContext(request))	

# 顯示教師手冊
def manual_teacher(request):
    # 記錄系統事件
    if is_event_open(request) :       
        log = Log(user_id=0, event='查看教師手冊')
        log.save()        
    return render_to_response('account/manual_teacher.html',  context_instance=RequestContext(request))	

# 顯示Windows架站
def manual_windows(request):
    # 記錄系統事件
    if is_event_open(request) :       
        log = Log(user_id=0, event='查看Windows架站')
        log.save()        
    return render_to_response('account/manual_windows.html',  context_instance=RequestContext(request))	

# 顯示Ubuntu架站
def manual_ubuntu(request):
    # 記錄系統事件
    if is_event_open(request) :       
        log = Log(user_id=0, event='查看ubuntu架站')
        log.save()        
    return render_to_response('account/manual_ubuntu.html',  context_instance=RequestContext(request))	

# 顯示Heroku架站
def manual_heroku(request):
    # 記錄系統事件
    if is_event_open(request) :       
        log = Log(user_id=0, event='查看Heroku架站')
        log.save()        
    return render_to_response('account/manual_heroku.html',  context_instance=RequestContext(request))	

# 顯示好文
def article(request):
    # 記錄系統事件
    if is_event_open(request) :       
        log = Log(user_id=0, event='查看好文分享')
        log.save()        
    return render_to_response('account/article.html',  context_instance=RequestContext(request))	

# 下載檔案
def download(request, filename):
    #down_file = File.objects.get(name = filename)
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DOWNLOAD_URL = BASE_DIR+"/download/"
    file_path = DOWNLOAD_URL + filename
    file_name = filename
    fp = open(file_path, 'rb')
    response = HttpResponse(fp.read())
    fp.close()
    mime = MimeTypes()
    type, encoding = mime.guess_type(file_name)
    if type is None:
        type = 'application/octet-stream'
    response['Content-Type'] = type
    response['Content-Length'] = str(os.stat(file_path).st_size)
    if encoding is not None:
        response['Content-Encoding'] = encoding
    if u'WebKit' in request.META['HTTP_USER_AGENT']:
        filename_header = 'filename=%s' % file_name.encode('utf-8')
    elif u'MSIE' in request.META['HTTP_USER_AGENT']:
        filename_header = ''
    else:
        filename_header = 'filename*=UTF-8\'\'%s' % urllib.quote(file_name.encode('utf-8'))
    response['Content-Disposition'] = 'attachment; ' + filename_header
    # 記錄系統事件
    if is_event_open(request) :       
        log = Log(user_id=request.user.id, event=u'下載檔案<'+filename+'>')
        log.save()     
    return response

def avatar(request):
    profile = Profile.objects.get(user = request.user)
    # 記錄系統事件
    if is_event_open(request) :       
        log = Log(user_id=request.user.id, event=u'查看個人圖像')
        log.save()        
    return render_to_response('account/avatar.html', {'avatar':profile.avatar}, context_instance=RequestContext(request))
    
# 記錄系統事件
class EventListView(ListView):
    context_object_name = 'events'
    paginate_by = 50
    template_name = 'account/event_list.html'

    def get_queryset(self):    
        user = User.objects.get(id=self.kwargs['user_id'])
        # 記錄系統事件
        if is_event_open(self.request) :           
            log = Log(user_id=self.request.user.id, event=u'查看個人事件<'+user.first_name+'>')
            log.save()       
        if self.request.GET.get('q') != None:
            queryset = Log.objects.filter(user_id=self.kwargs['user_id'], event__icontains=self.request.GET.get('q')).order_by('-id')
        else :
            queryset = Log.objects.filter(user_id=self.kwargs['user_id']).order_by('-id')
        return queryset
        
    def get_context_data(self, **kwargs):
        context = super(EventListView, self).get_context_data(**kwargs)
        q = self.request.GET.get('q')
        context.update({'q': q})
        return context	
        
    # 限本人 
    def render_to_response(self, context):
        #if is_teacher(self.kwargs['user_id'], self.request) :
        #    return redirect('/')
        return super(EventListView, self).render_to_response(context)      

# 記錄系統事件
class Event12ListView(ListView):
    context_object_name = 'events'
    paginate_by = 50
    template_name = 'account/event12_list.html'

    def get_queryset(self):    
        user = User.objects.get(id=self.kwargs['user_id'])
        # 記錄系統事件
        if is_event_open(self.request) :           
            log = Log(user_id=self.request.user.id, event=u'查看個人12堂課事件<'+user.first_name+'>')
            log.save()
        events = []
        for i in range(11):
            queryset = Log.objects.filter(user_id=self.kwargs['user_id'], event__icontains="查看課程內容<"+str(i+1)+">").order_by('-id')
            events.append(queryset)
        return events
        
    #def get_context_data(self, **kwargs):
    #    context = super(Event12ListView, self).get_context_data(**kwargs)
    #    q = self.request.GET.get('q')
    #    context.update({'q': q})
    #    return context	
        
    # 限本人 
    #def render_to_response(self, context):
    #    if not is_student(self.kwargs['user_id'], self.request) and not self.request.user.id == int(self.kwargs['user_id']):
    #        return redirect('/')
    #    return super(Event12ListView, self).render_to_response(context)      		
		
# 記錄系統事件
class EventAdminListView(ListView):
    context_object_name = 'events'
    paginate_by = 50
    template_name = 'account/event_admin_list.html'

    def get_queryset(self):    
        # 記錄系統事件
        log = Log(user_id=1, event=u'管理員查看系統事件')
        log.save()       
        if self.request.GET.get('q') != None:
            queryset = Log.objects.filter(event__icontains=self.request.GET.get('q')).order_by('-id')
        else :
            queryset = Log.objects.all().order_by('-id')
        return queryset
        
    def get_context_data(self, **kwargs):
        context = super(EventAdminListView, self).get_context_data(**kwargs)
        classrooms = Classroom.objects.all().order_by('-id')
        context['classrooms'] = classrooms
        q = self.request.GET.get('q')
        context.update({'q': q})
        return context	
        
    # 限管理員
    def render_to_response(self, context):
        if not self.request.user.id == 1 :
            return redirect('/')
        return super(EventAdminListView, self).render_to_response(context)      
        
# 記錄系統事件
class EventAdminClassroomListView(ListView):
    context_object_name = 'events'
    paginate_by = 50
    template_name = 'account/event_admin_classroom_list.html'

    def get_queryset(self):    
        # 記錄系統事件
        classroom = Classroom.objects.get(id=self.kwargs['classroom_id'])
        log = Log(user_id=1, event=u'管理員查看班級事件<'+classroom.name+'>')
        log.save()
        users = []
        enrolls = Enroll.objects.filter(classroom_id=self.kwargs['classroom_id'])
        for enroll in enrolls:
            if enroll.seat > 0 :
                users.append(enroll.student_id)
        if self.request.GET.get('q') != None:
            queryset = Log.objects.filter(user_id__in=users, event__icontains=self.request.GET.get('q')).order_by('-id')
        else :
            queryset = Log.objects.filter(user_id__in=users).order_by('-id')
        return queryset
        
    def get_context_data(self, **kwargs):
        context = super(EventAdminClassroomListView, self).get_context_data(**kwargs)
        q = self.request.GET.get('q')
        context.update({'q': q})
        classroom = Classroom.objects.get(id=self.kwargs['classroom_id'])
        context['classroom'] = classroom        
        return context	
        
    # 限管理員
    def render_to_response(self, context):
        if not self.request.user.id == 1:
            return redirect('/')
        return super(EventAdminClassroomListView, self).render_to_response(context)     
from django.utils.dateparse import parse_date
# 記錄系統事件
class EventCalendarView(ListView):
    context_object_name = 'events'
    #paginate_by = 50
    template_name = 'account/event_calendar.html'

    def get_queryset(self):    
        # 記錄系統事件
        user = User.objects.get(id=self.kwargs['user_id'])
        log = Log(user_id=self.request.user.id, event=u'查看登入記錄<'+user.first_name+'>')
        log.save()
        user_logs = Log.objects.filter(user_id=user.id, event="登入系統")
        logs = groupby(user_logs, key=lambda row: (localtime(row.publish).year, localtime(row.publish).month, localtime(row.publish).day))
        month_lists = []
        for key, value in logs:
            month_lists.append([key, list(value)])
        return month_lists
        
    def get_context_data(self, **kwargs):
        context = super(EventCalendarView, self).get_context_data(**kwargs)
        user = User.objects.get(id=self.kwargs['user_id'])
        context['user1'] = user
        return context	 

# 記錄系統事件
class EventTimeLineView(ListView):
    context_object_name = 'events'
    #paginate_by = 50
    template_name = 'account/event_timeline.html'

    def get_queryset(self):    
        # 記錄系統事件
        user = User.objects.get(id=self.kwargs['user_id'])
        log = Log(user_id=self.request.user.id, event=u'查看使用記錄<'+user.first_name+'>')
        log.save()
        user_logs = Log.objects.filter(user_id=user.id)
        logs = groupby(user_logs, key=lambda row: (localtime(row.publish).year, localtime(row.publish).month, localtime(row.publish).day, localtime(row.publish).hour))
        week = OrderedDict()
        month_list = []
        for key, value in logs:           
            month_list = [[key, list(value)]]
            week_number = datetime(*key).isocalendar()[1]
            if week.has_key(week_number):
                pass
                week[week_number].append(month_list)
            else:
                week[week_number] = [month_list]
        sorted(week.iteritems())
        return week
        
    def get_context_data(self, **kwargs):
        context = super(EventTimeLineView, self).get_context_data(**kwargs)
        context['week_number'] = datetime(*(2017,1,30)).isocalendar()[1]
        user = User.objects.get(id=self.kwargs['user_id'])
        context['user1'] = user
        return context
			
# 記錄系統事件
class EventVideoView(ListView):
    context_object_name = 'events'
    #paginate_by = 50
    template_name = 'account/event_video.html'

    def get_queryset(self):    
        # 記錄系統事件
        enrolls = Enroll.objects.filter(classroom_id=self.kwargs['classroom_id'])
        classroom = Classroom.objects.get(id=self.kwargs['classroom_id'])
        log = Log(user_id=self.request.user.id, event=u'查看影片觀看記錄<'+classroom.name+'>')
        log.save()
        students = []
        # 初始化 student_log
        for enroll in enrolls:
              students.append(enroll.student_id)
        user_logs = Log.objects.filter(Q(user_id__in=students) & (Q(event__icontains="PLAY") | Q(event__icontains="PAUSE")))
        logs = groupby(user_logs, key=lambda row: row.user_id)
        student_logs = {}
        datas = {}
        events = []
        for key, value in logs:
            student_log = list(value)
            student_logs[key] = student_log
            durations = 0
            logs = student_logs[key]
            play_time = ""
            end_time = ""
            for log in logs:
                if "PLAY" in log.event:
                    play_time = log.publish
                    playing = True
                elif "PAUSE" in log.event:
                    end_time = log.publish
                    duration = end_time - play_time
                    durations += duration.seconds
            datas[key]= durations
        for enroll in enrolls :
            if datas.has_key(enroll.student_id):
                events.append([enroll, datas[enroll.student_id]])
            else :
                events.append([enroll, 0])
        return events
        
    def get_context_data(self, **kwargs):
        context = super(EventVideoView, self).get_context_data(**kwargs)
        classroom = Classroom.objects.get(id=self.kwargs['classroom_id'])
        context['classroom'] = classroom
        enrolls = Enroll.objects.filter(classroom_id=classroom.id)
        context['height'] = 100 + enrolls.count() * 40
        return context
			
    # 限本班同學
    def render_to_response(self, context):
        try:
            enroll = Enroll.objects.get(student_id=self.request.user.id, classroom_id=self.kwargs['classroom_id'])
        except ObjectDoesNotExist :
            return redirect('/')
        return super(EventVideoView, self).render_to_response(context)        
	
			

# 新增教學筆記
def note_add(request):
    classroom_id = request.POST.get('classroomid')
    lesson = request.POST.get('lesson')
    memo = request.POST.get('memo')
    user_id = request.POST.get('userid')
    note_id = request.POST.get('noteid')
    if note_id == 0 or note_id == "0" :
        note = Note(classroom_id=classroom_id, user_id=user_id, lesson=lesson, memo=memo)
        note.save()	
        if is_event_open(request) :       
            log = Log(user_id=request.user.id, event=u'新增教學筆記')
            log.save()        
    else : 
        try: 
            note = Note.objects.get(id=note_id)
            note.memo = memo
            note.save()
            if is_event_open(request) :       
                log = Log(user_id=request.user.id, event=u'編輯教學筆記')
                log.save()    
        except:
            pass
    return JsonResponse({'status':'ok', 'note_id':note_id}, safe=False)

# 新增教學筆記
def note_get(request):
    classroom_id = request.POST.get('classroomid')
    lesson = request.POST.get('lesson')
    user_id = request.POST.get('userid')
    note_text = ""
    if not classroom_id == "0" :
        classroom_name = Classroom.objects.get(id=classroom_id).name
    else :
        classroom_name = "MyNote"
    notes = Note.objects.filter(classroom_id=classroom_id, user_id=user_id, lesson=lesson).order_by('-id')
    if notes.exists():
        for note in notes:
            note_text = note_text + str(localtime(note.publication_date).strftime("%Y-%m-%d %H:%M:%S"))
            note_text = note_text + " <a href=javascript:note_add('" + classroom_name + "'," + str(classroom_id) + ",'" + str(lesson) + "'," + str(note.id) + u")><img src='/static/images/icon_edit.png'>編輯筆記</a>" 
            note_text = note_text + "<div class=note_content_" + str(note.id) + ">" + note.memo + "</div>"
        return JsonResponse({'status':'ok', 'note_text':note_text, 'classroom_id':classroom_id}, safe=False)
    else :
        notes = None
        return JsonResponse({'status':'no_ok', 'note_text':note_text}, safe=False)
          
# 影片記錄
def videolog(request):
    tabName = request.POST.get('tabName')
    lesson = request.POST.get('lesson')
    duration = video_duration[video_url[lesson, tabName.encode("UTF-8")]]
    logs = Log.objects.filter(user_id=request.user.id, event__startswith=u"查看課程內容<"+lesson+"> | "+tabName+" |").order_by('id')
    xlist = []
    text = ""
    searching = False    
    for log in logs:
        video = log.event.split("|")
        action = video[2][1:video[2].find("[")]
        time = video[2][video[2].find("[")+1:video[2].find("]")]
        if not searching and action == "PLAY" :
            start_time = time
            start_log_time = log.publish
            searching = True
        if searching and ( action == "PAUSE" or action == "STOP") :
            row = str(localtime(start_log_time).strftime("%Y-%m-%d %H:%M:%S"))+"--["+start_time+"]--"+str(localtime(log.publish).strftime("%Y-%m-%d %H:%M:%S"))+"--["+time+ "]##"
            tmp = start_time.split(":")
            tfrom = int(tmp[0])*3600+int(tmp[1])*60+int(tmp[2])
            tmp = time.split(":")
            tto = tfrom + int((log.publish - start_log_time).total_seconds())
            xlist.append({'stamp':str(localtime(start_log_time).strftime("%Y-%m-%d %H:%M:%S")),'from':tfrom,'to':tto})
            text = text + row
            start_time = ""
            searching = False
    return JsonResponse({'status':'ok', 'text':text, 'duration':duration, 'recs':json.dumps(xlist)}, safe=False)
     
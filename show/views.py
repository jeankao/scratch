# -*- coding: utf-8 -*-
from __future__ import division
from django.shortcuts import render
from show.models import ShowGroup, ShowReview
from django.core.exceptions import ObjectDoesNotExist
from student.models import Enroll
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from show.forms import GroupForm, ShowForm, ReviewForm, ImageUploadForm, GroupShowSizeForm
from teacher.models import Classroom
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.db.models import Sum
from account.models import Profile, PointHistory, Log
from django.contrib.auth.models import User
from account.avatar import *
from django.core.exceptions import ObjectDoesNotExist
from collections import OrderedDict
from django.http import JsonResponse
from django.http import HttpResponse
import math
import cStringIO as StringIO
from PIL import Image,ImageDraw,ImageFont
from binascii import a2b_base64
import os
import StringIO
import xlsxwriter
from datetime import datetime
from django.utils.timezone import localtime

def is_teacher(user, classroom_id):
    return user.groups.filter(name='teacher').exists() and Classroom.objects.filter(teacher_id=user.id, id=classroom_id).exists()

# 判斷是否開啟事件記錄
def is_event_open(request):
        enrolls = Enroll.objects.filter(student_id=request.user.id)
        for enroll in enrolls:
            classroom = Classroom.objects.get(id=enroll.classroom_id)
            if classroom.event_open:
                return True
        return False


# 所有組別
def group(request, classroom_id):
        classroom = Classroom.objects.get(id=classroom_id)   
        student_groups = []
        group_show_open = Classroom.objects.get(id=classroom_id).group_show_open
        groups = ShowGroup.objects.filter(classroom_id=classroom_id)
        try:
                student_group = Enroll.objects.get(student_id=request.user.id, classroom_id=classroom_id).group_show
        except ObjectDoesNotExist :
                student_group = []		
        for group in groups:
            enrolls = Enroll.objects.filter(classroom_id=classroom_id, group_show=group.id)
            student_groups.append([group, enrolls,  classroom.group_show_size-len(enrolls)])
            
        #找出尚未分組的學生
        def getKey(custom):
            return custom.seat	
        enrolls = Enroll.objects.filter(classroom_id=classroom_id)
        nogroup = []
        for enroll in enrolls:
            if enroll.group_show == 0 :
		        nogroup.append(enroll)		
	    nogroup = sorted(nogroup, key=getKey)            
            
        # 記錄系統事件
        if is_event_open(request) :         
            log = Log(user_id=request.user.id, event=u'查看創意秀組別<'+classroom.name+'>')
            log.save()              
        return render_to_response('show/group.html', {'nogroup': nogroup, 'group_show_open':group_show_open, 'teacher':is_teacher(request.user, classroom_id), 'student_groups':student_groups, 'classroom_id':classroom_id, 'student_group':student_group}, context_instance=RequestContext(request))

# 新增組別
def group_add(request, classroom_id):
        classroom_name = Classroom.objects.get(id=classroom_id).name
        if request.method == 'POST':
            form = GroupForm(request.POST)
            if form.is_valid():
                group = ShowGroup(name=form.cleaned_data['name'],classroom_id=int(classroom_id))
                group.save()
                enrolls = Enroll.objects.filter(classroom_id=classroom_id)
                for enroll in enrolls :
                    review = ShowReview(show_id=group.id, student_id=enroll.student_id)
                    review.save()
                    
                # 記錄系統事件
                if is_event_open(request) :                 
                    log = Log(user_id=request.user.id, event=u'新增創意秀組別<'+group.name+'><'+classroom_name+'>')
                    log.save()                      
                return redirect('/show/group/'+classroom_id)
        else:
            form = GroupForm()
        return render_to_response('show/group_add.html', {'form':form}, context_instance=RequestContext(request))

# 設定組別人數
def group_size(request, classroom_id):
        if request.method == 'POST':
            form = GroupShowSizeForm(request.POST)
            if form.is_valid():
                classroom = Classroom.objects.get(id=classroom_id)
                classroom.group_show_size = form.cleaned_data['group_show_size']
                classroom.save()
                
                # 記錄系統事
                if is_event_open(request) :                  
                    log = Log(user_id=request.user.id, event=u'設定創意秀組別人數<'+classroom.name+'><'+str(form.cleaned_data['group_show_size'])+'>')
                    log.save()        
        
                return redirect('/show/group/'+classroom_id)
        else:
            classroom = Classroom.objects.get(id=classroom_id)
            form = GroupShowSizeForm(instance=classroom)
        return render_to_response('show/group_size.html', {'form':form}, context_instance=RequestContext(request))        

# 加入組別
def group_enroll(request, classroom_id,  group_id):
        classroom_name = Classroom.objects.get(id=classroom_id).name    
        group_name = ShowGroup.objects.get(id=group_id).name
        enroll = Enroll.objects.filter(student_id=request.user.id, classroom_id=classroom_id)
        enroll.update(group_show=group_id)
        # 記錄系統事件
        if is_event_open(request) :         
            log = Log(user_id=request.user.id, event=u'加入創意秀組別<'+group_name+'><'+classroom_name+'>')
            log.save()                      
        return redirect('/show/group/'+classroom_id)

# 刪除組別
def group_delete(request, group_id, classroom_id):
        classroom_name = Classroom.objects.get(id=classroom_id).name    
        group_name = ShowGroup(id=group_id).name    
        group = ShowGroup.objects.get(id=group_id)
        # 記錄系統事件
        if is_event_open(request) :         
            log = Log(user_id=request.user.id, event=u'刪除創意秀組別<'+group_name+'><'+classroom_name+'>')
            log.save()     
        group.delete()
        return redirect('/show/group/'+classroom_id)    

# 開放選組
def group_open(request, classroom_id, action):
    classroom = Classroom.objects.get(id=classroom_id)
    if action == "1":
        classroom.group_show_open=True
        classroom.save()
        # 記錄系統事件
        if is_event_open(request) :         
            log = Log(user_id=request.user.id, event=u'開放創意秀選組<'+classroom.name+'>')
            log.save()         
    else :
        classroom.group_show_open=False
        classroom.save()
        # 記錄系統事件
        if is_event_open(request) :         
            log = Log(user_id=request.user.id, event=u'關閉創意秀選組<'+classroom.name+'>')
            log.save()          
    return redirect('/show/group/'+classroom_id)  	
	

# 上傳創意秀
class ShowUpdateView(UpdateView):
    #model = ShowGroup
    #fields = ['name', 'title','number']
    form_class = ShowForm
    #template_name_suffix = '_update_form'
    #success_url = "/show/group/2"

    def get(self, request, **kwargs):
        self.object = ShowGroup.objects.get(id=self.kwargs['group_show'])
        members = Enroll.objects.filter(group_show=self.kwargs['group_show'])
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        context = self.get_context_data(object=self.object, form=form, members=members)
        return self.render_to_response(context)

    def get_object(self, queryset=None):
        obj = ShowGroup.objects.get(id=self.kwargs['group_show'])
        return obj
		
    def form_valid(self, form):
        obj = form.save(commit=False)
        
        # 限制小組成員才能上傳
        members = Enroll.objects.filter(group_show=self.kwargs['group_show'])
        is_member = False
        for member in members :
            if self.request.user.id == member.student_id:
                is_member = True
        
        if is_member :        
            if obj.done == False:
                for member in members:			
			        # credit
                    update_avatar(member.student_id, 4, 3)
                    # History
                    history = PointHistory(user_id=member.student_id, kind=4, message=u'3分--繳交創意秀<'+obj.title+'>', url='/show/detail/'+str(obj.id))
                    history.save()
            #save object
            obj.publish = timezone.now()
            obj.done = True
            obj.save()
        
            # 記錄系統事件
            if is_event_open(self.request) :             
                log = Log(user_id=self.request.user.id, event=u'上傳創意秀<'+obj.name+'>')
                log.save()
            return redirect('/show/group/'+self.kwargs['classroom_id'])
        else :
            return redirect('homepage')

# 評分
class ReviewUpdateView(UpdateView):
    model = ShowReview
    form_class = ReviewForm
    template_name_suffix = '_review'

    def get(self, request, **kwargs):
        show = ShowGroup.objects.get(id=self.kwargs['show_id'])
        try:
            self.object = ShowReview.objects.get(show_id=self.kwargs['show_id'], student_id=self.request.user.id)
        except ObjectDoesNotExist:
            self.object = ShowReview(show_id=self.kwargs['show_id'], student_id=self.request.user.id)
            self.object.save()        
        reviews = ShowReview.objects.filter(show_id=self.kwargs['show_id'], done=True)
        score1 = reviews.aggregate(Sum('score1')).values()[0]
        score2 = reviews.aggregate(Sum('score2')).values()[0]
        score3 = reviews.aggregate(Sum('score3')).values()[0]
        score = [self.object.score1, self.object.score2,self.object.score3]
        if reviews.count() > 0 :
            score1 = score1 / reviews.count()     
            score2 = score2 / reviews.count()  
            score3 = score3 / reviews.count()          
            scores = [math.ceil(score1*10)/10, math.ceil(score2*10)/10, math.ceil(score3*10)/10,  reviews.count()]

        else :
            scores = [0,0,0,0]
        members = Enroll.objects.filter(group_show=self.kwargs['show_id'])
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        context = self.get_context_data(show=show, form=form, members=members, review=self.object, scores=scores, score=score, reviews=reviews)
        return self.render_to_response(context)

    def get_object(self, queryset=None):
        try :
            obj = ShowReview.objects.get(show_id=self.kwargs['show_id'], student_id=self.request.user.id)
        except ObjectDoesNotExist:
            obj = ShowReview(show_id=self.kwargs['show_id'], student_id=self.request.user.id)
            obj.save()
        return obj
	
    def form_valid(self, form):
        show = ShowGroup.objects.get(id=self.kwargs['show_id'])        
        #save object
        obj = form.save(commit=False)
        if obj.done == False:
            classroom_id = ShowGroup.objects.get(id=self.kwargs['show_id']).classroom_id
            member = Enroll.objects.get(classroom_id=classroom_id, student_id=self.request.user.id)
            # credit
            update_avatar(member.student, 4, 1)
            # History
            show = ShowGroup.objects.get(id=self.kwargs['show_id'])			
            history = PointHistory(user_id=member.student_id, kind=4, message=u'1分--評分創意秀<'+show.title+'>', url='/show/detail/'+str(show.id))
            history.save()
        obj.publish = timezone.now()
        obj.done = True
        obj.save()
        # 記錄系統事件
        if is_event_open(self.request) :         
            log = Log(user_id=self.request.user.id, event=u'評分創意秀<'+show.name+'>')
            log.save()        
        return redirect('/show/detail/'+self.kwargs['show_id'])

# 所有同學的評分		
class ReviewListView(ListView):
    context_object_name = 'reviews'
    template_name = 'show/reviewlist.html'
    def get_queryset(self):
        show = ShowGroup.objects.get(id=self.kwargs['show_id'])        
        # 記錄系統事件
        if is_event_open(self.request) :         
            log = Log(user_id=self.request.user.id, event=u'查看創意秀所有評分<'+show.name+'>')
            log.save()  
        return ShowReview.objects.filter(show_id=self.kwargs['show_id'])  		

    def get_context_data(self, **kwargs):
        ctx = super(ReviewListView, self).get_context_data(**kwargs)
        try :
           review = ShowReview.objects.get(show_id=self.kwargs['show_id'], student_id=self.request.user.id)
        except ObjectDoesNotExist:
            review = ShowReview(show_id=self.kwargs['show_id'], student_id=self.request.user.id)
            review.save()        
        show = ShowGroup.objects.get(id=self.kwargs['show_id']) 
        members = Enroll.objects.filter(group_show=self.kwargs['show_id'])
        reviews = ShowReview.objects.filter(show_id=self.kwargs['show_id'], done=True)
        score1 = reviews.aggregate(Sum('score1')).values()[0]
        score2 = reviews.aggregate(Sum('score2')).values()[0]
        score3 = reviews.aggregate(Sum('score3')).values()[0]
        score = [review.score1, review.score2, review.score3]
        if reviews.count() > 0 :
            score1 = score1 / reviews.count()     
            score2 = score2 / reviews.count()  
            score3 = score3 / reviews.count()          
            scores = [math.ceil(score1*10)/10, math.ceil(score2*10)/10, math.ceil(score3*10)/10,  reviews.count()]
        else :
            scores = [0,0,0,0]        
        ctx['scores'] = scores
        ctx['show'] = show
        ctx['members'] = members
        return ctx

# 排行榜
class RankListView(ListView):
    context_object_name = 'lists'
    template_name = 'show/ranklist.html'
    def get_queryset(self):
        def getKey(custom):
            return custom[2]	
        lists = []
        shows = ShowGroup.objects.filter(classroom_id=self.kwargs['classroom_id'])
        for show in shows :
            students = Enroll.objects.filter(group_show=show.id)
            reviews = ShowReview.objects.filter(show_id=show.id, done=True)	
            if reviews.count() > 0 :			
                score = reviews.aggregate(Sum('score'+self.kwargs['rank_id'])).values()[0]/reviews.count()
            else :
                score = 0
            lists.append([show, students, score, reviews.count(), self.kwargs['rank_id']])
            lists= sorted(lists, key=getKey, reverse=True)
        # 記錄系統事件
        if is_event_open(self.request) :         
            log = Log(user_id=self.request.user.id, event=u'查看創意秀排行榜<'+self.kwargs['rank_id']+'>')
            log.save()  
        return lists

# 教師查看創意秀評分情況
class TeacherListView(ListView):
    context_object_name = 'lists'
    template_name = 'show/teacherlist.html'
    def get_queryset(self):
        lists = {}
        counter = 0
        enrolls = Enroll.objects.filter(classroom_id=self.kwargs['classroom_id']).order_by('seat')
        classroom_name = Classroom.objects.get(id=self.kwargs['classroom_id']).name
        for enroll in enrolls:
            lists[enroll.id] = []	            
            shows = ShowGroup.objects.filter(classroom_id=self.kwargs['classroom_id'])
            if not shows.exists():
                lists[enroll.id].append([enroll])
            else :
                for show in shows:
                    members = Enroll.objects.filter(group_show=show.id)
                    try: 
                        review = ShowReview.objects.get(show_id=show.id, student_id=enroll.student_id)
                    except ObjectDoesNotExist:
                        review = ShowReview(show_id=show.id)
                    lists[enroll.id].append([enroll, review, show, members])
		lists = OrderedDict(sorted(lists.items(), key=lambda x: x[1][0][0].seat))
        # 記錄系統事件
        if is_event_open(self.request) :         
            log = Log(user_id=self.request.user.id, event=u'查看創意秀評分狀況<'+classroom_name+'>')
            log.save()  
		
        return lists
        
        

# 藝廊                  
class GalleryListView(ListView):
    context_object_name = 'lists'
    paginate_by = 3
    template_name = 'show/gallerylist.html'
    def get_queryset(self):
        # 記錄系統事件
        if self.request.user.id > 0 :
            log = Log(user_id=self.request.user.id, event=u'查看藝廊')
        else :
            log = Log(user_id=0,event=u'查看藝廊')
        if is_event_open(self.request) :             
            log.save() 
        
        return ShowGroup.objects.filter(open=True).order_by('-publish')
		
# 查看藝郎某項目
def GalleryDetail(request, show_id):
    show = ShowGroup.objects.get(id=show_id)
    reviews = ShowReview.objects.filter(show_id=show_id, done=True)
    score1 = reviews.aggregate(Sum('score1')).values()[0]
    score2 = reviews.aggregate(Sum('score2')).values()[0]
    score3 = reviews.aggregate(Sum('score3')).values()[0]
    if reviews.count() > 0 :
        score1 = score1 / reviews.count()     
        score2 = score2 / reviews.count()  
        score3 = score3 / reviews.count()          
        scores = [math.ceil(score1*10)/10, math.ceil(score2*10)/10, math.ceil(score3*10)/10,  reviews.count()]
    else :
        scores = [0,0,0,0]        
    members = Enroll.objects.filter(group_show=show_id)
    #context = self.get_context_data(show=show, form=form, members=members, review=self.object, scores=scores, score=score, reviews=reviews)
    # 記錄系統事件
    if request.user.id > 0 :
        log = Log(user_id=request.user.id, event=u'查看藝廊<'+show.name+'>')
    else :
        log = Log(user_id=0, event=u'查看藝廊<'+show.name+'>')
    log.save() 
    
    return render(request, 'show/gallerydetail.html', {'show': show, 'members':members, 'scores':scores, 'reviews':reviews, 'teacher':is_teacher(request.user, show.classroom_id)})

# 將創意秀開放到藝廊
def make(request):
    show_id = request.POST.get('showid')
    action = request.POST.get('action')
    if show_id and action :
        try :
            show = ShowGroup.objects.get(id=show_id)	
            if action == 'open':
                show.open = True
                # 記錄系統事件
                if is_event_open(request) :                 
                    log = Log(user_id=request.user.id, event=u'藝廊上架<'+show.name+'>')
                    log.save()                 
            else:
                show.open = False		
                # 記錄系統事件
                if is_event_open(request) :                 
                    log = Log(user_id=request.user.id, event=u'藝廊下架<'+show.name+'>')
                    log.save()                          
            show.save()
        except ObjectDoesNotExist :
            pass
        return JsonResponse({'status':'ok'}, safe=False)        
    else:
        return JsonResponse({'status':'ko'}, safe=False)       
        
# 上傳 Dr Scratch 分析圖
def upload_pic(request, show_id):
    m = []
    if request.method == 'POST':
        '''
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                m = ShowGroup.objects.get(id=show_id)
                m.picture = form.cleaned_data['image']
				
                image_field = form.cleaned_data.get('image')
                image_file = StringIO.StringIO(image_field.read())
                image = Image.open(image_file)
                image = image.resize((800, 600), Image.ANTIALIAS)
                image_file = StringIO.StringIO()
                image.save(image_file, 'JPEG', quality=90)
                image_field.file = image_file
                m.save()
            except ObjectDoesNotExist:
                pass
            classroom_id = Enroll.objects.filter(student_id=request.user.id).order_by('-id')[0].classroom.id
            # 記錄系統事件
            log = Log(user_id=request.user.id, event='上傳Dr Scratch分析圖成功')
            log.save()             
            return redirect('/show/detail/'+show_id)
            '''
        try:
            dataURI = request.POST.get("screenshot")
            head, data = dataURI.split(',', 1)
            mime, b64 = head.split(';', 1)
            mtype, fext = mime.split('/', 1)
            binary_data = a2b_base64(data)
            directory = 'static/show/' + show_id
            image_file = "static/show/{id}/{filename}.{ext}".format(id=show_id, filename='Dr-Scratch', ext=fext)
            if not os.path.exists(directory):
                os.makedirs(directory)
            with open(image_file, 'wb') as fd:
                fd.write(binary_data)
                fd.close()
            m = ShowGroup.objects.get(id=show_id)
            m.picture = image_file
            m.save()
        except ObjectDoesNotExist:
            pass
        classroom_id = Enroll.objects.filter(student_id=request.user.id).order_by('-id')[0].classroom.id
        # 記錄系統事件
        if is_event_open(request) :         
            log = Log(user_id=request.user.id, event='上傳Dr Scratch分析圖成功')
            log.save()             
        return redirect('/show/detail/'+show_id+'/#drscratch')
    else :
        try:
            m = ShowGroup.objects.get(id=show_id)   
        except ObjectDoesNotExist:
            pass
        form = ImageUploadForm()
    return render_to_response('show/drscratch.html', {'form':form, 'show': m}, context_instance=RequestContext(request))

def excel(request, classroom_id):
    # 記錄系統事件
    if is_event_open(request) :       
        log = Log(user_id=request.user.id, event=u'下載創意秀到Excel')
        log.save()        

    output = StringIO.StringIO()
    workbook = xlsxwriter.Workbook(output)    
            
    shows = ShowGroup.objects.filter(classroom_id=classroom_id)
    
    worksheet = workbook.add_worksheet(u"分組")
    c = 0
    for show in shows:
        worksheet.write(c, 0, show.name)
        worksheet.write(c, 1, show.title)
        worksheet.write(c, 2, "https://scratch.mit.edu/projects/"+show.number)
        number = 3
        members = Enroll.objects.filter(group_show=show.id)
        for member in members:
            worksheet.write(c, number, "("+str(member.seat)+")"+member.student.first_name)
            number = number + 1        
        c = c + 1
    for show in shows :
        worksheet = workbook.add_worksheet(show.name)
        worksheet.write(0,0, u"組員")
        number = 1
        members = Enroll.objects.filter(group_show=show.id)
        for member in members:
            worksheet.write(0, number, "("+str(member.seat)+")"+member.student.first_name)
            number = number + 1
        worksheet.write(1,0, u"作品名稱") 
        worksheet.write(1,1, show.name)
        worksheet.write(2,0, u"上傳時間") 
        worksheet.write(2,1, str(localtime(show.publish)))        
        worksheet.write(3,0, u"作品位置")
        worksheet.write(3,1, "https://scratch.mit.edu/projects/"+str(show.number))

        worksheet.write(4,0, u"評分者")
        worksheet.write(4,1, u"美工設計")
        worksheet.write(4,2, u"程式難度")
        worksheet.write(4,3, u"創意表現")
        worksheet.write(4,4, u"評語")
        worksheet.write(4,5, u"時間")
        showreviews = ShowReview.objects.filter(show_id=show.id)        
        score1 = showreviews.aggregate(Sum('score1')).values()[0]
        score2 = showreviews.aggregate(Sum('score2')).values()[0]
        score3 = showreviews.aggregate(Sum('score3')).values()[0]
        if showreviews.count() > 0 :
            score1 = score1 / showreviews.count()     
            score2 = score2 / showreviews.count()  
            score3 = score3 / showreviews.count()          
            scores = [math.ceil(score1*10)/10, math.ceil(score2*10)/10, math.ceil(score3*10)/10,  showreviews.count()]
        else :
            scores = [0,0,0,0]
        
        worksheet.write(5,0, u"平均("+str(scores[3])+u"人)")
        worksheet.write(5,1, scores[0])
        worksheet.write(5,2, scores[1])
        worksheet.write(5,3, scores[2])        

        index = 6
        
        reviews = []
        for showreview in showreviews:
            enroll = Enroll.objects.get(classroom_id=classroom_id, student_id=showreview.student_id)
            reviews.append([showreview, enroll])
        
        def getKey(custom):
            return custom[1].seat
	
        reviews = sorted(reviews, key=getKey)        
        for review in reviews:
            worksheet.write(index,0, "("+str(review[1].seat)+")"+review[1].student.first_name)
            worksheet.write(index,1, review[0].score1)
            worksheet.write(index,2, review[0].score2)
            worksheet.write(index,3, review[0].score3)            
            worksheet.write(index,4, review[0].comment)  
            worksheet.write(index,5, str(localtime(review[0].publish)))             
            index = index + 1
        worksheet.insert_image(index+1,0, 'static/show/'+str(show.id)+'/Dr-Scratch.png')
    workbook.close()
    # xlsx_data contains the Excel file
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Show'+str(datetime.now().date())+'.xlsx'
    xlsx_data = output.getvalue()
    response.write(xlsx_data)
    return response

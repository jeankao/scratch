# -*- coding: utf-8 -*-
from django import forms
from teacher.models import Classroom
from student.models import Work, Enroll
from account.models import Message

# 新增一個課程表單
class ClassroomForm(forms.ModelForm):
        class Meta:
           model = Classroom
           fields = ['name','password']
        
        def __init__(self, *args, **kwargs):
            super(ClassroomForm, self).__init__(*args, **kwargs)
            self.fields['name'].label = "班級名稱"
            self.fields['password'].label = "選課密碼"
           

# 作業評分表單           
class ScoreForm(forms.ModelForm):
        RELEVANCE_CHOICES = (
            (100, "你好棒(100分)"),
            (90, "90分"),
            (80, "80分"),
            (70, "70分"),
            (60, "60分"),
        )
        score = forms.ChoiceField(choices = RELEVANCE_CHOICES, required=True, label="分數")
        #if user.groups.all()[0].name == 'teacher': 
        assistant = forms.BooleanField(required=False,label="小老師")
    
        class Meta:
           model = Work
           fields = ['score']
		   
        def __init__(self, user, *args, **kwargs): 
            super(ScoreForm, self).__init__(*args, **kwargs)	
            if user.groups.all().count() == 0 :
                del self.fields['assistant']

Check_CHOICES = (
    (100, "你好棒(100分)"),
    (90, "90分"),
    (80, "80分"),
    (70, "70分"),
    (60, "60分"),
    (40, "40分"),
    (20, "20分"),
    (0, "0分"),			
)				
				
class CheckForm1(forms.ModelForm):

        score_memo1 = forms.ChoiceField(choices = Check_CHOICES, required=True, label="分數")
        #if user.groups.all()[0].name == 'teacher': 
        certificate = forms.BooleanField(required=False,label="核發證書",initial=True)
    
        class Meta:
           model = Enroll
           fields = ['score_memo1']

class CheckForm2(forms.ModelForm):

        score_memo2 = forms.ChoiceField(choices = Check_CHOICES, required=True, label="分數")
        #if user.groups.all()[0].name == 'teacher': 
        certificate = forms.BooleanField(required=False,label="核發證書",initial=True)
    
        class Meta:
           model = Enroll
           fields = ['score_memo2']
		   
class CheckForm3(forms.ModelForm):

        score_memo3 = forms.ChoiceField(choices = Check_CHOICES, required=True, label="分數")
        #if user.groups.all()[0].name == 'teacher': 
        certificate = forms.BooleanField(required=False,label="核發證書",initial=True)
    
        class Meta:
           model = Enroll
           fields = ['score_memo3']
		   
class CheckForm4(forms.ModelForm):

        score_memo4 = forms.ChoiceField(choices = Check_CHOICES, required=True, label="分數")
        #if user.groups.all()[0].name == 'teacher': 
        certificate = forms.BooleanField(required=False,label="核發證書",initial=True)
    
        class Meta:
           model = Enroll
           fields = ['score_memo4']
           
# 新增一個課程表單
class AnnounceForm(forms.ModelForm):
        class Meta:
           model = Message
           fields = ['title', 'content']
        
        def __init__(self, *args, **kwargs):
            super(AnnounceForm, self).__init__(*args, **kwargs)
            self.fields['title'].label = "公告主旨"
            self.fields['title'].widget.attrs['size'] = 50	
            self.fields['content'].label = "公告內容"
            self.fields['content'].widget.attrs['cols'] = 50
            self.fields['content'].widget.attrs['rows'] = 20        
            
  
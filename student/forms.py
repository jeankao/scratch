# -*- coding: utf-8 -*-
from django import forms
from teacher.models import Classroom
from student.models import Enroll, EnrollGroup, Work, Bug, Debug

class EnrollForm(forms.Form):
        password =  forms.CharField()
        seat = forms.CharField()
        
        def __init__(self, *args, **kwargs):
            super(EnrollForm, self).__init__(*args, **kwargs)
            self.fields['password'].label = "選課密碼"
            self.fields['seat'].label = "座號"
        
class GroupForm(forms.ModelForm):
        class Meta:
           model = EnrollGroup
           fields = ['name']
           
        def __init__(self, *args, **kwargs):
            super(GroupForm, self).__init__(*args, **kwargs)
            self.fields['name'].label = "組別名稱"

# 組別人數
class GroupSizeForm(forms.ModelForm):
        class Meta:
           model = Classroom
           fields = ['group_size']
        
        def __init__(self, *args, **kwargs):
            super(GroupSizeForm, self).__init__(*args, **kwargs)
            self.fields['group_size'].label = "小組人數"
        
class SubmitForm(forms.ModelForm):
        class Meta:
           model = Work
           fields = ['number','memo']
           
        def __init__(self, *args, **kwargs):
            super(SubmitForm, self).__init__(*args, **kwargs)
            self.fields['number'].label = "作品編號"
            self.fields['memo'].label = "心得感想"

class SeatForm(forms.ModelForm):
        class Meta:
            model = Enroll
            fields = ['seat']

class BugForm(forms.ModelForm):
        class Meta:
           model = Bug
           fields = ['number','title', 'body']
           
        def __init__(self, *args, **kwargs):
            super(BugForm, self).__init__(*args, **kwargs)
            self.fields['title'].label = "問題主旨"
            self.fields['number'].label = "作品編號"
            self.fields['body'].label = "問題說明"
           
class DebugForm(forms.ModelForm):
        class Meta:
            model = Debug
            fields = ['number', 'body']
        
        def __init__(self, *args, **kwargs):
            super(DebugForm, self).__init__(*args, **kwargs)
            self.fields['body'].label = "除錯內容"
            self.fields['number'].label = "作品編號"
			
class DebugValueForm(forms.ModelForm):
        RELEVANCE_CHOICES = (
            (0, "沒有解決"),
            (1, "部份解決"),
            (2, "大概解決"),
            (3, "完全解決"),
		)
		
        reward = forms.ChoiceField(choices = RELEVANCE_CHOICES, required=True, label="解決程度")	
        id = forms.IntegerField(widget=forms.HiddenInput())
		
        class Meta:
            model = Debug
            fields = ['reward','id']
			
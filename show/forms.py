# -*- coding: utf-8 -*-
from django import forms
from show.models import ShowGroup, ShowReview
from teacher.models import Classroom
#from django.views.generic.edit import UpdateView

# 組別
class GroupForm(forms.ModelForm):
        class Meta:
           model = ShowGroup
           fields = ['name']
           
        def __init__(self, *args, **kwargs):
            super(GroupForm, self).__init__(*args, **kwargs)
            self.fields['name'].label = "組別名稱"

# 作品		
class ShowForm(forms.ModelForm):
        class Meta:
           model = ShowGroup
           fields = ['number','title','body']
           
        def __init__(self, *args, **kwargs):
            super(ShowForm, self).__init__(*args, **kwargs)
            self.fields['title'].label = "作品主題"
            self.fields['number'].label = "作品編號"
            self.fields['body'].label = "作品說明"
			
# 評分
class ReviewForm(forms.ModelForm):
        class Meta:
            model = ShowReview
            fields = ['score1', 'score2', 'score3', 'comment']
			
        #def __init__(self, *args, **kwargs):
            #super(ReviewForm, self).__init__(*args, **kwargs)
            #self.fields['score1'].label = "美工設計"
            #self.fields['score2'].label = "程式難度"
            #self.fields['score3'].label = "創意表現"
            #self.fields['comment'].label = "評語"			 
            
class ImageUploadForm(forms.Form):
    """Image upload form."""
    image = forms.ImageField()
    
# 組別人數
class GroupShowSizeForm(forms.ModelForm):
        class Meta:
           model = Classroom
           fields = ['group_show_size']
        
        def __init__(self, *args, **kwargs):
            super(GroupShowSizeForm, self).__init__(*args, **kwargs)
            self.fields['group_show_size'].label = "小組人數"
        
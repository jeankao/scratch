# -*- coding: UTF-8 -*-
from django import forms
from django.contrib.auth.models import User
from account.models import Log, Message, MessagePoll

# 使用者登入表單
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = "帳號"
        self.fields['password'].label = "密碼"
        
    
class UserRegistrationForm(forms.ModelForm):
    error_messages = {
        'duplicate_username': ("此帳號已被使用")
    }
    
    username = forms.RegexField(
        label="User name", max_length=30, regex=r"^[\w.@+-]+$",
        error_messages={
            'invalid': ("帳號名稱無效")
        }
    )
    
    password = forms.CharField(label='Password', 
                               widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', 
                                widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']
            
    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = "帳號"
        self.fields['first_name'].label = "真實姓名"
        self.fields['last_name'].label = "學校名稱"
        self.fields['email'].label = "電子郵件"
        self.fields['password'].label = "密碼"
        self.fields['password2'].label = "再次確認密碼"
        
    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        username = self.cleaned_data["username"]
        if self.instance.username == username:
            return username
        try:
            User._default_manager.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(
            self.error_messages['duplicate_username'],
            code='duplicate_username',
        )

# 修改密碼表單
class PasswordForm(forms.ModelForm):
        class Meta:
            model = User
            fields = ['password']

# 修改真實姓名表單       
class RealnameForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name']
            
    def __init__(self, *args, **kwargs):
        super(RealnameForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].label = "真實姓名"
        
# 修改學校表單       
class SchoolForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['last_name']
            
    def __init__(self, *args, **kwargs):
        super(SchoolForm, self).__init__(*args, **kwargs)
        self.fields['last_name'].label = "學校名稱"        

# 修改信箱表單       
class EmailForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']
            
    def __init__(self, *args, **kwargs):
        super(EmailForm, self).__init__(*args, **kwargs)
        self.fields['email'].label = "電子郵件"        
        self.fields['email'].widget.attrs['size'] = 50

# 查詢事件
class EventForm(forms.ModelForm):
    class Meta:
        model = Log
        fields = ['event']    
        
            
    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields['event'].label = "事件名稱"        
        
# 新增一個私訊表單
class LineForm(forms.ModelForm):

        class Meta:
           model = Message
           fields = ['title','content',]
        
        def __init__(self, *args, **kwargs):
            super(LineForm, self).__init__(*args, **kwargs)
            self.fields['title'].label = "主旨"
            self.fields['title'].widget.attrs['size'] = 50
            self.fields['content'].label = "內容"
            self.fields['content'].widget.attrs['cols'] = 50
            self.fields['content'].widget.attrs['rows'] = 20                              

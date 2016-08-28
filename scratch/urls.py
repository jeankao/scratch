"""scratch URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from account import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^account/', include('account.urls')),
    url(r'^teacher/', include('teacher.urls')),    
    url(r'^student/', include('student.urls')),        
    url(r'^certificate/', include('certificate.urls')),     
    url(r'^show/', include('show.urls')),     
    url(r'^download/(?P<filename>[^/]+)/$', views.download), 
    url(r'^$', views.homepage, name='homepage'),
    
]

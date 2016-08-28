from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    # post views
    url(r'^$', views.upload_pic),   
    url(r'^show/(?P<unit>\d+)/(?P<enroll_id>\d+)/$', views.show),   
    #url(r'^image/(?P<unit>\d+)/(?P<enroll_id>\d+)/(?P<teacher_id>\d+)/$', 'certificate.views.make_image'),   
    url(r'^classroom/(?P<unit>\d+)/(?P<classroom_id>\d+)/$', views.classroom),   
    url(r'^make/$', views.make, name='make'),
	url(r'^make_certification/(?P<unit>\d+)/(?P<enroll_id>\d+)/(?P<action>[^/]+)/$', views.make_certification),
    #url(r'^test/$', views.test, name='test'),	
]
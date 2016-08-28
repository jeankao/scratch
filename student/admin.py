from django.contrib import admin

from student.models import Assistant, Work, Enroll

# Register your models here.
admin.site.register(Assistant)
admin.site.register(Work)
admin.site.register(Enroll)

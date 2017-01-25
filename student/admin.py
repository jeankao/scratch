from django.contrib import admin

from student.models import Assistant, Work, Enroll, WorkFile

# Register your models here.
admin.site.register(Assistant)
admin.site.register(Work)
admin.site.register(Enroll)
admin.site.register(WorkFile)

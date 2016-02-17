from django.contrib import admin

# Register your models here.
from .models import Course, Section, User, TimeWindow, Tag, Expertise, PrevAssignment, Application

admin.site.register(Course)
admin.site.register(Section)
admin.site.register(User)
admin.site.register(TimeWindow)
admin.site.register(Tag)
admin.site.register(Expertise)
admin.site.register(PrevAssignment)
admin.site.register(Application)

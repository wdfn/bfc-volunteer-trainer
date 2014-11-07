from django.contrib import admin
from trainingtracker.models import Section, Course, Comment, Skill, Job, Timeslot

# Register your models here.
admin.site.register(Section)
admin.site.register(Course)
admin.site.register(Comment)
admin.site.register(Skill)
admin.site.register(Job)
admin.site.register(Timeslot)
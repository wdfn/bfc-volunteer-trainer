from django.contrib import admin
from django.contrib.auth.models import User
from trainingtracker.models import Attendance, Section, Course, Comment, Skill, Job, Timeslot, Trainee

# Register your models here.
class DatesInline(admin.StackedInline):
    model = Timeslot
    extra = 3

class TraineesInline(admin.TabularInline):
    model = Trainee

class SectionAdmin(admin.ModelAdmin):
    inlines = [DatesInline, TraineesInline]
    filter_horizontal = ("courses", "skills", "jobs",)

class AttendancesInline(admin.TabularInline):
    model = Attendance

class TraineeAdmin(admin.ModelAdmin):
    inlines = [AttendancesInline]


admin.site.register(Section, SectionAdmin)
admin.site.register(Trainee, TraineeAdmin)
admin.site.register(Course)
#admin.site.register(Comment)
admin.site.register(Skill)
admin.site.register(Job)
#admin.site.register(Timeslot)

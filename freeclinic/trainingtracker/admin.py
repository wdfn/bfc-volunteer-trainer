from django.contrib import admin
from django.contrib.auth.models import User, Group
from models import Attendance, Section, Course, Comment, Skill, SkillCompletion, Job, Timeslot, Trainee

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
    extra = 0
    can_delete = False

class SkillInline(admin.TabularInline):
    model = SkillCompletion
    extra = 0
    can_delete = False
    required = False

class TraineeAdmin(admin.ModelAdmin):
    inlines = [AttendancesInline, SkillInline]

class CourseAdmin(admin.ModelAdmin):
    inlines = [AttendancesInline]

class SkillAdmin(admin.ModelAdmin):
    inlines = [SkillInline]


admin.site.register(Section, SectionAdmin)
admin.site.register(Trainee, TraineeAdmin)
admin.site.register(Course, CourseAdmin)
#admin.site.register(Comment)
admin.site.register(Skill, SkillAdmin)
admin.site.register(Job)
admin.site.unregister(Group)
#admin.site.register(Timeslot)

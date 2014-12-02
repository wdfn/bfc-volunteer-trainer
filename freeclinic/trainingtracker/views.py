from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from models import Course, Trainee, Section, Attendance, SkillCompletion, Timeslot, Shift
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.utils.html import escape
from django.views.generic.edit import View
from django import forms
# from django.views.generic.edit import UpdateView



# Create your views here.

# TODO:
#    * Logout view

# This is our landing page, after the user logs in. 
@login_required
def index(request):
    # Gets currently logged in user
    curr_user = request.user
    context = {}

    # Check if user is a trainee, if not, we don't show any data. 
    # Remember, to be in a section, you must be a trainee. 
    try: 
        curr_user = Trainee.objects.get(user=curr_user)
    except Trainee.DoesNotExist:
        return redirect('/nosectionfound')

    # curr_user is now a trainee. Let's get some information.
    context['curr_section'] = curr_user.section
    context['curr_courses'] = curr_user.courses.order_by("id") 
    context['curr_skills'] = curr_user.skills.order_by("id") 
    context['curr_jobs'] = curr_user.jobs.order_by("id")
    context['curr_timeslots'] = Timeslot.objects.filter(section=curr_user.section)
    context['curr_user'] = curr_user

    
    # we want all the other trainee's in this section, except for the current user.
    all_other_trainees = Trainee.objects.filter(section=context['curr_section']).exclude(user=curr_user.user)
    
    # we create a dictionary mapping the other trainees to their attendance and skill completion querysets
    others = {}
    for trainee in all_other_trainees:
        others[trainee] = {'attendances': Attendance.objects.filter(trainee=trainee).order_by('course__id'), 'skill_comps': SkillCompletion.objects.filter(trainee=trainee).order_by('skill__id')}
    context['others'] = others

    shifts = {}
    for timeslot in Timeslot.objects.filter(section=curr_user.section):
        shifts[timeslot] = Shift.objects.filter(timeslot=timeslot)
    context['curr_shifts'] = shifts
    
    # current_user's attendances
    attendances = Attendance.objects.filter(trainee=curr_user).order_by('course__id')
    skill_completions = SkillCompletion.objects.filter(trainee=curr_user).order_by('skill__id')

    # Add on the current user's attendances so they always show up first / somehow seperate
    context['my_attendances'] = attendances
    context['my_skill_comps'] = skill_completions

    return render(request, 'bfctraining/index.html', context)

# What do we need here?
#   Class name
#   Class description
#   Some unique box identifier
#   Comments... do we display them publicly? No, we will just send an email

class get_User(View):
    def set_user_and_section_and_courses(self, curr_user, context):
        context['curr_section'] = curr_user.section
        context['curr_courses'] = curr_user.courses.order_by("id") 
        context['curr_user'] = curr_user
        return context

    def set_username_and_fname_and_lname_and_email(self, curr_user, context):
        context['username'] = curr_user.user.username
        context['fname'] = curr_user.user.first_name
        context['lname'] = curr_user.user.last_name
        context['email'] = curr_user.user.email
        return context

@login_required
def course(request, course_identifier):
    # This is essentially copy and pasted from above
    curr_user = request.user
    context = {}

    # Check if user is a trainee, if not, we don't show any data. 
    # Remember, to be in a section, you must be a trainee. 
    try: 
        curr_user = Trainee.objects.get(user=curr_user)
    except Trainee.DoesNotExist:
        return redirect('/nosectionfound')

    context = set_user_and_section_and_courses(curr_user, context)

    # Actual content unique to courses
    context['id'] = course_identifier
    curr_course = get_object_or_404(Course, id=course_identifier)
    context['description'] = curr_course.description
    context['name'] = curr_course.name
    # We only display the embed from box if this string isn't empty
    context['include_box'] = True if len(curr_course.box_embed_code) > 0 else False
    # We need to HTML escape the embed code to prevent XSS.
    context['embedcode'] = escape(curr_course.box_embed_code)

    return render(request, 'bfctraining/course.html', context)

# We do some brief work (assign a shift to the current user) and then return a redirect to the homepage.
@login_required
def takeshift(request, shift_identifier):
    curr_user = request.user
    context = {}

    try: 
        curr_user = Trainee.objects.get(user=curr_user)
    except Trainee.DoesNotExist:
        return redirect('/nosectionfound')

    curr_shift = get_object_or_404(Shift, id=shift_identifier)

    if curr_shift.taken:
        return redirect('/shiftalreadytaken')

    curr_shift.trainee = curr_user
    curr_shift.save()

    return redirect('/index')

@login_required
def settings(request):
    return HttpResponse("Place-holder for user settings page")

# This is the index for someone logged in without a Section (no tables, no classes, etc.)
@login_required
def noSectionFound(request):
    return HttpResponse("Your account has not been assigned to a section. Please contact your staff and have them add you to a section.")

def logout_view(request):
    logout(request)
    return render(request, "bfctraining/logout.html")


class Settings(get_User):
    def get(self, request):
        curr_user = request.user

        context = {}

        try: 
            curr_user = Trainee.objects.get(user=curr_user)
        except Trainee.DoesNotExist:
            return redirect('/nosectionfound')

    # We display the current user's information.
        context = self.set_user_and_section_and_courses(curr_user, context)
        context = self.set_username_and_fname_and_lname_and_email(curr_user, context)

        return render(request, 'bfctraining/settings.html', context)

    def post(self, request):

        curr_user = request.user

        try: 
            curr_user = Trainee.objects.get(user=curr_user)
        except Trainee.DoesNotExist:
            return redirect('/nosectionfound')

        context = {}

        new_username = request.POST['username']
        new_firstname = request.POST['firstname']
        new_lastname = request.POST['lastname']
        new_email = request.POST['email']

        if new_username != "":
            curr_user.user.username = new_username
        if new_firstname != "":
            curr_user.user.first_name = new_firstname
        if new_lastname != "":
            curr_user.user.last_name = new_lastname
        if new_email != "":
            curr_user.user.email = new_email

        curr_user.user.save()

        context = self.set_user_and_section_and_courses(curr_user, context)
        context = self.set_username_and_fname_and_lname_and_email(curr_user, context)

        return render(request, 'bfctraining/settings.html', context)

def set_user_and_section_and_courses(curr_user, context):
    context['curr_section'] = curr_user.section
    context['curr_courses'] = curr_user.courses.order_by("id") 
    context['curr_user'] = curr_user
    return context

def set_username_and_fname_and_lname_and_email(curr_user, context):
    context['username'] = curr_user.user.username
    context['fname'] = curr_user.user.first_name
    context['lname'] = curr_user.user.last_name
    context['email'] = curr_user.user.email
    return context


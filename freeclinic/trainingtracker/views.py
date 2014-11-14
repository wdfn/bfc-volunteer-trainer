from django.shortcuts import render, redirect
from django.http import HttpResponse
from trainingtracker.models import Course, Trainee, Section, Attendance
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.html import escape
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
    context['curr_user'] = curr_user
    
    # we want all the other trainee's in this section, except for the current user.
    all_other_trainees = Trainee.objects.filter(section=context['curr_section']).exclude(user=curr_user.user)
    
    # we create a dictionary mapping the other trainees to their attendance queryset
    others = {}
    for trainee in all_other_trainees:
        others[trainee] = Attendance.objects.filter(trainee=trainee).order_by('course__id')
    context['others'] = others
    
    # current_user's attendances
    attendances = Attendance.objects.filter(trainee=curr_user).order_by('course__id')

    # Add on the current user's attendances so they always show up first / somehow seperate
    context['my_attendances'] = attendances

    return render(request, 'bfctraining/index.html', context)

# What do we need here?
#   Class name
#   Class description
#   Some unique box identifier
#   Comments... do we display them publicly? 
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

    context['curr_section'] = curr_user.section
    context['curr_courses'] = curr_user.courses.order_by("id") 
    context['curr_user'] = curr_user

    # Actual content unique to courses
    context['id'] = course_identifier
    curr_course = Course.objects.get(id=course_identifier)
    context['description'] = curr_course.description
    context['name'] = curr_course.name
    # We only display the embed from box if this string isn't empty
    context['include_box'] = True if len(curr_course.box_embed_code) > 0 else False
    # We need to HTML escape the embed code to prevent XSS.
    context['embedcode'] = escape(curr_course.box_embed_code)

    return render(request, 'bfctraining/course.html', context)

@login_required
def settings(request):
    return HttpResponse("Place-holder for user settings page")

# This is the index for someone logged in without a Section (no tables, no classes, etc.)
@login_required
def noSectionFound(request):
    return HttpResponse("Place-holder for no section page.")

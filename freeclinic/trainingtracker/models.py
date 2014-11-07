from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Course(models.Model):
    # Course description
    description = models.TextField()

    # Box URL

    # Name
    name = models.CharField(max_length=50, unique=True)

    # Make the string show up nicely
    def __str__(self):
        return self.name


class Comment(models.Model):
    # Text
    text = models.TextField()

    # Date Published
    published = models.DateTimeField()

    # Course posted for 
    course = models.ForeignKey(Course)

class Skill(models.Model):
    # Name
    name = models.CharField(max_length=50, unique=True)

    # Make the string show up nicely
    def __str__(self):
        return self.name

    # In Which Sections?

class Job(models.Model):
    # Name
    name = models.CharField(max_length=50, unique=True)

    # Make the string show up nicely
    def __str__(self):
        return self.name

    # In Which Sections?


# I add the "null=True, blank=True" here in an attempt to allow the creation of sections without
# explicitly created courses, skills, jobs, and timeslots. For example, when creating
# a new secion, we may not have timeslots properly added. You can read more about this
# here: https://docs.djangoproject.com/en/dev/ref/models/fields/
class Section(models.Model):
    # Name
    name = models.CharField(max_length=50, unique=True)

    # List of classes
    courses = models.ManyToManyField(Course, null=True, blank=True)

    # List of skills
    skills = models.ManyToManyField(Skill, null=True, blank=True)

    # List of jobs
    jobs = models.ManyToManyField(Job, null=True, blank=True)

    # Make the string show up nicely
    def __str__(self):
        return self.name


# List of users - how do I plug in to django.contrib.auth?
class Trainee(models.Model):
    user = models.OneToOneField(User)
    section = models.ForeignKey(Section)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name

# These should definitely be unique to a Section
class Timeslot(models.Model):
    # Starting Time and Ending Times
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    # This is a user, not a trainee, in case a non trainee wants to sign up for a position
    worker = models.ForeignKey(User)

    # Which unique section is this in?
    section = models.ForeignKey(Section)

# This is the actual model determining whether a Trainee has attended a Course or not
class Attendance(models.Model):
    trainee = models.ForeignKey(Trainee)
    course = models.ForeignKey(Course)
    # Assume they haven't yet attended
    attended = models.BooleanField(default=False)

# This is the model containing the value of a skill
class SkillCompletion(models.Model):
    trainee = models.ForeignKey(Trainee)
    skill = models.ForeignKey(Skill)

    value = models.CharField(max_length=100)





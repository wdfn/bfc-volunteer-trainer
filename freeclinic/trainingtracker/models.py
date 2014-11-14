from django.db import models
from django.contrib.auth.models import User

# Create your models here
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

class Course(models.Model):
    # Course description
    description = models.TextField()

    # Box URL
    box_embed_code = models.CharField(max_length=100)
    
    # Name
    name = models.CharField(max_length=50, unique=True)

    # Make the string show up nicely
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return "/course/%i" % self.id

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

# These should definitely be unique to a Section
class Timeslot(models.Model):
    # Starting Time and Ending Times
    start_time = models.DateTimeField()

    end_time = models.DateTimeField()

    # This is a user, not a trainee, in case a non trainee wants to sign up for a position
    worker = models.ForeignKey(User)

    # Which unique section is this in?
    section = models.ForeignKey(Section)


# Inherits, in a way, from users in the OneToOneField
class Trainee(models.Model):
    user = models.OneToOneField(User)
    section = models.ForeignKey(Section)
    
    def _trainees_courses(self):
        return self.section.courses

    courses = property(_trainees_courses)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name

    # We need to ensure, somehow, that the trainee has attendance objects for each course in it's section.
    def save(self, *args, **kwargs):
        # Remove old attendances
        if Attendance.objects.filter(trainee=self).exists():
            for attendance in Attendance.objects.filter(trainee=self):
                attendance.delete()
        super(Trainee,self).save(*args,**kwargs)
        # Add the new ones
        for course in self.courses.all():
            if not Attendance.objects.filter(trainee=self,course=course).exists():
                new_attendance = Attendance(trainee=self,course=course)
                new_attendance.save()
    
    # We use the name in the models so we create a method to get it here
    def name(self):
        return str(self)

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

class Comment(models.Model):
    # Text
    text = models.TextField()

    # Date Published
    published = models.DateTimeField()

    # Course posted for 
    course = models.ForeignKey(Course)




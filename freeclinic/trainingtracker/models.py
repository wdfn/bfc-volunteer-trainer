from django.db import models

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

class Timeslot(models.Model):
    # Date
    start_time = models.DateTimeField()

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

    # List of timeslots
    timeslots = models.ManyToManyField(Timeslot, null=True, blank=True)

    # Make the string show up nicely
    def __str__(self):
        return self.name

    # List of users - how do I plug in to django.contrib.auth?


from django.db import models
from django.contrib.auth.models import User

# Create your models here
class Skill(models.Model):
    # Name
    name = models.CharField(max_length=50, unique=True)

    # Make the string show up nicely
    def __str__(self):
        return self.name

    # Regenerate all skills for trainees - is this neccesary?
    def save(self, *args, **kwargs):
        if SkillCompletion.objects.filter(skill=self).exists():
            for skillcompletion in SkillCompletion.objects.filter(section=self):
                skillcompletion.trainee.save()
    
        super(Skill,self).save(*args,**kwargs)
    
class Course(models.Model):
    # Course description
    description = models.TextField()

    # Box URL
    box_embed_code = models.CharField(max_length=100, blank=True)
    
    # Name
    name = models.CharField(max_length=50, unique=True)

    # Make the string show up nicely
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return "/course/%i" % self.id

    # Regenerate all courses for trainees - Is this neccesary?
    def save(self, *args, **kwargs):
        if Attendance.objects.filter(course=self).exists():
            for attendance in Attendance.objects.filter(section=self):
                attendance.trainee.save()    
        super(Course,self).save(*args,**kwargs)

class Job(models.Model):
    # Name
    name = models.CharField(max_length=50, unique=True)

    # Make the string show up nicely
    def __str__(self):
        return self.name
      

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

    # Regenerate all skills, attendances for trainees. 
    def save(self, *args, **kwargs):
        super(Section,self).save(*args,**kwargs)
        if Trainee.objects.filter(section=self).exists():
            for trainee in Trainee.objects.filter(section=self):
                trainee.save()
        if Timeslot.objects.filter(section=self).exists():
            for timeslot in Timeslot.objects.filter(section=self).all():
                timeslot.save()

# Inherits, in a way, from users in the OneToOneField
class Trainee(models.Model):
    user = models.OneToOneField(User)
    section = models.ForeignKey(Section)
    
    def _trainees_courses(self):
        return self.section.courses

    def _trainees_skills(self):
        return self.section.skills

    def _trianees_jobs(self):
        return self.section.jobs

    courses = property(_trainees_courses)
    skills = property(_trainees_skills)
    jobs = property(_trianees_jobs)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name

    # We need to ensure, somehow, that the trainee has attendance objects for each course in it's section.
    def save(self, *args, **kwargs):
        super(Trainee,self).save(*args,**kwargs)
        # Add the new ones
        # Remove old attendances, saving previous attendances
        if Attendance.objects.filter(trainee=self).exists():
            for attendance in Attendance.objects.filter(trainee=self):
                if attendance.course not in self.courses.all():
                    attendance.delete()

        if SkillCompletion.objects.filter(trainee=self).exists():
            for skillcompletion in SkillCompletion.objects.filter(trainee=self):
                if skillcompletion.skill not in self.skills.all():
                    skillcompletion.delete()
        
        for course in self.courses.all():
            if not Attendance.objects.filter(trainee=self,course=course).exists():
                new_attendance = Attendance(trainee=self,course=course)
                new_attendance.save()

        for skill in self.skills.all():
            if not SkillCompletion.objects.filter(trainee=self,skill=skill).exists():
                new_skill = SkillCompletion(trainee=self,skill=skill)
                new_skill.save()
    
    # We use the name in the models so we create a method to get it here
    def name(self):
        return str(self)

# These should definitely be unique to a Section
class Timeslot(models.Model):
    # Starting Time and Ending Times
    start_time = models.DateTimeField()

    end_time = models.DateTimeField()

    section = models.ForeignKey(Section)

    def save(self, *args, **kwargs):
        super(Timeslot,self).save(*args,**kwargs)
        # make sure all shifts for all timeslots in section exist
        for timeslot in Timeslot.objects.filter(section=self):
            for job in self.section.jobs.all():
                if not Shift.objects.filter(timeslot=timeslot, job=job).exists():
                    print "no " + str(timeslot) + " and " + str(job) + " job exist"
                    new_shift = Shift()
                    new_shift.timeslot = timeslot
                    new_shift.job = job
                    new_shift.save()

class Shift(models.Model):
    timeslot = models.ForeignKey(Timeslot)
    job = models.ForeignKey(Job)
    trainee = models.ForeignKey(Trainee, blank=True, null=True)

    def _taken(self):
        return self.trainee != None

    taken = property(_taken)
    
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

    value = models.CharField(max_length=100, default="", blank=True)

class Comment(models.Model):
    # Text
    text = models.TextField()

    # Date Published
    published = models.DateTimeField()

    # Course posted for 
    course = models.ForeignKey(Course)




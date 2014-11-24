from django.core.management.base import BaseCommand, CommandError
from trainingtracker.models import Course, Skill

class Command(BaseCommand):
    help = 'Generates test data based on args'
    args = '<Courses, Trainees, Sections, Skills> <number to generate>'

    def handle(self, *args, **kwargs):
        if len(args) > 2:
            raise CommandError('Only accepts a model name and the number to create.')
        if args[0] == "Courses":
            for course in Course.objects.all():
                course.delete()
            for i in range(0, int(args[1])):
                new_course = Course()
                new_course.name = "Course " + str(i)
                new_course.description = "Description for course " + str(i)
                new_course.save()
        elif args[0] == "Skills":
            for skill in Skill.objects.all():
                skill.delete()
            for i in range(0, int(args[1])):
                new_skill = Skill()
                new_skill.name = "Skill " + str(i)
                new_skill.save()
        else:
            raise CommandError('Model doesn\'t exist or hasn\'t been implemented yet.')


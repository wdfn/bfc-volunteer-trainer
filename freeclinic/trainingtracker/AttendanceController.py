from django.shortcuts import render
from freeclinic.trainingtracker.models import Attendance, Course, Trainee

def change(request):
	user_id = request.POST["user"]
	course_id = request.POST["course"]
	trainee = Trainee.objects.get(id=user_id)
	curr_user = request.user


	try:
		context = {}
		context["success"] = False
		if curr_user.has_perm('trainingtracker.change_attendance'):
		
			attendance = Attendance.objects.filter(trainee__id=user_id).filter(course__id=course_id)[0]
			
			if attendance.attended:
				attendance.attended = False
			else:
				attendance.attended = True
			attendance.save()
			context["success"] = True
			
	except Exception as e:
		context["success"] = str(e)
	return render(request, 'ajax/change_attendance.html', context)
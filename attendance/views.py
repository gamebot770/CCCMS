from django.shortcuts import render
from django.views.generic import ListView
from django.http import HttpResponse
from clubSetup.models import *

# Create your views here.
"""
class updateAttendance(ListView):
	
	model = Student
	context_object_name = "studList"
	template_name = "attendanceUpdate.html"
"""


def updateAttendance(request,clubID):
	
	studList = Student.objects.all()
	formList = Form.objects.all()
	
	context = {"studList":studList,"formList":formList}
	
	return render(request,"attendanceUpdate.html",context)
	
	

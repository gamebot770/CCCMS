from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [

	url(r'^(\d+)/update/$',views.updateAttendance,name="attendanceUpdate"),
	url(r'^(\d+)/received/$',views.attendedStudents,name="attended")
]

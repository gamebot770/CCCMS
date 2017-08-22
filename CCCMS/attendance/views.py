from django.shortcuts import render,get_object_or_404
from django.views.generic import ListView
from django.http import HttpResponse
from clubSetup.models import *
from attendance.models import *
import datetime

# Create your views here.

def updateAttendance(request,clubID):
	club = get_object_or_404(Club,pk=clubID)
	studList = Student.objects.all()
	formList = Form.objects.all()
	
	#Date Handling
	
	monthList=["","January","February","March","April","May","June","July","August","September","October","November","December"]
	weekdayList=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
	updateAvailableDate(club)#Updates the list of possible dates
	dateList = readAvailableDate(club) #Reads all dates that are possible
	
	
	criteriaList = []
	criteriaListRaw = Criteria.objects.filter(clubID = club)
	for criteria in criteriaListRaw:
		criteriaList.append(criteria)
		
	while len(criteriaList) < 3:
		criteriaList.append("None")	
	
	context = {"studList":studList,"formList":formList,"club":club,"dateList":dateList,"monthList":monthList,"clubDay":weekdayList[club.day],"criteriaList":criteriaList}
	
	return render(request,"attendanceUpdate.html",context)
	

def attendedStudents(request,clubID):
	studList = []
	studDictListRaw = request.POST
	
	#Skips the csrf token
	studDictList = iter(studDictListRaw)
	print(studDictList)
	next(studDictList)
	
	dateKey = next(studDictList)
	
	
	
	
	#Creates list of students who have attended
	print(request.POST)
	for studDict in studDictList:	
		
		stud = Student.objects.get(pk=studDict) 
	
	
	#Processing of attended students
	
	club = Club.objects.get(pk=clubID)
	clubFilePath = clubInfoStorage.location + "/" + club.name + "/attendance"
	addToMaster(clubFilePath,"Master_File.ca",studList)
	
	#Obtain the Date from the dictionary and convert to datetime object
	#NOTE : returned date as string value
	date = request.POST[dateKey]
	date = datetime.datetime.strptime(date, '%Y/%m/%d') 
	
	writeDateData(club,date,studList)
	
	
	
	return render(request,"attended.html",{"studList":studList})


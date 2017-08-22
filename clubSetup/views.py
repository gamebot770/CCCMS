from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from .models import *


# Create your views here.
def clubSetup(request):
	context={}
	return render(request,"clubSetup/mainPage1.html",context)

def installClub(request):
	determineCurrentTerm()
	a = Club()
	
	a.name = request.POST['clubName']
	a.purpose = request.POST['clubPurpose']
	a.facultyAdvisor = request.POST['clubFaculty']
	a.isSportsClub = request.POST['isSportsClub']
	a.income = request.POST['clubIncome']
	a.motto = request.POST['clubMotto']
	a.day = request.POST['clubDay']
	
	a.save()
	
	termStart = Term.objects.get(pk=1).termStart
	termEnd = Term.objects.get(pk=1).termEnd
	
	days,weekdayList,monthList,startMonth,dateList = a.clubDates(termStart,termEnd,int(a.day))
	clubDay = weekdayList[int(a.day)]
	
	a.setDates(dateList)
	a.getDates()
	a.countDates()
	a.save()

	determineCurrentTerm()
	context = {"dayList":days,"weekdayList":weekdayList,"monthList":monthList,"startMonth":startMonth,"clubDay":clubDay,"dateList":dateList}
	
	return render(request,"clubSetup/submitted.html",context)


def details(request,clubID):
	
	club1 = Club.objects.get(pk=clubID)
	
	context = {"club":club1}
	
	return render(request,"clubSetup/details.html",context)
		

def uploadStudList(request):
	return render(request,"clubSetup/uploadStudList.html",{})

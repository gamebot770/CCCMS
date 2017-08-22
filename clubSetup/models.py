from django.db import models
from django.core.files.storage import FileSystemStorage
from datetime import *
from .pythonFunctions import fileManip
import calendar
import pickle
import os
import csv



# REMEMBER TO FIX HARDCODED CRITERIA CALCULATOR

#############################
#  							#
#	FUNCTION DECLARATIONS 	#
#						  	#
#############################




#File storage location for the student list.
studStorage = FileSystemStorage(location = 'Files/studentList')
attendanceStorage = FileSystemStorage(location = 'Files/attendance')

def fileLoad(path):
	#Module controlling the upload of students to the database
	studentList = []
	
	#opens File
	
	fileName = "StudentTest.csv"
	fullPath = path + "/" + fileName
	fp = open(fullPath,"r")
	
	#Reads students from file
	readStudents(fp,studentList)
	
	#Registers students on the database
	registerStudents(studentList)
	
	
	
def searchForm(formName):

	#Returns the form instance by searching based on form name
	formList = Form.objects.all()
	
	for form in formList:
		if formName == form.name:
			return form
			
			
def readStudents(fp,studentList):
	

	studentDictionary = csv.DictReader(fp,delimiter=",",quotechar="|")
	
	
	for stud in studentDictionary:
		studentTemp = Student()
		studentTemp.firstName = stud["First Name"]
		studentTemp.lastName = stud["Last Name"]
		studentTemp.form = searchForm(stud["Form"])
		studentList.append(studentTemp)
		print (studentList)
			

			


	
def registerStudents(studentList):
	for stud in studentList:
		print(stud.firstName)
		stud.save()
		
def determineCurrentTerm():
	now = datetime.now() #Gets current date and time
	nowDate = date(now.year,now.month,now.day)
	termList = []
	
	i = 1
	try:
		while((Term.objects.get(id = i).termStart<=nowDate and nowDate<=Term.objects.get(id = i).termEnd)==False):
			i+=1
		
		setCurrentTerm(i)
		
	except:
		print ("Not currently in a term")
		return
	
def setCurrentTerm(termIndex):
	
	termList = Term.objects.all()
	for term in termList:
		term.isCurrentTerm=False
	
	currentTerm = Term.objects.get(pk=termIndex)
	setattr(currentTerm,'isCurrentTerm',True)
	
	
def setYearID():
	yearsList = []
	yearsList = AcademicYear.objects.all()
	
	try:
		currentYear = yearsList[len(yearsList)-1].yearID + 1	#Checks previous year for yearID and sets the current yearID one year higher
	except:
		currentYear = 2017 #DEFAULT YEAR
		
	return currentYear
		

#Criteria Functions


	
#############################	
#							#
#	 MODEL DECLARATIONS		#
#							#
#############################		
		
class AcademicYear(models.Model):
	
	yearID = models.IntegerField(default=setYearID)
	studentList = models.FileField(storage=studStorage)	
	updateStudentList = models.BooleanField(default=True)
			
	def makeTerms(self):
		
		"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
			Creates 3 terms associated with the academic year
		"""""""""""""""""""""""""""""""""""""""""""""""""""""""""

		christmas = Term(name = "Christmas" + str(self.yearID))
		easter = Term(name = "Easter" + str(self.yearID))
		summer = Term(name = "Summer" + str(self.yearID))
		
		setattr(christmas,'yearID',self)
		setattr(easter,'yearID',self)
		setattr(summer,'yearID',self)
		
		christmas.save()
		easter.save()
		summer.save()
		
	def __str__(self):
		nextYear = self.yearID + 1
		return str(self.yearID) + " - " + str(nextYear)
		
	def save(self,*args,**kwargs):
		super(AcademicYear,self).save(*args,**kwargs)
		if self.updateStudentList == True :
			fileLoad(studStorage.location)
			setattr(self,'updateStudentList',False)
	
	
class Term(models.Model):
	
	defaultDate = datetime(2017,1,1)
	defaultDateEnd = datetime(2017,2,2)
	name = models.CharField(max_length=300)
	termStart = models.DateField(default=defaultDate)
	termEnd = models.DateField(default=defaultDateEnd) 
	yearID = models.ForeignKey(AcademicYear,on_delete=models.CASCADE,default=-2017)
	isCurrentTerm = models.BooleanField(default=False)

	def __str__(self):
		return self.name
	
	def getTermStart(self):
		return self.termStart
	
	def getTermEnd(self):
		return self.termEnd
		


class Club(models.Model):
	
	#Field declarations and size
	
	
	name = models.CharField(max_length = 60)
	purpose= models.CharField(max_length = 500)
	facultyAdvisor = models.CharField(max_length = 60)
	isSportsClub = models.BooleanField(max_length = 60)
	#numDaysHeld = models.IntegerField(default=0)
	#daysHeld = models.IntegerField(default=0)
	income = models.FloatField(default=0)
	#*criteria* = _to be discussed_
	motto= models.CharField(max_length=100)
	day = models.IntegerField(default=0)
	meetingsNum= models.IntegerField(default=0)
	
	
	def __str__(self):
		return self.name
		
	def weeklyUpdate(self):
		fileName = club.name + ".csv"
		fileNameAttendance = club.name + "attendance" + ".csv"
		studList = readAttendance(fileNameAttendance)
		updateMasterList(fileName,studList)
		
	def readAttendance(self,fileName):
		studentList=[]
		fullPath = attendanceStorage.location + "/" + fileName
		fp = open(fullPath,"r")
		readStudents(fp,studentList)
		
		#need to check with master list. Add if necessary.
		
	
		
	def clubDates(self,termStart,termEnd,day):
		#Initialise
		
		x=0
		i=0
		offset=0
		dateList = []

		#Lists Initialise

		listDay=[]
		totalDay=[]
		monthList=["January","February","March","April","May","June","July","August","September","October","November","December"]
		weekdayList=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
		cal= calendar.Calendar() 

		#Extracting the data from arguements 
		startMonth=termStart.month
		startDay=termStart.day
		endMonth=termEnd.month
		endDay=termEnd.day

		#Calender calculations
		for j in range(startMonth,endMonth+1):  
			offset = 0
			i = 0
			calenderList = cal.monthdayscalendar(termEnd.year, j)

			while (calenderList[i][day]==0):
				offset+=1 #represents the offset in weeks
				i+=1
			try:
				x = offset
				while(1):
					if calenderList[x][day] != 0 :
						monday = calenderList[x][day] 
						listDay.append(monday)
					x+=1
			except IndexError:
				totalDay.append(listDay)
				listDay=[]

		#Fixing the limits at beginning of loop
		i=0
		for a in totalDay[0][:]:	
			
			if a<startDay:
				totalDay[0].remove(a)
			i+=1

		#Fixing the limits at end of loop
		i=0	
		for a in totalDay[len(totalDay)-1][:]:
				
			if a>endDay:
				totalDay[len(totalDay)-1].remove(a)
			i+=1	
			
			
		#Print Statement
		monthID = startMonth	   
		for month in totalDay: #month represents list of days in a month
			
			for specificDay in month:
				dateList.append(self.createDatesList(dateList,monthID,specificDay,termEnd.year))
			monthID+=1
			
		for dates in dateList:
			print (dates)
		
		
		return(totalDay,weekdayList,monthList,startMonth,dateList)
		
		
		
		
	def	createDatesList(self,dateList,month,specificDay,year):
		tempDate = date(year,month,specificDay) #Sets tempDate as a datetime.date object that will be stored later
		return tempDate
		
		"""	
		#Print Statement
		a = startMonth	
		for month in totalDay:
			
			for specificDay in month:
				print (weekdayList[day],specificDay ,'of ',monthList[a-1])
			a+=1
		"""
	
	def setDates(self,dateList):
		
		try:
			BASE_PATH = os.path.abspath("clubSetup") #Gets absolute path to the django directory clubSetup
			folder = "dates/" #name of folder to save into
			try :
				os.mkdir(os.path.join(BASE_PATH, folder)) #creates folder to save into if it does not exist
			except :
				pass
				
			fileName = self.name + "dates.cb" 
			fullPath = os.path.join(BASE_PATH,folder,fileName) #creates full path to save file
			
			
			with open(fullPath,"wb") as file:
				for date in dateList:
					pickle.dump(date,file,-1)
			file.close()
		except FileNotFoundError:
			print("File could not be found")
		return
	
	def getDates(self):
		
		dateList = []
		try:
			BASE_PATH = os.path.abspath("clubSetup")
			folder = "dates/"
			fileName = self.name + "dates.cb"
			fullPath = os.path.join(BASE_PATH,folder,fileName)
			
			with open(fullPath,"rb") as file: #Reads all dates of club from list
				try:
					while(1):
						dateList.append(pickle.load(file))
				except EOFError:
					print("FOUND THE LIST!")
					for date in dateList:
						print (date)
					return dateList
							
		except FileNotFoundError:
			print("No file found")
			return
	
	def countDates(self):
		count = 0
		
		dateList = self.getDates()
		for date in dateList:
			count+=1
		
		setattr(self,'meetingsNum',count)
		
		return count
		
	def setAttendanceCriteria(self):
		ATTEND_MIN_PERCENT = 0.70 
		
		#Alter the value above to change the criteria set by the school
		
		self.criteria = self.countDates() * ATTEND_MIN_PERCENT

class Form(models.Model):
	
	name = models.CharField(max_length=3,primary_key=True)

	def __str__(self):
		return self.name
		
class Student(models.Model):
	
	firstName = models.CharField(max_length=250)
	lastName = models.CharField(max_length=250)
	form = models.ForeignKey(Form,on_delete=models.CASCADE,null=True)
	
	def __str__(self):
		return self.firstName + " " + self.lastName
	
	
class Critera(models.Model):
	
	question = models.CharField(max_length=250)
	
	"""
	There are currently 4 question types:
		
	type - criteriaID
	"""	
	BOOLEAN       = 0
	COUNT         = 1 
	RECORD_UP_TO  = 2
	DUES_TRACKER  = 3
	
	
		
	questionTypes =	(
		(BOOLEAN,"True/False"),
		(COUNT,"Count"),
		(RECORD_UP_TO,"Record Up To"),
		(DUES_TRACKER,"Dues Tracker")
	
	)
	criteriaID = models.IntegerField(choices=questionTypes)
	criteriaDefault = models.CharField(max_length=8)
	criteriaTarget = models.CharField(max_length=8)
	clubID = models.ForeignKey(Club,on_delete=models.CASCADE)
	
	def __str__(self):
		return self.question
	
def makeSchoolForms():
	
	#Module which creates all forms in school when run.
	
	#Creating forms 1-1 to 5-8
	
	for form in range(1,6):
		for classNum in range(1,9):
			
			formName = str(form) + "-" + str(classNum)
			formTemp = Form(name=formName)
			formTemp.save()  
			
	#Sixth form creation
	formTemp = Form(name="6A")
	formTemp.save()
	formTemp = Form(name="6B")
	formTemp.save()
	

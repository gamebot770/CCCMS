from django.db import models
from django.core.files.storage import FileSystemStorage
from django.core.files import File
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
clubInfoStorage = FileSystemStorage(location = 'Files/Clubs')


def createMainClubFolder(instance,filename):
	
	#Creates the Folder and master file in case it does not exist
	
	try:
		os.mkdir(os.path.join(clubInfoStorage.location,"%s" % instance.name))
	except:
		print("Could not make club directory")
	
	return os.path.join(clubInfoStorage.location,"%s" % instance.name)


def createCustomFolder(instance,folderName):
	
	try:
		os.mkdir(os.path.join(clubInfoStorage.location,"%s" % instance.name,"%s" % folderName))
		
	except:
		print("Could not make ",folderName," folder")
	
	return os.path.join(clubInfoStorage.location,"%s" % instance.name,"%s" % folderName)


def createFileInCustomFolder(path,fileName):

	fp = openFile(path,fileName,"rb") #Checks if file exists

	if fp==None: #If the file does not exist attempt to create it
		fp = openFile(path,fileName,"wb")
		print("File attempted to be created")
		
	if fp == None: #If the file could no be created print error message
		print("File could not be created")
	else: 
		fullPath = fp.name
		fp.close()
		return fullPath
		
def createCustomFolderAndFile(instance,folderName,fileName):
	#Creates a custom folder in club main directory and a file at the same time
	path = createCustomFolder(instance,folderName)
	fullPath = createFileInCustomFolder(path,fileName)
	return fullPath
	
def createFolderByPath(path,folderName):
	#creates a folder by specifying the path
	try:
		os.mkdir(os.path.join(path,"%s" % folderName))
	except:
		print("Could not make club directory")
	
	return os.path.join(path,"%s" % folderName)
	
def createMasterFile(instance,fileName):
	
	#creates the master File
	
	mainPath = createMainClubFolder(instance,fileName)
	attendancePath = createFolderByPath(mainPath,"attendance")
	fullPath = createFileInCustomFolder(attendancePath,"Master_File.ca")
	
	return fullPath
	
def csvFileLoad(path,fileName):
	#Module controlling the upload of students to the database
	studentList = []
	
	#opens File
	fp = openFile(path,fileName,"r")
	
	#Reads students from file
	readStudents(fp,studentList)
	
	#Registers students on the database
	registerStudents(studentList)
	
def openFile(path,fileName,mode):
	
	#opens file based on mode passed as parameter
	
	fullPath = os.path.join(path,"%s" % fileName)
	print(fullPath)
	try:
		fp = open(fullPath,mode)
		return fp
	except:
		print("Could not open File")
		return None
	

	
	
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
	
	termList = Term.objects.all()
	i = termList[0].pk
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
		print(term)
		term.isCurrentTerm=False
	
	print(termIndex)
	
	currentTerm = Term.objects.get(pk=termIndex)
	currentTerm.isCurrentTerm = True
	currentTerm.save()
	
	
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
		determineCurrentTerm()
				
		if self.updateStudentList == True :
			csvFileLoad(studStorage.location,"StudentTest.csv")
			self.updateStudentList = False
		super(AcademicYear,self).save(*args,**kwargs)
		clubList = Club.objects.all()
		for club in clubList:
			club.save()
		
	
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
		
	def save(self,*args,**kwargs):
		super(Term,self).save(*args,**kwargs)
		#Updates all clubs when a term date is changed as it will affect meeting dates.
		clubList = Club.objects.all()
		for club in clubList:
			club.save()
		

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
	meetingsNum= models.IntegerField("number of meetings",default=0)
	masterFile = models.FileField(upload_to = createMainClubFolder, null=True,max_length=1000,blank=True)
	
	
	def __str__(self):
		return self.name
		
	def weeklyUpdate(self):
		fileName = club.name + ".csv"
		fileNameAttendance = club.name + "attendance" + ".csv"
		studList = readAttendance(fileNameAttendance)
		updateMasterList(fileName,studList)
		
	def readAttendance(self,fileName):
		studentList=[]
		fullPath = clubInfoStorage.location + "/" + fileName
		fp = open(fullPath,"r")
		readStudents(fp,studentList)
		
		#need to check with master list. Add if necessary.
		
	def installClubDates(self):
		termStart = Term.objects.get(isCurrentTerm=True).termStart
		termEnd = Term.objects.get(isCurrentTerm=True).termEnd
		print(termStart)
		print(termEnd)
		print("--------------")
		dateList = self.clubDates(termStart,termEnd,int(self.day))[4]
		self.setDates(dateList)
			
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
		""""	
		for dates in dateList:
			print (dates)
		"""
		
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
			print(dateList)
			folder = "dates/" #name of folder to save into
			path = createFolderByPath(os.path.join(clubInfoStorage.location,"%s" % self.name,"attendance"),"dates")
			fullPath = createFileInCustomFolder(path,"dates.df")
			print(dateList)
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
			folder = "dates" #name of folder to save into
			path = createFolderByPath(os.path.join(clubInfoStorage.location,"%s" % self.name,"attendance"),"dates")
			fullPath = createFileInCustomFolder(path,"dates.df")
			
			with open(fullPath,"rb") as file:
				try:
					while(1):
						dateList.append(pickle.load(file))
				except EOFError:
					print("FOUND THE LIST!")
					for date in dateList:
						print (date)
					return dateList
		except FileNotFoundError:
			print("File could not be found")
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
		

	def save(self,*args,**kwargs):
		self.masterFile.name=(createMasterFile(self,""),"Master_File.ca") #Assigns the Master File to the club
		self.installClubDates()
		print(self.name)
		self.countDates()
		print("-----")
		super(Club,self).save(*args,**kwargs)
		
				
class Criteria(models.Model):
	
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
	htmlType = models.CharField(max_length=20,default="",null=True,blank=True)
	

			
	
	def __str__(self):
		return self.question
		
	
	def setHtmlType(instance):
		#Sets the HTMl type on forms
		"""""
		BOOLEAN       = 0
		COUNT         = 1 
		DUES_TRACKER  = 2
		"""
		print(instance.criteriaID)
		if instance.criteriaID == 0:
			return "checkbox"
		if instance.criteriaID == 1 or instance.criteriaID==2:
			return "number"
			
	def save(self,*args,**kwargs):
		self.htmlType = self.setHtmlType()
		super(Criteria,self).save(*args,**kwargs)
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
	

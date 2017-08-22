from django.db import models
from clubSetup.models import *
import pickle as f
from datetime import datetime

# Create your models here.

""""
def attendanceFileUpdate(path,fileName,studList):
	fp = openFile(path,fileName,"r")
	prevStudList = extractStudents
	for stud in studList:
		checkStudent(stud,)
"""	

def updateAvailableDate(club):
	updatedDateList = []
	
	#Updates the available dates for a club by comparing it to the current date
	#And dates which already exist
	path = os.path.join(clubInfoStorage.location,"%s" % club.name,"attendance/dates")
	fp = openFile(path,"available.df","wb")
	dateList = club.getDates()
	now = datetime.now().date()
	
	for date in dateList:
		if date<now and readDateData(club,date)==None:
			f.dump(date,fp,-1)
		
	
def readAvailableDate(club):
	dateList = []
	path = os.path.join(clubInfoStorage.location,"%s" % club.name,"attendance/dates")
	fp = openFile(path,"available.df","rb")
	
	try:
		while(1):
			dateList.append(f.load(fp))
	except:
		pass
		
	return dateList

def readDateData(club,date):
	studList = []
	path = os.path.join(clubInfoStorage.location,"%s" % club.name,"attendance/dates")
	fp = openFile(path,(str(date) + ".df"),"rb")
	if fp==None:
		return None
	try:
		while(1):
			studList.append(f.load(fp))
	except:
		return studList
			



def writeDateData(club,date,studList):
	path = os.path.join(clubInfoStorage.location,"%s" % club.name,"attendance/dates")
	fp = openFile(path,(str(date.date()) + ".df"),"wb")
	for stud in studList:
		print("----")
		print(stud)
		print('---')
		f.dump(stud,fp,-1)
	
def searchObjectList(instance,objectList):
	
	#Searches for object in list of object and returns index
	i = 0
	
	try:
		while(1):
			if(instance.pk == objectList[i].student.pk):
				return i
			else:
				i+=1
	except:
		return -1 #Object has not been found
	
	

def addToMaster(path,fileName,studList):
	fp = openFile(path,fileName,"rb")
	
	studRecordList = []
	
	#for stud in studList:
	#	print(stud.firstName)
	
	try:
		
		while (1):
			
			studRecordList.append(f.load(fp))
					
	except EOFError:
		fp.close()
		fp = openFile(path,fileName,"wb")
		
		
		for stud in studRecordList:
			print(stud.student.firstName)
		print("-----------")
				
		
		for stud in studList:
			
			i = searchObjectList(stud,studRecordList)
			print(stud.firstName + " " +str(i))
			if i!=-1:
				studRecordList[i].incrementAttendance()
				print(studRecordList[i].student.firstName + " " + str(studRecordList[i].attendance))
			else:
 
				studRecordList.append(clubRecord(student = stud))
				print(stud.firstName)
				
	for stud in studRecordList:
		f.dump(stud,fp,-1)


class clubRecord(models.Model):
	
	student = models.ForeignKey(Student,on_delete=models.CASCADE)
	attendance = models.IntegerField(default=0)
	dues = models.FloatField(default=0)

	def incrementAttendance(self):
		self.attendance = self.attendance + 1
		print(self.attendance)		
	

		
	 
	
	

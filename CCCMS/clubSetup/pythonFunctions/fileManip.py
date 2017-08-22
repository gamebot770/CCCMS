import csv


def decode(code):
	
	isClubID = True
	clubID = ""
	attendance = ""
	
	
	for digit in code:

		#Comma separates the clubID from the attendance
		# | separates two datasets
		
		if digit=="," or digit=="|":
			isClubID = swapBoolean(isClubID)
			
			if digit=="|":
				
				print("Print clubID: ",clubID)
				print("Print Attendance: ",attendance)
				clubID = ""
				attendance = ""
				
			continue
			
		if isClubID == True:
			clubID = clubID + str(digit) #Reads all digits of a number in clubID
			
		else:
			attendance = attendance + str(digit)
			
	return

def swapBoolean(boolVar):
	
	#swapBoolean changes the true value of a boolean to false or vice versa
	
	if boolVar == True:
		boolVar = False
	else:
		boolVar=True
	return boolVar

def addClub(code,clubID,attendance):
	
	code = code + str(clubID) + "," + str(attendance) + "|"
	return code
	

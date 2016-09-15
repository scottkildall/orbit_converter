#! /user/bin/env python
import sys
import os
import datetime
import csv

# ProcessFiles() is the main entry point
def ProcessFiles():
	fileList = getInputFiles()
	
	for i in range(len(fileList)):
		if fileList[i].find(".txt") > -1:
			processEphemerisFile(fileList[i])
		else:
			print "Skipping file: " + fileList[i]

# returns a list of input files
def getInputFiles():
	fileList = os.listdir("input")

	# ideally weed out all non .txt files
	return fileList

# process a file, locate in the "input" directory (hardcoded)
def processEphemerisFile(filename):
	print "Processing file: " + filename

	fileText = getFileLines("input/" + filename)
	
	# extract Target Body Name [line 31]
	targetBodyName = extractTargetBodyName(fileText[30])
	print targetBodyName

	
	# extract Start Date [line 35]
	startDate = extractStartOrStopDate(fileText[34],"Start time      : A.D.")
	print startDate


	stopDate = extractStartOrStopDate(fileText[35],"Stop  time      : A.D.")
	print stopDate

	# line after the $$SOE

	csvOutputFileObj = openOutputCSVFile(targetBodyName + ".csv")

	## now iterate through many lines extract XYZ, add to CSV here
	lineIndex = 66 
	while lineIndex < len(fileText):
		#print fileText[lineIndex]
		if fileText[lineIndex].find("$$EOE") > -1:
			print "End data"
			break

		dateStr = extractDate(fileText[lineIndex],"= A.D.")
		#print dateStr
		if dateStr == False:
				print "Bad date: " + fileText[lineIndex]
				break

		lineIndex = lineIndex + 1
		xyzData = extractXYZData(fileText[lineIndex],[dateStr])
		#print xyzData

		csvOutputFileObj.writerow(xyzData)

		lineIndex = lineIndex + 3
		

	## now go line, by ine
	# add step size here??
	# Step-size       : 
#	startDT = datetime.datetime.strptime(startDate, "%Y-%b-%d" )
#	stopDT = datetime.datetime.strptime(stopDate, "%Y-%b-%d" )
	
#	dt = startDT
	
	# this will parse out all the dates, but we atually need to extract the x,y,z and put them into a CSV
#	while True:
#		print dt.strftime("%b %d, %Y")
#		dt =  dt + datetime.timedelta(days=1)
#		if dt == stopDT:
#		break



# Line in file looks something like this:
# Target body name: 26858 Misterrogers (1993 FR)
def extractTargetBodyName(line):
	targetBodyName = "001 Not Found"

	for i in range(0, len(line)):
		if line[i] == "(":
			targetBodyName = line[len("Target body name: "):i-1]
			break

	return targetBodyName

# Line in file looks something like this:
# Start time      : A.D. 2100-Jan-01 00:00:00.0000 TDB
def extractStartOrStopDate(line, searchStr):
	dateStr = False
	startIndex = -1
	endIndex = -1

	for i in range(0 + len(searchStr), len(line)):
		if line[i] == " ":

			if startIndex > 0:
				endIndex = i
				dateStr = line[startIndex:endIndex]
				break
			else:
				# first ' ' character
				startIndex = i+1


	# now dateStr = "2100-Jan-01" (or something like this), swap around to make "Jan 01 2001"
	#dateStr = dateStr[5:8] + " " + dateStr[9:11] + " " + dateStr[0:4] 
	return dateStr

# Line in file looks something like this:
# Start time      : A.D. 2100-Jan-01 00:00:00.0000 TDB
def extractDate(line, searchStr):
	dateStr = False
	startIndex = -1
	endIndex = -1
	spaceCount = 0

	for i in range(0 + len(searchStr), len(line)):
		if line[i] == " ":
			if spaceCount < 2:
				spaceCount = spaceCount + 1

			elif startIndex > 0:
				endIndex = i
				dateStr = line[startIndex:endIndex]
				break
			else:
				# first ' ' character
				startIndex = i+1


	# now dateStr = "2100-Jan-01" (or something like this), swap around to make "Jan 01 2001"
	#dateStr = dateStr[5:8] + " " + dateStr[9:11] + " " + dateStr[0:4] 
	return dateStr

def extractXYZData(xyzLine, xyzArr):
	#xyzArr = []

	startIndex = -1
	endIndex = -1
	
	numIndex = -1
	skipping = True
	

	## Clean this up
	for i in range(len(xyzLine)):
		#print str(ord(xyzLine[i])) + " " + xyzLine[i] + "| "

		if startIndex == -1 and xyzLine[i] != " ":
			#print "found startIndex"
			startIndex = i
		elif startIndex != -1 and xyzLine[i] == " ":
			#print str(float(xyzLine[startIndex:i]))
			xyzArr.append(float(xyzLine[startIndex:i]))
			startIndex = -1

	#print str(float(xyzLine[startIndex:len(xyzLine)]))
	xyzArr.append(float(xyzLine[startIndex:len(xyzLine)]))

		#print str(ord(xyzLine[i])) + " " + xyzLine[i] + "| "
		#if skipping == True and xyzLine[i] == " ":
		#	skipping = False
		#	startIndex = i
		#elif skipping == False and xyzLine[i] == " ":
		#	skipping = True
		#	endIndex = i
		#	print str(xyzLine[startIndex:endIndex])

	return xyzArr

def openOutputCSVFile(filename):
	print filename
	csvOutFileObj = False

	#with open("output/" + filename, 'wb') as csvfile:
	csvfile = open("output/" + filename, 'wb')
	csvOutFileObj = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
   	csvOutFileObj.writerow(["date", "x", "y", "z"])

	return csvOutFileObj

# makes an array from lines in a file, stripping off the newlines


def getFileLines(filename):
	f = open( filename, "r" )
	
	lines = f.readlines()
	arr = []
	for line in lines:
    		arr.append( line.rstrip('\n') )

	
	f.close()


	print len(arr)
	return arr


if __name__ == "__main__":
	ProcessFiles()

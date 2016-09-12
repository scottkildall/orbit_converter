#! /user/bin/env python
import sys
import os
import datetime


# ProcessFiles() is the main entry point
def ProcessFiles():
	fileList = getInputFiles()
	
	for i in range(len(fileList)):
		processEphemerisFile(fileList[i])

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

	## now iterate through many lines extract XYZ, add to CSV here
	lineIndex = 66 
	print fileText[lineIndex]
	dateStr = extractDate(fileText[lineIndex],"= A.D.")
	print dateStr
	
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
			targetBodyName = line[0:i-1]
			break

	return targetBodyName

# Line in file looks something like this:
# Start time      : A.D. 2100-Jan-01 00:00:00.0000 TDB
def extractStartOrStopDate(line, searchStr):
	dateStr = "002 Not Found"
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
	dateStr = "002 Not Found"
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

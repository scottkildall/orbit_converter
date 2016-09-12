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
	fileText = fileText[0]
	# this could be cleaned up so that it isn't a

	# look for Taget body name
	searchStr = "Target body name: "
	index = fileText.find(searchStr)
	if index > -1:
		targetBodyName = extractTargetBodyName(fileText, index, searchStr)
	
	searchStr = "Start time      : A.D."
	index = fileText.find(searchStr)
	if index > -1:
		startDate = extractStartOrStopDate(fileText, index, searchStr)
	
	searchStr = "Stop  time      : A.D."
	index = fileText.find(searchStr)
	if index > -1:
		stopDate = extractStartOrStopDate(fileText, index, searchStr)
	
	# add step size here??
	# Step-size       : 

	print targetBodyName
	print startDate
	print stopDate

# Line in file looks something like this:
# Target body name: 26858 Misterrogers (1993 FR)
def extractTargetBodyName(fileText, index, searchStr):
	targetBodyName = "001 Not Found"

	for i in range(index, len(fileText)):
		if fileText[i] == "(":
			targetBodyName = fileText[index:i-1]
			break

	return targetBodyName

# Line in file looks something like this:
# Start time      : A.D. 2100-Jan-01 00:00:00.0000 TDB
def extractStartOrStopDate(fileText, index, searchStr):
	dateStr = "002 Not Found"
	startIndex = -1
	endIndex = -1

	for i in range(index + len(searchStr), len(fileText)):
		if fileText[i] == " ":
			if startIndex > 0:
				endIndex = i
				dateStr = fileText[startIndex:endIndex]
				break
			else:
				# first ' ' character
				startIndex = i+1




	# now dateStr = "2100-Jan-01" (or something like this), swap around to make "Jan 01 2001"
	dateStr = dateStr[5:8] + " " + dateStr[9:11] + " " + dateStr[0:4] 
	return dateStr

# makes an array from lines in a file, stripping off the newlines
def getFileLines(filename):
	f = open( filename, "r" )
	arr = []
	for line in f:
    		arr.append( line.rstrip('\n') )
	f.close()

	return arr


if __name__ == "__main__":
	ProcessFiles()

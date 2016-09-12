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
	
	print targetBodyName

# Line in file looks something like this:
# Target body name: 26858 Misterrogers (1993 FR)
def extractTargetBodyName(fileText, index, searchStr):
	targetBodyName = "001 Not Found"

	for i in range(index, len(fileText)):
		if fileText[i] == "(":
			targetBodyName = fileText[index:i-1]
			break

	return targetBodyName

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

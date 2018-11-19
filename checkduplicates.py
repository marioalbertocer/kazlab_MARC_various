# This script checks if the fasta files (aligned or unaligned) in the current folder contain duplicates
# Place the script in your folder and run like ...
# python checkduplicates.py

import os

filesNumber = 0
duplicates = 0

for i in os.listdir("./"):
	if ".fas" in i:
		filesNumber += 1
		file = open(i , "r").readlines()
		tags = []
		for line in file:
			line = line.strip()
			if ">" in line : tags.append(line) 
		
		for line in file:
			countLine = 0 
			if ">" in line:
				line = line.strip()
				for tag in tags:
					if tag == line:
						countLine += 1

			if countLine > 1:
				duplicates += 1 
				print "%s\t%s\t" % (i, line)
				
			 
					
print "total number of files analyzed = " + str(filesNumber)
print "total number of duplicates = " + str(duplicates)

			

#!/usr/bin/python3

import csv
import sys

def writeentry(hFile, sName, sPhys, sLog):
	hFile.write("host %s {\n\thardware ethernet %s;\n\tfixed-address %s;\n}\n" % (sName, sPhys, sLog))

if __name__ == "__main__":
	if len(sys.argv) < 3:
		print("Not enough arguments: %s infile.csv outfile.conf [namecol] [maccol] [ipcol]" % (sys.argv[0]))
		exit()

	hInFile = None
	hOutFile = None
	iName = 0
	iPhysAddr = 2
	iLogAddr = 4
	try:
		hInFile = open(sys.argv[1], "r")
	except Exception as e:
		exit("Cannot open input file for reading: %s" % (e))
	try:
		hOutFile = open(sys.argv[2], "w")
	except Exception as e:
		hInFile.close()
		exit("Cannot open output file for writing: %s" % (e))


	try:
		iName = int(sys.argv[3])
		iPhysAddr = int(sys.argv[4])
		iLogAddr = int(sys.argv[5])
	except IndexError:
		pass
	except ValueError as e:
		hInFile.close()
		hOutFile.close()
		exit("Invalid column value: %s" % (e))

	oCSV = csv.reader(hInFile)
	next(oCSV)
	for lRow in oCSV:
		writeentry(hOutFile, lRow[iName], lRow[iPhysAddr], lRow[iLogAddr])
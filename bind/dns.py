#!/usr/bin/python3

import sys
import csv

def writeentry(hForFile, hRevFile, sDom, sAddr):
	if len(sDom) == 0 or len(sAddr) == 0:
		return
	hForFile.write("%s.	IN	A	%s\n" % (sDom, sAddr))
	hRevFile.write("%s	IN	PTR	%s.\n" % ('.'.join(sAddr.split('.')[::-1]) + ".in-addr.arpa.", sDom))

if __name__ == "__main__":
	if len(sys.argv) < 4:
		print("Not enough arguments: %s infile.csv for.domain.tld rev.domain.tld [domcol] [ipcol]" % (sys.argv[0]))
		exit()

	hInFile = None
	hForFile = None
	hRevFile = None
	iLogAddr = 4
	iDom = 6

	try:
		hInFile = open(sys.argv[1], "r")
	except Exception as e:
		exit("Cannot open input file for reading: %s" % (e))
	try:
		hForFile = open(sys.argv[2], "a")
	except Exception as e:
		hInFile.close()
		exit("Cannot open forward file for writing: %s" % (e))

	try:
		hRevFile = open(sys.argv[3], "a")
	except Exception as e:
		hInFile.close()
		hForFile.close()
		exit("Cannot open reverse file for writing: %s" % (e))

	try:
		iDom = int(sys.argv[4])
		iLogAddr = int(sys.argv[5])
	except IndexError:
		pass
	except ValueError as e:
		hInFile.close()
		hForFile.close()
		hRevFile.close()
		exit("Invalid column value: %s" % (e))

	oCSV = csv.reader(hInFile)
	next(oCSV)
	for lRow in oCSV:
		writeentry(hForFile, hRevFile, lRow[iDom], lRow[iLogAddr])
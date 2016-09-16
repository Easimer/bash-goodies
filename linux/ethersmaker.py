#!/usr/bin/python3

def readline(hFile):
	return hFile.readline().split(',')

lEntries = []

with open("src.csv") as hFile:
	nLen = 0
	bFirst = True
	while True:
		lRow = readline(hFile)
		print(lRow)
		if len(lRow) < 8:
			break
		else:
			if bFirst:
				bFirst = False
				continue
			else:
				lEntries.append((lRow[1], lRow[2]))
	print(lEntries)

with open("ethers", "w") as hFile:
	for tPair in lEntries:
		hFile.write("%s %s\n" % (tPair[0], tPair[1]))

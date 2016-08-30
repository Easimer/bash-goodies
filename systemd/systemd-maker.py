#!/usr/bin/python3

# Interactive SystemD Oneshot Service Unitfile Maker
# This program's output is NOT considered stable. Use at your own risk.

# Usage: systemd-maker.py outfile
# outfile cannot be '-'

import os
import sys

strDescription=""
strAfter=""
strBefore=""
strRequires=""
strRequisite=""
strWants=""
strExecStart=""
strAssertPath=[]
strWantedBy="multi-user.target"
strOnFailure=""

arrWantedChoices = [
	['When multi-user, text UI is used', 'multi-user.target'],
	['When graphical UI is used', 'graphical.target'],
	['When the system is in rescue mode', 'rescue.target'],
]

arrBeforeAfter = [
	['Local filesystems are mounted', 'local-fs.target'],
	['Remote filesystems are mounted', 'remote-fs.target'],
	['Network is available', 'network.target'],
	['There is a configured network device', 'network-online.target'],
	['A multi-user, text UI is activated', 'multi-user.target'],
	['A graphical UI is activated', 'graphical.target'],
]

def promptline(msg):
	try:
		return input(msg + ": ")
	except:
		exit("\nNo files were modified.")

def promptchoice(strMsg, arrChoices):
	print(strMsg)
	nChoicesLen = len(arrChoices)
	for i in range(nChoicesLen):
		print("[%d] %s (%s)" % (i + 1, arrChoices[i][0], arrChoices[i][1]))
	nChoice = int(promptline("Choice"))
	if nChoice <= nChoicesLen and nChoice > 0:
		return arrChoices[nChoice - 1][1]
	else:
		return promptchoice(strMsg, arrChoices)

def promptmcma(strMsg, arrChoices):
	arrAnswers = []
	arrNewChoices = [['Manual', 'manual'], ['Finish', 'finish']] + arrChoices
	while True:
		print("\x1b[2J\x1b[H")
		c = promptchoice("%s: %s" % (strMsg, ', '.join(arrAnswers)), arrNewChoices)
		if c == 'manual':
			c = promptline("Please enter")
		if c != 'finish':
			arrAnswers.append(c)
		else:
			return ' '.join(arrAnswers)

def swrite(hFile, strKey, strValue, bCheckLength=True):
	if len(strValue) == 0 and bCheckLength:
		return
	hFile.write("%s=%s\n" % (strKey, strValue))

def swritesec(hFile, strSection):
	hFile.write("[%s]\n" % strSection)

if __name__ == "__main__":

	print("Interactive SystemD Oneshot Service Unitfile Maker")
	print("This program's output is NOT considered stable. Use at your own risk.\n")

	if len(sys.argv) < 2:
		exit("Usage: %s outfile\n\toutfile cannot be '-'" % sys.argv[0])

	bAdvanced = False

	bAdvanced = promptline("Advanced mode? [y/N]").startswith('y')

	# description
	strDescription = promptline("Enter a description (Description)")
	strExecStart = promptline("Executable and arguments to call upon activation (ExecStart)")
	strBefore = promptmcma("Activate this service before (Before)", arrBeforeAfter)
	strAfter = promptmcma("Activate this service after (After)", arrBeforeAfter)
	strRequires = promptmcma("The service requires these and will try to activate them but if\none of them fails, this will too (Requires)", arrBeforeAfter)
	strOnFailure = promptmcma("The services to be activated when this fails (OnFailure)", arrBeforeAfter)
	if bAdvanced:
		strRequisite = promptmcma("The service will fail if atleast one of these is not already active (Requisite)", arrBeforeAfter)
		strWants = promptmcma("The service wants these and will try to activate them but won't fail\nif one of these fails (Wants)", arrBeforeAfter)
		while True:
			strLine = promptline("Check this path if it exists, fail if it doesn't (AssertPathExists) (empty line to skip)")
			if strLine == "":
				break
			else:
				strAssertPath.append(strLine)
		strWantedBy = promptmcma("The service's target/runlevel (WantedBy)", arrWantedChoices)

	with open(sys.argv[1], 'w') as hFile:
		swritesec(hFile, "Unit")
		swrite(hFile, "Description", strDescription)
		swrite(hFile, "Before", strBefore)
		swrite(hFile, "After", strAfter)
		swrite(hFile, "Requires", strRequires)
		swrite(hFile, "Requisite", strRequisite)
		swrite(hFile, "Wants", strWants)
		swrite(hFile, "OnFailure", strOnFailure)

		swritesec(hFile, "Service")
		swrite(hFile, "Type", "oneshot")
		swrite(hFile, "ExecStart", strExecStart)

		swritesec(hFile, "Install")
		swrite(hFile, "WantedBy", strWantedBy)
		
		for strPath in strAssertPath:
			swrite(hFile, "AssertPathExists", strPath)

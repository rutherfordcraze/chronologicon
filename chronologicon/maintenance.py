#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Chronologicon v4.x
# Rutherford Craze
# https://craze.co.uk
# 181103

import chronologicon, time

LOGS_FILENAME = chronologicon.LOGS_FILENAME
LOGS = chronologicon.LoadLogs()
PREFLIGHTS = True # False == Fail

if LOGS == False:
	print("Unable to load file: " + LOGS_FILENAME + ". Please ensure it exists.")
	PREFLIGHTS = False

def List(verbose = False):
	qty = 10
	columnTabs = [6, 20, 40, 60]

	if verbose:
		print("\n  Displaying all logs:\n")
		qty = len(LOGS)
	else:
		print("\n  Displaying " + str(qty) + " most recent logs:\n")

	totalLogs = len(LOGS)

	print(u"\u001b[37m  ID    Discipline    Project             Start               End\u001b[0m") # This is a catastrophically bad way of doing it

	for i in range(qty):
		logID = totalLogs - 1 - i
		line = str(logID) + "  "

		if len(line) < columnTabs[0]:
			line += " " * (columnTabs[0] - len(line))

		line += LOGS[logID]['DISC'] + "  "

		if len(line) < columnTabs[1]:
			line += " " * (columnTabs[1] - len(line))

		line += LOGS[totalLogs - 1 - i]['PROJ']

		if len(line) < columnTabs[2]:
			line += " " * (columnTabs[2] - len(line))

		line += time.strftime("%y/%m/%d %H:%M", time.localtime(LOGS[logID]['TIME_START']/1000))

		if len(line) < columnTabs[3]:
			line += " " * (columnTabs[3] - len(line))

		line += time.strftime("%y/%m/%d %H:%M", time.localtime(LOGS[logID]['TIME_END']/1000))

		print("  " + line)
	print(" ")


def Maintenance(args):
	if PREFLIGHTS == False:
		return

	verbose = False

	if 'verbose' in args:
		verbose = True

	if 'list' in args:
		PrintRecentLogs(verbose)
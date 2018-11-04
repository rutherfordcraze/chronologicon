#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Chronologicon v4.x
# Rutherford Craze
# https://craze.co.uk
# 181103

import chronologicon, operator

LOGS_FILENAME = chronologicon.LOGS_FILENAME
LOGS = chronologicon.LoadLogs()
PREFLIGHTS = True # False == Fail

if LOGS == False:
	print("Unable to load file: " + LOGS_FILENAME + ". Please ensure it exists.")
	PREFLIGHTS = False

def PrintRecentLogs(qty = 10, verbose = False):
	if PREFLIGHTS == False:
		return

	if verbose:
		qty = len(LOGS)

	totalLogs = len(LOGS)

	print("\nDisplaying " + str(qty) + " most recent logs:\n")

	for i in range(qty):
		line = str(i + 1) + "  "
		if i + 1 < 10:
			line += " "

		line += LOGS[totalLogs - 1 - i]['DISC'] + "  "

		if len(line) < 16:
			line += " " * (16 - len(line))

		line += LOGS[totalLogs - 1 - i]['PROJ']

		if LOGS[totalLogs - 1 - i]['XNOTE'] is not "":
			if len(line) < 30:
				line += " " * (30 - len(line))
			line += "  " + LOGS[totalLogs - 1 - i]['XNOTE']

		print(line)
	print("\n")
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Chronologicon v4.x
# Rutherford Craze
# https://craze.co.uk
# 181103

import chronologicon, time, os, json
from datetime import datetime
from  chronologicon.strings import *

PREFS = chronologicon.PREFS
LOGS_FILENAME = chronologicon.LOGS_FILENAME
LOGS = chronologicon.LoadLogs()

SYN_DISC = ['discipline', 'disc', 'sector']
SYN_PROJ = ['project', 'proj']

SYN_TIME_START = ['start', 'start_time', 'time_start']
SYN_TIME_END = ['end', 'end_time', 'time_end']

def List(verbose = False):
	qty = 10
	columnTabs = [6, 20, 40, 60]

	if LOGS == False:
		Message('maintLogsFileNotFound','',LOGS_FILENAME)
		return

	totalLogs = len(LOGS)

	if totalLogs < qty or verbose:
		Message('maintAllLogsTitle')
		qty = totalLogs
	else:
		Message('maintRecentLogsTitle', '', qty)

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

def Edit(logID = None, attribute = None, newValue = None):
	logToEdit = LOGS[int(logID)]

	if attribute in SYN_DISC:
		logToEdit['DISC'] = newValue
		ApplyEdit(logID, logToEdit)

	elif attribute in SYN_PROJ:
		logToEdit['PROJ'] = newValue
		ApplyEdit(logID, logToEdit)

	elif attribute in SYN_TIME_START:
		try:
			dt = datetime.strptime(str(newValue), '%y/%m/%d %H:%M')
			ms = int(time.mktime(dt.timetuple()) * 1000)
			logToEdit['TIME_START'] = ms
			logToEdit['TIME_LENGTH'] = int((logToEdit['TIME_END'] - ms) / 1000)
			ApplyEdit(logID, logToEdit)
		except Exception as e:
			Message('maintStartEditFailed', e)

	elif attribute in SYN_TIME_END:
		try:
			dt = datetime.strptime(str(newValue), '%y/%m/%d %H:%M')
			ms = int(time.mktime(dt.timetuple()) * 1000)
			logToEdit['TIME_END'] = ms
			logToEdit['TIME_LENGTH'] = int((ms - logToEdit['TIME_START']) / 1000)
			ApplyEdit(logID, logToEdit)
		except Exception as e:
			Message('maintStartEditFailed', e)

	else:
		Message('maintUnrecognisedAttribute')

def ApplyEdit(logID, newValue):
	LOGS[int(logID)] = newValue
	PersistLogs()

def Remove(logID = None):
	del LOGS[int(logID)]
	PersistLogs()

def PersistLogs():
	try:
		# Write logs to logs file
		with open(os.path.join(PREFS.get('SAVE_DIR'), LOGS_FILENAME), 'w') as LOGS_FILE:
			LOGS_FILE.write(json.dumps(LOGS, indent=4))

		Message('maintEditSuccess')
	except Exception as e:
		Message('maintEditFailure', e)

#!/usr/bin/env python3

# Chronologicon v4.0
# "The Command Line One"
# Rutherford Craze
# https://craze.co.uk
# 181020

import json, os, time

LOGS_FILENAME = 'data/logs.json'
STATS_FILENAME = 'data/stat.json'
PRESAVE_FILENAME = 'data/presave.json'

LOGS_DEFAULT = []

CUR_LOG = {
	'TIME_START':0,
	'TIME_END':0,
	'TIME_LENGTH':0,

	'DISC':"",
	'PROJ':"",
	'XNOTE':""
	}
CUR_STATS = {
	'discByTime':{},
	'projByTime':{},
	'projByDisc':{},
	'workByHour':{},
	'avgLogLength':0,
	'totalLogs':0,
	'totalTime':0
	}



# --CORE-FUNCTIONS----------------------------------

# Any mission-critical components should be checked/ created before starting
def Preflights():
	# Check if log file exists; create it (and its parent folder) if it doesn't
	try:
		with open(LOGS_FILENAME, 'r') as LOGS_FILE:
			return True
	except:
		print("Logs file not found. Creating...")
		os.makedirs(os.path.dirname(LOGS_FILENAME), exist_ok=True)
		try:
			with open(LOGS_FILENAME, "w") as LOGS_FILE:
				LOGS_FILE.write(json.dumps(LOGS_DEFAULT))
			return True
		except:
			print("Unable to create log file. Please check your install.")
			return False



# Start a new log and save its initial parameters to the presave file
def StartLog(args):
	if len(args) < 2:
		print("Not enough information to start a new log.\nUsage: '$ chron -s <discipline> <project> <optional_note>'")
	else:
		# Abort if there's already a log running
		if(os.path.getsize(PRESAVE_FILENAME) > 10):
			print("Log already in progress.")
			return

		CUR_LOG['TIME_START'] = int(time.time() * 1000)
		CUR_LOG['DISC'] = args[0]
		CUR_LOG['PROJ'] = args[1]
		if len(args) > 2:
			CUR_LOG['XNOTE'] = args[2]

		try:
			with open(PRESAVE_FILENAME, 'w+') as PRESAVE_FILE:
				PRESAVE_FILE.write(json.dumps(CUR_LOG))
		except:
			print("Unable to start log.")
			return

		print("Started new log with discipline '" + CUR_LOG['DISC'] + "' and project '" + CUR_LOG['PROJ'] + "'.")

# Cancel an in-progress log and reset the presave file
def CancelLog(quietly=False):
	try:
		with open(PRESAVE_FILENAME, 'w') as PRESAVE_FILE:
			PRESAVE_FILE.write("")
	except:
		print("Error ending previous log.")
		return

	if quietly is not True:
		print("Log cancelled.")

# Record the current log and clear the presave file
def StopLog():
	try:
		with open(PRESAVE_FILENAME) as PRESAVE_FILE:
			CUR_LOG = json.load(PRESAVE_FILE)
	except:
		print("No log in progress.")
		return

	CUR_LOG['TIME_END'] = int(time.time() * 1000)
	CUR_LOG['TIME_LENGTH'] = CUR_LOG['TIME_END'] - CUR_LOG['TIME_START']
	seconds = str(CUR_LOG['TIME_LENGTH'] // 1000)

	try:
		with open(LOGS_FILENAME, 'rb+') as LOGS_FILE:
			LOGS_FILE.seek(-1, os.SEEK_END)
			LOGS_FILE.truncate()

		with open(LOGS_FILENAME, 'a') as LOGS_FILE:
			if(os.path.getsize(LOGS_FILENAME) > 10):
				LOGS_FILE.write(',')
			LOGS_FILE.write('\n' + json.dumps(CUR_LOG) + ']')

		CancelLog(True)

		if seconds == '1':
			print("Log complete. Tracked " + seconds + " second.")
		else:
			print("Log complete. Tracked " + seconds + " seconds.")

		SaveStats()

	except:
		print("Unable to save log. Please try again or check your install.")

# Create/ overwrite stats file with info from all logs
def SaveStats():
	try:
		# Read/ generate stats from logs file
		with open(LOGS_FILENAME) as LOGS_FILE:
			LOGS = json.load(LOGS_FILE)
			for log in range(len(LOGS)):
				thisLog = LOGS[log]

				# Total logs
				CUR_STATS['totalLogs'] = len(LOGS)

				# Total ms tracked
				CUR_STATS['totalTime'] += thisLog['TIME_LENGTH']

				# Average log duration
				CUR_STATS['avgLogLength'] = CUR_STATS['totalTime'] // CUR_STATS['totalLogs']

				# Disciplines by time
				CUR_STATS['discByTime'][thisLog['DISC']] = CUR_STATS['discByTime'].get(thisLog['DISC'], 0) + thisLog['TIME_LENGTH']

				# Projects by time
				CUR_STATS['projByTime'][thisLog['PROJ']] = CUR_STATS['projByTime'].get(thisLog['PROJ'], 0) + thisLog['TIME_LENGTH']

				# Projects-by-discipline breakdown assignment
				CUR_STATS['projByDisc'][thisLog['PROJ']] = CUR_STATS['projByDisc'].get(thisLog['PROJ'], dict())
				CUR_STATS['projByDisc'][thisLog['PROJ']][thisLog['DISC']] = CUR_STATS['projByDisc'][thisLog['PROJ']].get(thisLog['DISC'], 0) + thisLog['TIME_LENGTH']

				# Productivity by hour
				logHour = time.strftime("%H", time.localtime(thisLog['TIME_START']/1000))
				CUR_STATS['workByHour'][logHour] = CUR_STATS['workByHour'].get(logHour, 0) + 1

		# Write statistics to stats file
		with open(STATS_FILENAME, 'w') as STATS_FILE:
			STATS_FILE.write('[' + json.dumps(CUR_STATS) + ']')
	except:
		print("Unable to update statistics file.")

def Backup():
	try:
		with open(LOGS_FILENAME) as LOGS_FILE:
			with open('data/chron_backup-' + time.strftime("%y%m%d_%H%M", time.localtime()) + '.json', 'w') as BACKUP_FILE:
				BACKUP_FILE.write(LOGS_FILE.read())
		print("Log file backed up.")
	except:
		print("Unable to back up logs.")
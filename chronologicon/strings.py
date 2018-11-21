#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Chronologicon v4.x
# Rutherford Craze
# https://craze.co.uk
# 181119

HELP_TEXT = """
Usage:
	chron <command> <options>

Commands:
	start <options>				 Start a new log timer.
	stop										Complete the current log.
	status									Check whether a log is in progress.
	cancel									Abort the current entry.
	stats <options>				 View stats & graphs.
	list										Show the 10 most recent logs.
	backup									Backup the log data file.
	edit <options>					Edit an attribute of a specific log.
	remove <options>			 Remove a specific log entry.
	directory <options>		 Change the save directory.

For detailed usage:
	https://github.com/rutherfordcraze/chronologicon
"""

STRINGS = {
	'cTestMessage':									'Chron Test Message',
	'chronHelp':										HELP_TEXT,
	'chronLogAbortCancelled':				'Log not cancelled.',
	'chronEditInputInvalid':				'Unexpected input. Usage:\n$ chron edit <logID> <attribute> <newValue>',
	'chronRemoveInputInvalid':			'Unexpected input. Usage:\n$ chron remove <logID>',
	'chronUnrecognisedCommand':			'Command not recognised.',
	'chronNotEnoughArguments':			'Not enough arguments.\n' + HELP_TEXT,
	'chronOldPythonVersion':				'You are running Chronologicon on python #x. This version will not be supported in future.',
	'maintLogsFileNotFound':				'Unable to load file: #x. Please ensure it exists.',
	'maintStartEditFailed':					'Start time could not be edited.',
	'maintEndEditFailed':						'End time could not be edited.',
	'maintUnrecognisedAttribute':		'Attribute not recognised.',
	'maintEditSuccess':							'Log edited.',
	'maintEditFailure':							'"Unable to update logs file.',
	'maintAllLogsTitle':						'\n  Displaying all logs:\n',
	'maintRecentLogsTitle':					'\n  Displaying #x most recent logs:\n'
}

def Message(msg, e = '', extra = ''):
	msg = STRINGS[msg]
	if extra != '':
		msg = msg.replace('#x', str(extra))
	print(msg)
	if e != '':
		print(str(e))

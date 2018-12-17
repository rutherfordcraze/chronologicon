# -*- coding: utf-8 -*-

# Chronologicon v5.x
# Rutherford Craze
# https://craze.co.uk
# 181119

HELP_TEXT = """
Usage:
    chron <command> <options>

Commands:
    start <options>         Start a new log timer.
    stop                    Complete the current log.
    status                  Check whether a log is in progress.
    cancel                  Abort the current entry.
    stats <options>         View stats & graphs.
    list                    Show the 10 most recent logs.
    backup                  Backup the log data file.
    edit <options>          Edit an attribute of a specific log.
    directory <options>     Change the save directory.

For detailed usage:
    https://github.com/rutherfordcraze/chronologicon
"""

STRINGS = {
    'chronHelp':                        HELP_TEXT,
    'chronLogAbortCancelled':           'Log not cancelled.',
    'chronEditInputInvalid':            'Unexpected input. Usage:\n$ chron edit <logID> <attribute> <newValue>',
    'chronRemoveInputInvalid':          'Unexpected input. Usage:\n$ chron remove <logID>',
    'chronUnrecognisedCommand':         'Command not recognised.',
    'chronNotEnoughArguments':          'Not enough arguments.\n' + HELP_TEXT,
    'chronOldPythonVersion':            'You are running Chronologicon on python #x. This version will not be supported in future.',

    'maintLogsFileNotFound':            'Unable to load file: #x. Please ensure it exists.',
    'maintStartEditFailed':             'Start time could not be edited.',
    'maintEndEditFailed':               'End time could not be edited.',
    'maintUnrecognisedAttribute':       'Attribute not recognised.',
    'maintEditSuccess':                 'Log edited.',
    'maintEditFailure':                 '"Unable to update logs file.',
    'maintAllLogsTitle':                '\n  Displaying all logs:\n',
    'maintRecentLogsTitle':             '\n  Displaying #x most recent logs:\n',

    'inputSaveDirUpdated':              'Save directory updated.',
    'inputBackupComplete':              'Logs file backed up.',
    'inputBackupFailed':                'Unable to back up logs.',
    'inputNoCurrentLog':                'No log in progress.',
    'inputLogInProgress':               'Log in progress: #x.',
    'inputTimeElapsed':                 'Current duration: #x seconds.',
    'inputLogAborted':                  'Log cancelled.',
    'inputLogAbortFailed':              'Unable to cancel the current log.',
    'inputStatsUpdateFailed':           'Unable to update stats file.',
    'inputLogCompletionFailed':         'Unable to save log. Please try again or check your install.',
    'inputLogCompleteSingular':         'Log complete. Tracked #x second.',
    'inputLogCompletePlural':           'Log complete. Tracked #x seconds.',
    'inputStartNotEnoughArguments':     'Not enough information to start a new log.\nUsage: \'$ chron -s <discipline> <project> <optional_note>\'',
    'inputLogAlreadyInProgress':        'Log already in progress.',
    'inputNoPresaveFile':               'Unable to load temp file. If this is your first log, please ignore this message.',
    'inputLogStartFailed':              'Unable to start log.',
    'inputLogStarted':                  'Started new log: #x.',
    'inputMigrationFailed':             'Unable to migrate logs file.',
    'inputMigrationComplete':           'Migration complete.',

    'initSaveDirNotVerified':           'Save directory could not be verified. Please use the \'$ chron directory\' command to set a new one.',
    'initSaveDirNotSet':                'No save directory specified. Please use the \'$ chron directory\' command to set one.',
    'initCreatingLogsFile':             'Creating logs file...',
    'initCreatingStatsFile':            'Creating stats file...',
    'initCreatingTempFile':             'Creating temporary save file...',
    'initCreateLogFileFailed':          'Unable to create logs file. Please check your install.',
    'initCreateStatsFileFailed':        'Unable to create stats file. Please check your install.',
    'initCreateTempFileFailed':         'Unable to create temporary save file. Please check your install.',
    'initVersionCheckFailed':           'Unable to check logs file version.',
    'initLogsOutdated':                 'Logs file was saved using an old version. Backing up and migrating to the latest version...',

    'outputLoadStatsFailed':            'Unable to load file: #x. Please ensure it exists.',
    'outputLoadLogsFailed':            'Unable to load file: #x. Please ensure it exists.'
}

def Message(msg, e=None, extra=None):
    msg = STRINGS[msg]
    if extra:
        msg = msg.replace('#x', str(extra))
    print(msg)
    if e:
        print(str(e))

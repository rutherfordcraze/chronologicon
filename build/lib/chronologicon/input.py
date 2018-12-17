# -*- coding: utf-8 -*-

# Chronologicon v5.x
# Rutherford Craze
# https://craze.co.uk
# 181123

import json, os, time
from datetime import datetime
from easysettings import EasySettings
from chronologicon.strings import *

LOGS_FILENAME = 'logs.json'
STATS_FILENAME = 'stat.json'
PRESAVE_FILENAME = 'temp.json'
BACKUPS_DIRNAME = '/Backups/'
TIME_FORMAT = '%y/%m/%d %H:%M:%S'

LOGS_DEFAULT = []

CUR_FILEPATH = os.path.dirname(__file__)
CUR_LOG = {
    'TIME_START': '',
    'TIME_END': '',
    'TIME_LENGTH': 0,

    'DISC': "",
    'PROJ': "",
    'XNOTE': ""
    }
CUR_STATS = {
    'discbytime': {},
    'projbytime': {},
    'projbydisc': {},
    'workbyhour': {},
    'avgloglength': 0,
    'totallogs': 0,
    'totaltime': 0
    }

PREFS = EasySettings(os.path.join(CUR_FILEPATH, 'prefs.conf'))

# Used by Output
def LoadStats():
    try:
        # Load statistics from stats file
        with open(os.path.join(PREFS.get('SAVE_DIR'), STATS_FILENAME), 'r') as STATS_FILE:
            CUR_STATS = json.load(STATS_FILE)
            return CUR_STATS
    except:
        return False

# Used by Maintenance
def LoadLogs():
    try:
        # Load logs from logs file
        with open(os.path.join(PREFS.get('SAVE_DIR'), LOGS_FILENAME), 'r') as LOGS_FILE:
            CUR_LOGS = json.load(LOGS_FILE)
            return CUR_LOGS
    except:
        return False

# Update the save directory preferences
def ChangeSaveDir(newSaveDir):
    global PREFS
    PREFS.setsave('SAVE_DIR', os.path.expanduser(newSaveDir))
    PREFS.setsave('BACKUP_DIR', os.path.expanduser(os.path.join(newSaveDir + BACKUPS_DIRNAME)))
    Message('inputSaveDirUpdated')

# Create a copy of the logs file in a specified directory; return true if it worked and false if it didn't
def Backup():
    # Check that a backup directory is set
    if not PREFS.has_option('BACKUP_DIR'):
        PREFS.setsave('BACKUP_DIR', os.path.join(PREFS.get('SAVE_DIR') + BACKUPS_DIRNAME))

    try:
        if not os.path.exists(PREFS.get('BACKUP_DIR')):
            os.makedirs(PREFS.get('BACKUP_DIR'))
        with open(os.path.join(PREFS.get('SAVE_DIR'), LOGS_FILENAME)) as LOGS_FILE:
            with open(os.path.join(PREFS.get('BACKUP_DIR'), 'chron_backup-' + time.strftime("%y%m%d_%H%M", time.localtime()) + '.json'), 'w') as BACKUP_FILE:
                BACKUP_FILE.write(LOGS_FILE.read())
        Message('inputBackupComplete')
        return True
    except Exception as e:
        Message('inputBackupFailed', e)
        return False

# Display any in-progress logs
def Status():
    try:
        with open(os.path.join(CUR_FILEPATH, PRESAVE_FILENAME)) as PRESAVE_FILE:
            CUR_LOG = json.load(PRESAVE_FILE)
            Message('inputLogInProgress', '', CUR_LOG['DISC'] + ', ' + CUR_LOG['PROJ'])

            delta = datetime.now() - datetime.strptime(CUR_LOG['TIME_START'], TIME_FORMAT)
            seconds = str(delta.seconds)
            Message('inputTimeElapsed', '', seconds)
    except:
        Message('inputNoCurrentLog')

# Cancel an in-progress log and reset the presave file
def CancelLog(quietly=False):
    try:
        with open(os.path.join(CUR_FILEPATH, PRESAVE_FILENAME), 'w') as PRESAVE_FILE:
            PRESAVE_FILE.write('')
    except Exception as e:
        Message('inputLogAbortFailed', e)
        return

    if not quietly:
        Message('inputLogAborted')

# Create/ overwrite stats file with info from all logs
def SaveStats():
    try:
        # Read/ generate stats from logs file
        with open(os.path.join(PREFS.get('SAVE_DIR'), LOGS_FILENAME)) as LOGS_FILE:
            LOGS = json.load(LOGS_FILE)
            for log in range(len(LOGS)):
                thisLog = LOGS[log]

                # Total logs
                CUR_STATS['totallogs'] = len(LOGS)

                # Total ms tracked
                CUR_STATS['totaltime'] += thisLog['TIME_LENGTH']

                # Average log duration
                CUR_STATS['avgloglength'] = CUR_STATS['totaltime'] // CUR_STATS['totallogs']

                # Disciplines by time
                CUR_STATS['discbytime'][thisLog['DISC']] = CUR_STATS['discbytime'].get(thisLog['DISC'], 0) + thisLog['TIME_LENGTH']

                # Projects by time
                CUR_STATS['projbytime'][thisLog['PROJ']] = CUR_STATS['projbytime'].get(thisLog['PROJ'], 0) + thisLog['TIME_LENGTH']

                # Projects-by-discipline breakdown assignment
                CUR_STATS['projbydisc'][thisLog['PROJ']] = CUR_STATS['projbydisc'].get(thisLog['PROJ'], dict())
                CUR_STATS['projbydisc'][thisLog['PROJ']][thisLog['DISC']] = CUR_STATS['projbydisc'][thisLog['PROJ']].get(thisLog['DISC'], 0) + thisLog['TIME_LENGTH']

                # Productivity by hour (maybe outdated)
                if thisLog['TIME_LENGTH'] < 3601: # Simple entry for single-hour logs
                    logHour = str(datetime.strptime(thisLog['TIME_START'], TIME_FORMAT).hour).zfill(2)
                    CUR_STATS['workbyhour'][logHour] = CUR_STATS['workbyhour'].get(logHour, 0) + 1
                else:
                    logHour = str(datetime.strptime(thisLog['TIME_START'], TIME_FORMAT).hour).zfill(2)
                    for h in range((thisLog['TIME_LENGTH'] // 3600) + 1): # For multi-hour logs, log all hours covered
                        logHour = str(int(logHour) + 1).zfill(2)
                        if int(logHour) > 23:
                            logHour = '00'
                        CUR_STATS['workbyhour'][logHour] = CUR_STATS['workbyhour'].get(logHour, 0) + 1

        # Write statistics to stats file
        with open(os.path.join(PREFS.get('SAVE_DIR'), STATS_FILENAME), 'w') as STATS_FILE:
            STATS_FILE.write('[' + json.dumps(CUR_STATS, indent=4).lower() + ']')
    except Exception as e:
        Message('inputStatsUpdateFailed', e)


# Start a new log and save its initial parameters to the presave file
def StartLog(args):
    if len(args) < 2:
        Message('inputNotEnoughArguments')
    else:
        try:
            # Abort if there's already a log running
            if os.path.getsize(os.path.join(CUR_FILEPATH, PRESAVE_FILENAME)) > 10:
                Message('inputLogAlreadyInProgress')
                return
        except:
            Message('inputNoPresaveFile')

        #CUR_LOG['TIME_START'] = int(time.time() * 1000)
        CUR_LOG['TIME_START'] = time.strftime(TIME_FORMAT, time.localtime(time.time()))
        CUR_LOG['DISC'] = args[0]
        CUR_LOG['PROJ'] = args[1]
        if len(args) > 2:
            CUR_LOG['XNOTE'] = args[2]

        try:
            with open(os.path.join(CUR_FILEPATH, PRESAVE_FILENAME), 'w+') as PRESAVE_FILE:
                PRESAVE_FILE.write(json.dumps(CUR_LOG))
        except Exception as  e:
            Message('inputLogStartFailed', e)
            return

        Message('inputLogStarted', '', CUR_LOG['DISC'] + ', ' + CUR_LOG['PROJ'])


# Record the current log and clear the presave file
def StopLog():
    try:
        with open(os.path.join(CUR_FILEPATH, PRESAVE_FILENAME)) as PRESAVE_FILE:
            CUR_LOG = json.load(PRESAVE_FILE)
    except Exception as e:
        Message('inputNoCurrentLog')
        return

    CUR_LOG['TIME_END'] = time.strftime(TIME_FORMAT, time.localtime(time.time()))

    delta = datetime.strptime(CUR_LOG['TIME_END'], TIME_FORMAT) - datetime.strptime(CUR_LOG['TIME_START'], TIME_FORMAT)
    CUR_LOG['TIME_LENGTH'] = delta.seconds
    seconds = str(CUR_LOG['TIME_LENGTH'])

    try:
        ALL_LOGS = None

        # Open the logs file, read its contents, close it
        with open(os.path.join(PREFS.get('SAVE_DIR'), LOGS_FILENAME), 'r') as LOGS_FILE:
            ALL_LOGS = json.load(LOGS_FILE)

        ALL_LOGS.append(CUR_LOG)

        # Open logs file, insert new contents, close it
        with open(os.path.join(PREFS.get('SAVE_DIR'), LOGS_FILENAME), 'w') as LOGS_FILE:
            LOGS_FILE.write(json.dumps(ALL_LOGS, indent=4))

        CancelLog(True)

        if seconds == '1':
            Message('inputLogCompleteSingular', '', seconds)
        else:
            Message('inputLogCompletePlural', '', seconds)

        SaveStats()

    except Exception as e:
        Message('inputLogCompletionFailed', e)

# Migrate logs from v4.x to v5.x
def MigrateLogs():
    # Make sure file is backed up first
    if Backup():
        try:
            ALL_LOGS = []
            with open(os.path.join(PREFS.get('SAVE_DIR'), LOGS_FILENAME), "r") as LOGS_FILE_OLD:
                ALL_LOGS = json.load(LOGS_FILE_OLD)
                for log in ALL_LOGS:
                    startTimeFormatted = time.strftime(TIME_FORMAT, time.localtime(log['TIME_START']/1000))
                    endTimeFormatted = time.strftime(TIME_FORMAT, time.localtime(log['TIME_END']/1000))

                    log['TIME_START'] = startTimeFormatted
                    log['TIME_END'] = endTimeFormatted

            with open(os.path.join(PREFS.get('SAVE_DIR'), LOGS_FILENAME), "w") as LOGS_FILE:
                LOGS_FILE.write(json.dumps(ALL_LOGS, indent=4))

            Message('inputMigrationComplete')
        except Exception as e:
            Message('inputMigrationFailed', e)

# -*- coding: utf-8 -*-

# Chronologicon v5.x
# Rutherford Craze
# https://craze.co.uk
# 181028

import json
import os
import chronologicon.input
from easysettings import EasySettings
from chronologicon.strings import *

LOGS_FILENAME = 'logs.json'
STATS_FILENAME = 'stat.json'
PRESAVE_FILENAME = 'temp.json'

LOGS_DEFAULT = []

CUR_FILEPATH = os.path.dirname(__file__)
PREFS = EasySettings(os.path.join(CUR_FILEPATH, 'prefs.conf'))


# Logs version check
try:
    LOGS = ''
    with open(os.path.join(PREFS.get('SAVE_DIR'), LOGS_FILENAME), "r") as LOGS_FILE:
        LOGS = json.load(LOGS_FILE)

    if type(LOGS[0]['TIME_START']) is int:
        Message('initLogsOutdated')
        input.MigrateLogs()
except Exception as e:
    Message('initVersionCheckFailed', e)


# Check any mission-critical files and create missing ones.
def Preflights():
    global PREFS

    # Check save directory
    if PREFS.has_option('SAVE_DIR'):
        if os.path.isdir(PREFS.get('SAVE_DIR')):
            pass
        else:
            Message('initSaveDirNotVerified')
            return False
    else:
        Message('initSaveDirNotSet')
        return False

    # Check logs file
    if os.path.exists(os.path.join(PREFS.get('SAVE_DIR'), LOGS_FILENAME)):
        pass
    else:
        Message('initCreatingLogsFile')
        try:
            # os.makedirs(os.path.dirname(LOGS_FILENAME), exist_ok=True)
            with open(os.path.join(PREFS.get('SAVE_DIR'), LOGS_FILENAME), "w") as LOGS_FILE:
                LOGS_FILE.write(json.dumps(LOGS_DEFAULT))
        except Exception as e:
            Message('initCreateLogFileFailed', e)
            return False

    # Check stats file
    if os.path.exists(os.path.join(PREFS.get('SAVE_DIR'), STATS_FILENAME)):
        pass
    else:
        Message('initCreatingStatsFile')
        try:
            # os.makedirs(os.path.dirname(LOGS_FILENAME), exist_ok=True)
            with open(os.path.join(PREFS.get('SAVE_DIR'), STATS_FILENAME), "w") as STATS_FILE:
                pass
        except Exception as e:
            Message('initCreateStatsFileFailed', e)
            return False

    # Check temp file
    if os.path.exists(os.path.join(CUR_FILEPATH, PRESAVE_FILENAME)):
        pass
    else:
        Message('initCreatingTempFile')
        try:
            with open(os.path.join(CUR_FILEPATH, PRESAVE_FILENAME), "w") as PRESAVE_FILE:
                pass
        except Exception as e:
            Message('initCreateTempFileFailed', e)
            return False

    return True

 # -*- coding: utf-8 -*-

# Chronologicon v5.x
# Rutherford Craze
# https://craze.co.uk
# 181028

import operator
import datetime
import chronologicon
from chronologicon.terminalsize import get_terminal_size
from chronologicon.strings import Message

STATS_FILENAME = chronologicon.STATS_FILENAME
STATS = {}
LOGS_FILENAME = chronologicon.LOGS_FILENAME
LOGS = {}
TERM_WIDTH = get_terminal_size()[0]
BAR_WIDTH = TERM_WIDTH - 4
MVP_DISC = []

# Console colour ANSI escapes
class colors:
    RED = u"\u001b[31m"
    BLUE = u"\u001b[34m"
    GREY = u"\u001b[37m"
    RESET = u"\u001b[0m"
    DEBUG = u"\u001b[35m"

class bars:
    SINGLE = u"\u2588"
    DOUBLE = u"\u2590\u258C"
    SHORTDOUBLE = u"\u2597\u2596"

def GetDbt(byProject = None, graphWidth = BAR_WIDTH):
    global MVP_DISC

    if byProject is None:
        dbt = sorted(STATS['discbytime'].items(), key=operator.itemgetter(1))
    else:
        dbt = sorted(STATS['projbydisc'][byProject].items(), key=operator.itemgetter(1))
    dbtGraph = "  "
    dbtKey = "  "
    R = 0;

    for discipline in range(len(dbt)):
        if discipline < 3:
            k = dbt[len(dbt) - 1 - discipline][0]
            v = dbt[len(dbt) - 1 - discipline][1]
            MVP_DISC.append(str(k))

            if byProject is None:
                bar = int(float(v) / float(STATS['totaltime']) * graphWidth)
            else:
                bar = int(float(v) / float(STATS['projbytime'][byProject]) * graphWidth)

            R += bar

            if MVP_DISC[0] == k:
                dbtGraph += (bar * bars.SINGLE)
                dbtKey += str(k).capitalize() + "  "
            elif len(MVP_DISC) > 1 and MVP_DISC[1] == k:
                dbtGraph += colors.RED + (bar * bars.SINGLE) + colors.RESET
                dbtKey += colors.RED + str(k).capitalize() + colors.RESET + "  "
            elif len(MVP_DISC) > 2 and MVP_DISC[2] == k:
                dbtGraph += colors.BLUE + (bar * bars.SINGLE) + colors.RESET
                dbtKey += colors.BLUE + str(k).capitalize() + colors.RESET + "  "
            else:
                R -= bar # Ignore 'other' stuff for now, put it at the end

    if R < graphWidth:
        dbtGraph += colors.GREY + ((graphWidth - R) * bars.SINGLE) + colors.RESET
        dbtKey += colors.GREY + "Other" + colors.RESET

    return (dbtGraph, dbtKey)

def GetWbh():
    height = 6
    maxValue = max(STATS['workbyhour'].items(), key=operator.itemgetter(1))[1]
    wbh = sorted(STATS['workbyhour'].items())
    wbhClamped = []
    wbhGraph = "  | "
    wbhKey = "  | "

    c = 0
    for hour in range(24):
        if c < len(wbh):
            if wbh[c][0] == str(hour).zfill(2):
                wbhClamped.append(int(float(wbh[c][1]) / float(maxValue) * height))
                c += 1
            else:
                wbhClamped.append(0)
        else: wbhClamped.append(0)

    for row in range(height):
        if row > 0:
            wbhGraph += "\n  | "
        for col in range(len(wbhClamped)):
            if wbhClamped[col] >= height - row:
                wbhGraph += bars.DOUBLE
            else:
                wbhGraph += colors.GREY + "··" + colors.RESET

    for col in range(0, len(wbhClamped), 3):
        wbhKey += str(col).zfill(2) + '    '

    return(wbhGraph, wbhKey)

def GetPbt(verbose = False, uniform = False):
    if verbose == False:
        projects = 5
    else:
        projects = len(STATS['projbytime'])

    graphWidth = BAR_WIDTH;
    pbt = sorted(STATS['projbytime'].items(), key=operator.itemgetter(1))
    maxValue = max(STATS['projbytime'].items(), key=operator.itemgetter(1))[1]
    pbtList = ""

    for project in range(len(pbt)):
        if project < projects:
            k = pbt[len(pbt) - 1 - project][0]

            # Skip blank project names
            if k == '':
                continue

            v = pbt[len(pbt) - 1 - project][1]
            spacer = BAR_WIDTH - len(k) - len(str(v)) + 1

            if uniform:
                pBarWidth = graphWidth
            else:
                pBarWidth = int(float(v) / float(maxValue) * graphWidth)

            # Skip zero-width graph bars
            if pBarWidth < 1:
                continue

            dbtGraph, dbtKey = GetDbt(k, pBarWidth)

            pbtList += dbtGraph + "\n"
            label =  str(int(v / 60 / 60)) + colors.GREY + " H" + colors.RESET
            labelString = "  " + str(k).capitalize()

            # Add 11 to compensate for left padding and the ansi colour code
            labelString += " " * (BAR_WIDTH - len(labelString) - len(label) + 11)
            labelString += label
            pbtList += labelString + "\n\n"

    return pbtList

# Kinda inefficient, but I'm planning on refactoring the way stats work soon anyway.
def GetRecents():
    recentDays = BAR_WIDTH // 2 - 1
    height = 6
    now = datetime.datetime.now() # Prevent alignment issues due to processing time crossing a log 'anniversary'
    times = []
    disciplines = []

    for i in range(recentDays):
        day = datetime.date.strftime(now - datetime.timedelta(days=i), '%y/%m/%d')
        timeThisDay = 0
        disciplinesThisDay = {}

        for log in LOGS:
            if log['TIME_START'][0:8] == day:
                timeThisDay += log['TIME_LENGTH']
                disciplinesThisDay.update({log['DISC']: log['TIME_LENGTH']})

        dbt = sorted(disciplinesThisDay.items(), key=operator.itemgetter(1))
        keyDiscipline = ""
        if dbt:
            maxValue = max(disciplinesThisDay.items(), key=operator.itemgetter(1))[1]
            dbt.reverse()
            keyDiscipline = dbt[0][0]
        times.append(timeThisDay)
        disciplines.append(keyDiscipline)

    maxValue = max(times)
    times.reverse()
    recentsGraph = ""
    for row in range(height):
        if row > 0:
            recentsGraph += "\n  | "
        else:
            recentsGraph += "  | "
        for col in range(len(times)):
            if times[col] / maxValue * height >= height - row:
                if disciplines[col] in MVP_DISC:
                    if disciplines[col] == MVP_DISC[0]:
                        recentsGraph += bars.DOUBLE
                    elif disciplines[col] == MVP_DISC[1]:
                        recentsGraph += colors.RED + bars.DOUBLE + colors.RESET
                    elif disciplines[col] == MVP_DISC[2]:
                        recentsGraph += colors.BLUE + bars.DOUBLE + colors.RESET
                else:
                    recentsGraph += colors.GREY + bars.DOUBLE + colors.RESET
            else:
                if times[col] > 0 and row == height - 1:
                    recentsGraph += colors.GREY + bars.SHORTDOUBLE + colors.RESET
                else:
                    recentsGraph += colors.GREY + "··" + colors.RESET

    recentsKey = "  | " + str(recentDays) + " days ago"
    recentsKey += " " * (BAR_WIDTH - len(recentsKey) - 3)
    recentsKey += "Today"

    return(recentsGraph, recentsKey)


def ViewStats(args):
    global STATS
    global LOGS
    STATS = chronologicon.input.LoadStats()[0]
    LOGS = chronologicon.input.LoadLogs()

    if STATS == False:
        Message('outputLoadStatsFailed', '', STATS_FILENAME)
        return

    if LOGS == False:
        Message('outputLoadLogsFailed', '', LOGS_FILENAME)
        return

    # Overview numbers
    TotalEntries = "  Total Entries:       " + str(STATS['totallogs'])
    TotalTime =    "  Total Time:          " + str(int(STATS['totaltime']/60/60)) + colors.GREY + " Hours" + colors.RESET
    AvgEntry =     "  Average Duration:    " + str(STATS['avgloglength']//60) + colors.GREY + " Minutes\n" + colors.RESET

    # Graphs
    dbtGraph, dbtKey = GetDbt()
    wbhGraph, wbhKey = GetWbh()
    recentsGraph, recentsKey = GetRecents()

    if len(args) > 0:
        verbose = False
        uniform = False

        if 'refresh' in args:
            chronologicon.input.SaveStats()
            STATS = chronologicon.input.LoadStats() # Reload
            STATS = STATS[0]

        if 'verbose' in args:
            verbose = True

        if 'uniform' in args:
            uniform = True

        pbtList = GetPbt(verbose, uniform)
    else:
        pbtList = GetPbt()


    print("\n\n  Chronologicon ─ Statistics Overview:\n\n")

    print(TotalEntries)
    print(TotalTime)
    print(AvgEntry)

    print('\n  Work by Hour\n')
    print(wbhGraph)
    print('  | ' + 48 * '─')
    print(wbhKey)

    print('\n\n  Recent History\n')
    print(recentsGraph)
    print('  | ' + (BAR_WIDTH - 2) * '─')
    print(recentsKey)

    print('\n\n  Work by Discipline\n')
    print(dbtGraph)
    print(dbtKey)

    print('\n\n  Largest Projects\n')
    print(pbtList)

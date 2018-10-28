#!/usr/bin/env python

# Chronologicon v4.x
# Rutherford Craze
# https://craze.co.uk
# 181028

import chronologicon, operator

STATS_FILENAME = chronologicon.STATS_FILENAME
STATS = {}
BAR_WIDTH = 50


# Console colour ANSI escapes
class colors:
	RED = u"\u001b[31m"
	BLUE = u"\u001b[34m"
	YELLOW = u"\u001b[33m"
	RESET = u"\u001b[0m"

def GetDbt():
	dbt = sorted(STATS['discbytime'].items(), key=operator.itemgetter(1))
	dbtGraph = "  "
	dbtKey = "  "
	R = 0;
	for discipline in range(len(dbt)):
		if discipline < 3:
			k = dbt[len(dbt) - 1 - discipline][0]
			v = dbt[len(dbt) - 1 - discipline][1]
			# parseInt(data.discbytime[dbt[i]] / data.totaltime * 100);

			bar = int(float(v) / float(STATS['totaltime']) * BAR_WIDTH)
			R += bar
			if discipline == 0:
				dbtGraph += (bar * u"\u2588")
				dbtKey += str(k) + "  "
			if discipline == 1:
				dbtGraph += colors.RED + (bar * u"\u2588") + colors.RESET
				dbtKey += colors.RED + str(k) + colors.RESET + "  "
			if discipline == 2:
				dbtGraph += colors.BLUE + (bar * u"\u2588") + colors.RESET
				dbtKey += colors.BLUE + str(k) + colors.RESET + "  "

	if R < BAR_WIDTH:
		dbtGraph += colors.YELLOW + ((BAR_WIDTH - R) * u"\u2588") + colors.RESET
		dbtKey += colors.YELLOW + "other" + colors.RESET

	return (dbtGraph, dbtKey)

def GetWbh():
	height = 6
	maxValue = max(STATS['workbyhour'].items(), key=operator.itemgetter(1))[1]
	wbh = sorted(STATS['workbyhour'].items())
	wbhClamped = []
	wbhGraph = "  | "
	wbhKey = "  | "
	for hour in range(len(wbh)):
		wbhClamped.append(int(float(wbh[hour][1]) / float(maxValue) * height))

	for row in range(height):
		if row > 0:
			wbhGraph += "\n  | "
		for col in range(len(wbhClamped)):
			if wbhClamped[col] >= height - row:
				wbhGraph += u"\u2590\u258C"
			else:
				wbhGraph += "  "

	for col in range(0, len(wbhClamped), 3):
		wbhKey += wbh[col][0] + '    '

	return(wbhGraph, wbhKey)

def GetPbt():
	projects = 5
	graphWidth = BAR_WIDTH;

	pbt = sorted(STATS['projbytime'].items(), key=operator.itemgetter(1))
	maxValue = max(STATS['projbytime'].items(), key=operator.itemgetter(1))[1]

	pbtList = ""
	for project in range(len(pbt)):
		if project < projects:
			k = pbt[len(pbt) - 1 - project][0]
			v = pbt[len(pbt) - 1 - project][1]
			spacer = BAR_WIDTH - len(k) - len(str(v))

			pbtList += "  " + (int(float(v) / float(maxValue) * graphWidth) * u"\u2588") + "\n"
			pbtList += "  " + str(k) + ":" + (spacer * ' ') + str(v / 60 / 60) + " h\n\n"

	return pbtList


def ViewStats():
	global STATS
	STATS = chronologicon.LoadStats()
	STATS = STATS[0]

	if STATS == False:
		print("Unable to load stats file. Please check it exists.")
		return

	# Overview numbers
	TotalEntries = "  Total Entries:    " + str(STATS['totallogs'])
	TotalTime =    "  Total Time:       " + str(int(STATS['totaltime']/60/60)) + " h"
	AvgEntry =     "  Average Log:      " + str(STATS['avgloglength']//60) + " m\n"

	# Graphs
	dbtGraph, dbtKey = GetDbt()
	wbhGraph, wbhKey = GetWbh()
	pbtList = GetPbt()


	Spacer = "\n\n"
	print(Spacer)
	print("  ─── Chronologicon 4.56 ─── Statistics Overview ───\n\n")
	print(TotalEntries)
	print(TotalTime)
	print(AvgEntry)
	print('\n  Work by discipline\n')
	print(dbtGraph)
	print(dbtKey)
	print('\n\n  Work by hour')
	print(wbhGraph)
	print('  | ' + (BAR_WIDTH - 2) * '─')
	print(wbhKey)
	print('\n\n  Largest projects\n')
	print(pbtList)
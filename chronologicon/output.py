#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Chronologicon v4.x
# Rutherford Craze
# https://craze.co.uk
# 181028

import chronologicon, operator

STATS_FILENAME = chronologicon.STATS_FILENAME
STATS = {}
BAR_WIDTH = 50
MVP_DISC = []

# Console colour ANSI escapes
class colors:
	RED = u"\u001b[31m"
	BLUE = u"\u001b[34m"
	GREY = u"\u001b[37m"
	RESET = u"\u001b[0m"
	DEBUG = u"\u001b[35m"

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
				dbtGraph += (bar * u"\u2588")
				dbtKey += str(k) + "  "
			elif len(MVP_DISC) > 1 and MVP_DISC[1] == k:
				dbtGraph += colors.RED + (bar * u"\u2588") + colors.RESET
				dbtKey += colors.RED + str(k) + colors.RESET + "  "
			elif len(MVP_DISC) > 2 and MVP_DISC[2] == k:
				dbtGraph += colors.BLUE + (bar * u"\u2588") + colors.RESET
				dbtKey += colors.BLUE + str(k) + colors.RESET + "  "
			else:
				R -= bar # Ignore 'other' stuff for now, put it at the end

	if R < graphWidth:
		dbtGraph += colors.GREY + ((graphWidth - R) * u"\u2588") + colors.RESET
		dbtKey += colors.GREY + "other" + colors.RESET

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
				wbhGraph += u"\u2590\u258C"
			else:
				wbhGraph += "  "

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
			pbtList += "  " + str(k) + (spacer * ' ') + str(v / 60 / 60) + " h\n\n"

	return pbtList


def ViewStats(args):
	global STATS
	STATS = chronologicon.LoadStats()
	STATS = STATS[0]

	if STATS == False:
		print("Unable to load file: " + STATS_FILENAME + ". Please ensure it exists.")
		return

	# Overview numbers
	TotalEntries = "  Total Entries:    " + str(STATS['totallogs'])
	TotalTime =    "  Total Time:       " + str(int(STATS['totaltime']/60/60)) + " h"
	AvgEntry =     "  Average Log:      " + str(STATS['avgloglength']//60) + " m\n"

	# Graphs
	dbtGraph, dbtKey = GetDbt()
	wbhGraph, wbhKey = GetWbh()

	if len(args) > 0:
		verbose = False
		uniform = False

		if 'refresh' in args:
			chronologicon.SaveStats()
			STATS = chronologicon.LoadStats() # Reload
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

	print('\n  Work by discipline\n')
	print(dbtGraph.encode('utf-8'))
	print(dbtKey)

	print('\n\n  Work by hour')
	print(wbhGraph.encode('utf-8'))
	print('  | ' + (BAR_WIDTH - 2) * '─')
	print(wbhKey)

	print('\n\n  Largest projects\n')
	print(pbtList.encode('utf-8'))

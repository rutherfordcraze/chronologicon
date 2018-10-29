# Chronologicon
v4.57 — 181028

A minimal time tracker, now rewritten for the command line. 

Chron stores in-progress logs in a temporary file in its install directory, meaning you can safely exit all terminal windows, restart your computer, and install updates while logging.

Install:
`$ pip install chronologicon`


## Commands
`$ chron` with no arguments will run preflight checks. This will create any mission-critical files which are currently missing. It returns nothing if everything is OK.

```
-s <args>   Start a new log timer
-x          Complete the current log
-v          View stats & graphs
-b          Backup the log data file
-d <dir>    Change the save directory
--cancel    Abort the current entry
```

The first time you use Chronologicon, you'll need to specify a save directory with the `-d` argument.


## Usage

`$ chron -d ~/Documents/Chron` Change the save directory to a folder on your computer.

`$ chron -s 'discipline' 'project' 'note'`
Create a new log with discipline, project, and (optionally) a note.

`$ chron -x`
Stop tracking and save the current log.

`$ chron -e /Users/<username>/Desktop`
Save the log data file and a stats file to the desktop.


## Combinations

Because the commands Chronologicon takes are all technically optional arguments, you can use them in combination with each other:

`$ chron -x -s <args>` will stop the current log and start a new one with the specified discipline and project.

`$ chron -x -v` will stop the current log and then display statistics.

I haven't tested every combination, so use them at your own risk (and make regular backups!)
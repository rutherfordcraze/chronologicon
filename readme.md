# Chronologicon
v4.51 — 181028

A minimal time tracker, now rewritten for the command line. This is just the tracking side — it doesn't currently include support for displaying tracked information. This feature is in development.

`$ pip install chronologicon` to install.

## Commands
`$ chron` with no arguments will run preflight checks. This will create any mission-critical files which are currently missing. It returns nothing if everything is OK.

```
-s <args>   Start a new log timer
-x          Complete the current log
-b          Backup the log data file
-d <dir>    Change the save directory
--cancel    Abort the current entry
```

## Usage

`$ chron -d ~/Documents/Chron` Change the save directory to a folder on your computer.

`$ chron -s 'discipline' 'project' 'note'`
Create a new log with discipline, project, and (optionally) a note.

`$ chron -x`
Stop tracking and save the current log.

`$ chron -e /Users/<username>/Desktop`
Save the log data file and a stats file to the desktop.
# Chronologicon
v4.14 — 181020

A minimal time tracker, now rewritten for the command line. This is just the tracking side — it doesn't currently include support for displaying tracked information. This feature is in development.

## Commands
`$ chron` with no arguments will run preflight checks. This will create any mission-critical files which are currently missing. It returns nothing if everything is OK.

```
-s <args>   Start a new log timer
-x          Complete the current log
-b          Backup the log data file
-e <dir>    Export all data to a directory
--cancel    Abort the current entry
```

## Usage

`$ chron -s 'discipline' 'project' 'note'`
Create a new log with discipline, project, and (optionally) a note.

`$ chron -x`
Stop tracking and save the current log.

`$ chron -e /Users/<username>/Desktop`
Save the log data file and a stats file to the desktop.
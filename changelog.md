## 5.7

— Fixed issue with recent history graph colours not being accurate.

— Added disclaimer to readme & license to repo.


## 5.6

— Fixed issue where recent history graph would have no colours when tracked disciplines contained uppercase letters.

— Tiny performance optimisation in history graph.

— Added current log duration in hours to status output.

— Changed install instructions in readme.

— Fixed an issue with interpuncts in the output window causing python2 to crash.


## 5.5

— Incremented version number.


## 5.4

— Minor style changes to statistics overview.

— Added a graph of recent log history, with bars coloured by most prominent discipline.

— Migrated some error messages from output.py to strings.py.

— Fixed the misalignment of hour labels in the project duration overview.


## 5.3

— Added current elapsed time message to status.


## 5.2

— Added remove feature for previous logs.

— Reformatted and tidied up a bunch of code.

— Running chron with no arguments now displays status, not help.


## 5.1

— Backups are automatically placed in a 'Backups' folder.

— Separated input features into their own module, `__init__` is now only for preflights.

— Finished centralising messages for all modules except output.

— Updated log file format to use human-readable, timezone-independent time strings.

— Added migration feature for old logs.

— Log write behaviour changed, now overwrites instead of appending.

— Output now resizes to the terminal window.

— Work by discipline graph moved to be closer to project graphs.


## 4.75

— Centralised maintenance messages in strings.py


## 4.74

— Began centralising output messages in strings.py.


## 4.73

— All error messages now include exception info.

— Stats are now case-insensitive, graphs will auto-capitalise project and discipline names.

— Work by Hour graph now counts multi-hour logs across their duration, not just by the hour they were started.


## 4.72

— Specified Python 3 as default interpreter and added a warning if 2.7 is used.

— `directory` command can now interpret user-relative paths (`~/`).

— Running chron with no arguments now displays help text.

— All modules now specify UTF-8 coding. Output module has had minor updates to reflect this.

— All commands now run pre-flight checks before executing. These verify that core save files exist and create missing ones.

About
=====

Simple library for automated report generating from the BTNet bug-tracker system

Requirements
============

-  Windows 8+, Windows server 2012+
-  Lates Chrome browser installed (otherwise, might be a Selenium driver compatibility issues)
-  Python 3+
-  Access to Internet/PyPy

Installation
============

To install, simply do::

    1. Open CMD
    2. Access project directory, e.g., "cd btnetauto_py"
    3. python setup.py install

Rename user_conf-sample.json to user_conf.json and put relevant details there.

Usage
=====

1. Open CMD
2. Access project directory, e.g., "cd btnetauto_py"
3. Run it with something like "python ."

Can be automated by windows task scheduler.

Customization:
=============

- Report structure to be defined in report_struct.json file

reportName - Name of the report file
columns - list of column names from original BugTracker.NET report you wish to filter out
priority - default values "2 - must fix" and "3 - fix". You might add others from BugTracker.NET
txt - the text to be placed in the email

Running tests::
=============

    C:\btnetauto_py>python tests.py
    testReportConf (__main__.TestJsonSettingsInterface) ... ok
    testUserConf (__main__.TestJsonSettingsInterface) ... ok
    testLoggerFactory (__main__.TestLogger) ... ok

    ----------------------------------------------------------------------
    Ran 3 tests in 0.002s

    C:\btnetauto_py>

Reporting issues
================

Please report any issues in the `issue
tracker <https://github.com/swifty94/btnetauto_py/issues/new>`__.


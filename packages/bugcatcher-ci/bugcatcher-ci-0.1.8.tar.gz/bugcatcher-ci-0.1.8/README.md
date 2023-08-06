# bugcatcher-ci
Continuous Integration Tool Assisting in Static Code Analysis Facilitated Through BugCatcher by Faster Than Light

[![PyPI version](https://badge.fury.io/py/bugcatcher-ci.svg)](https://badge.fury.io/py/bugcatcher-ci)
[![CircleCI](https://circleci.com/gh/faster-than-light/bugcatcher-ci.svg?style=svg)](https://circleci.com/gh/faster-than-light/bugcatcher-ci)

[![Issues](https://img.shields.io/github/issues/faster-than-light/bugcatcher-ci)](https://github.com/faster-than-light/bugcatcher-ci/issues)
![Forks](https://img.shields.io/github/forks/faster-than-light/bugcatcher-ci)
![Stars](https://img.shields.io/github/stars/faster-than-light/bugcatcher-ci)
[![License: GPL v2](https://img.shields.io/badge/License-GPL%20v2-blue.svg)](https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html)

### Installation

#### Installing with PIP
`pip install bugcatcher-ci`

#### Sample Integration
Please view the changed files in [this PR](https://github.com/faster-than-light/sampleproject/pull/1). Setting up your testing is as easy as following this example and making sure you have an environment variable saved on CircleCI/TravisCI for `FTL_SID`. Your `FTL_SID` can be found on the dashboard of your BugCatcher account at https://bugcatcher.fasterthanlight.dev

Example of a test run using BugCatcher-CI:
```
% pytest -s
=============================================================== test session starts ===============================================================
platform darwin -- Python 3.8.0, pytest-5.2.2, py-1.8.0, pluggy-0.13.0
rootdir: /sampleproject
plugins: bugcatcher-0.1.6
collected 2 items                                                                                                                                 

tests/test_simple.py 
Testing codebase with BugCatcher API...
Uploading "sampleproject" code to BugCatcher...
Found a `.gitignore` file. Evaluating files...
6 of 20 local files match .gitignore patterns.
14 files ready to upload...
Local item MANIFEST.in
Local item README.md
Local item setup.py
Local item .gitignore
Local item tox.ini
Local item setup.cfg
Local item LICENSE.txt
Local item .travis.yml
Local item tests/test_simple.py
Local item tests/__init__.py
Local item sample/__init__.py
Local item sample/package_data.dat
Local item data/data_file
Local item .circleci/config.yml
Sending new files:
	.circleci/config.yml
	.gitignore
	.travis.yml
	LICENSE.txt
	MANIFEST.in
	README.md
	data/data_file
	sample/__init__.py
	sample/package_data.dat
	setup.cfg
	setup.py
	tests/__init__.py
	tests/test_simple.py
	tox.ini

14 items total changed

Running tests on "sampleproject" using BugCatcher...
BugCatcher results for "sampleproject":

Severity: low ===> tests/test_simple.py (lines 15-15)
	assert_used - Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

Severity: low ===> tests/test_simple.py (lines 17-17)
	assert_used - Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

Severity: low ===> tests/test_simple.py (lines 21-21)
	assert_used - Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.

Minimum Severity Level to FAIL tests: "medium"
PASSING! - All results are less than "medium" level severity.
..

=============================================================== 2 passed in 34.72s ================================================================
```
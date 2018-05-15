tmsyscall
=========

[![pypi version](https://img.shields.io/pypi/v/tmsyscall.svg?maxAge=2592000)](https://pypi.python.org/pypi/tmsyscall)
[![GitHub Forks](https://img.shields.io/github/forks/joaompinto/tmsyscall.svg)](https://github.com/joaompinto/tmsyscall/network)
[![GitHub Open Issues](https://img.shields.io/github/issues/joaompinto/tmsyscall.svg)](https://github.com/joaompinto/tmsyscall/issues)
[![coverage report for master branch](https://codecov.io/github/joaompinto/tmsyscall/coverage.svg?branch=master)](https://codecov.io/github/joaompinto/tmsyscall?branch=master)
[![sphinx documentation for latest release](https://readthedocs.org/projects/tmsyscall/badge/?version=latest)](https://readthedocs.org/projects/tmsyscall/?badge=latest)


Requirements
------------

-   Python 2.7 or 3.4+ (currently tested with 2.7, 3.4)


Installation
------------

``` {.sourceCode .bash}
pip install tmsyscall
```

Usage
-------------

Check the documentation at <http://tmsyscall.readthedocs.io/en/latest/>


Something here.

Usage
-----

Something else here.

Bugs and Feature Requests
-------------------------

Bug reports and feature requests are happily accepted via the [GitHub
Issue
Tracker](https://github.com/joaompinto/tmsyscall/issues).
Pull requests are welcome. Issues that don't have an accompanying pull
request will be worked on as my time and priority allows.

Development
===========

To install for development:

1.  Fork the
    [tmsyscall](https://github.com/joaompinto/tmsyscall)
    repository on GitHub
2.  Create a new branch off of master in your fork.

``` {.sourceCode .bash}
$ virtualenv tmsyscall
$ cd tmsyscall && source bin/activate
$ pip install -e git+git@github.com:YOURNAME/tmsyscall.git@BRANCHNAME#egg=tmsyscall
$ cd src/tmsyscall
```

The git clone you're now in will probably be checked out to a specific
commit, so you may want to `git checkout BRANCHNAME`.

Guidelines
----------

-   pep8 compliant with some exceptions (see pytest.ini)
-   100% test coverage with pytest (with valid tests)

Testing
-------

Testing is done via [pytest](http://pytest.org/latest/), driven by
[tox](http://tox.testrun.org/).

-   testing is as simple as:
    -   `pip install tox`
    -   `tox`
-   If you want to pass additional arguments to pytest, add them to the
    tox command line after "--". i.e., for verbose pytext output on py27
    tests: `tox -e py27 -- -v`

Release Checklist
-----------------

1.  Open an issue for the release; cut a branch off master for that
    issue.
2.  Confirm that there are CHANGES.rst entries for all major changes.
3.  Ensure that Travis tests passing in all environments.
4.  Ensure that test coverage is no less than the last release (ideally,
    100%).
5.  Increment the version number in tmsyscall/version
    and add version and release date to CHANGES.rst, then push to
    GitHub.
6.  Confirm that README.rst renders correctly on GitHub.
7.  Upload package to testpypi:
    -   Make sure your \~/.pypirc file is correct (a repo called `test`
        for <https://testpypi.python.org/pypi>)
    -   `rm -Rf dist`
    -   `python setup.py register -r https://testpypi.python.org/pypi`
    -   `python setup.py sdist bdist_wheel`
    -   `twine upload -r test dist/*`
    -   Check that the README renders at
        <https://testpypi.python.org/pypi/tmsyscall>

8.  Create a pull request for the release to be merged into master. Upon
    successful Travis build, merge it.
9.  Tag the release in Git, push tag to GitHub:
    -   tag the release. for now the message is quite simple:
        `git tag -s -a X.Y.Z -m 'X.Y.Z released YYYY-MM-DD'`
    -   push the tag to GitHub: `git push origin X.Y.Z`

10. Upload package to live pypi:
    -   `twine upload dist/*`

11. make sure any GH issues fixed in the release were closed.


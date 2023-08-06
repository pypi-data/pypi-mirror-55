========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |appveyor| |requires|
        | |codecov|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|
.. |docs| image:: https://readthedocs.org/projects/python-tiidan-utils/badge/?style=flat
    :target: https://readthedocs.org/projects/python-tiidan-utils
    :alt: Documentation Status

.. |travis| image:: https://travis-ci.org/ionelmc/python-tiidan-utils.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/ionelmc/python-tiidan-utils

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/ionelmc/python-tiidan-utils?branch=master&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/ionelmc/python-tiidan-utils

.. |requires| image:: https://requires.io/github/ionelmc/python-tiidan-utils/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/ionelmc/python-tiidan-utils/requirements/?branch=master

.. |codecov| image:: https://codecov.io/github/ionelmc/python-tiidan-utils/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/ionelmc/python-tiidan-utils

.. |version| image:: https://img.shields.io/pypi/v/tiidan-utils.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/tiidan-utils

.. |commits-since| image:: https://img.shields.io/github/commits-since/ionelmc/python-tiidan-utils/v0.0.0.svg
    :alt: Commits since latest release
    :target: https://github.com/ionelmc/python-tiidan-utils/compare/v0.0.0...master

.. |wheel| image:: https://img.shields.io/pypi/wheel/tiidan-utils.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/tiidan-utils

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/tiidan-utils.svg
    :alt: Supported versions
    :target: https://pypi.org/project/tiidan-utils

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/tiidan-utils.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/tiidan-utils


.. end-badges

Tiidan utils in python.

* Free software: BSD 2-Clause License

Installation
============

::

    pip install tiidan-utils

Documentation
=============


https://python-tiidan-utils.readthedocs.io/


Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox

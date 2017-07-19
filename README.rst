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

.. |docs| image:: https://readthedocs.org/projects/skywatch-python-client/badge/?style=flat
    :target: https://readthedocs.org/projects/skywatch-python-client
    :alt: Documentation Status

.. |travis| image:: https://travis-ci.org/medwig/skywatch-python-client.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/medwig/skywatch-python-client

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/medwig/skywatch-python-client?branch=master&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/medwig/skywatch-python-client

.. |requires| image:: https://requires.io/github/medwig/skywatch-python-client/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/medwig/skywatch-python-client/requirements/?branch=master

.. |codecov| image:: https://codecov.io/github/medwig/skywatch-python-client/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/medwig/skywatch-python-client

.. |version| image:: https://img.shields.io/pypi/v/skywatch.svg
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/skywatch

.. |commits-since| image:: https://img.shields.io/github/commits-since/medwig/skywatch-python-client/v0.1.0.svg
    :alt: Commits since latest release
    :target: https://github.com/medwig/skywatch-python-client/compare/v0.1.0...master

.. |wheel| image:: https://img.shields.io/pypi/wheel/skywatch.svg
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/skywatch

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/skywatch.svg
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/skywatch

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/skywatch.svg
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/skywatch


.. end-badges

Python client to access Skywatch API

* Free software: Apache Software License 2.0

Installation
============

::

    pip install skywatch

Documentation
=============

https://skywatch-python-client.readthedocs.io/

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

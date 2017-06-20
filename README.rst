.. image:: https://img.shields.io/badge/license-MIT-brightgreen.svg
    :target: https://github.com/Kalimaha/pact-test/blob/master/LICENSE
.. image:: https://img.shields.io/badge/python-2.7,%203.3,%203.4,%203.5,%203.6-brightgreen.svg
    :target: https://travis-ci.org/Kalimaha/pact-test
.. image:: https://img.shields.io/badge/pypi-0.1.1-brightgreen.svg
    :target: https://pypi.python.org/pypi?:action=display&name=pact-test&version=0.1.1
.. image:: https://img.shields.io/pypi/wheel/Django.svg
    :target: https://pypi.python.org/pypi?:action=display&name=pact-test&version=0.1.1
.. image:: https://travis-ci.org/Kalimaha/pact-test.svg?branch=master
    :target: https://travis-ci.org/Kalimaha/pact-test
.. image:: https://coveralls.io/repos/github/Kalimaha/pact-test/badge.svg?branch=development
    :target: https://coveralls.io/github/Kalimaha/pact-test?branch=development
.. image:: https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg 
    :target: https://saythanks.io/to/Kalimaha

Pact Test for Python
===============

Python implementation for Pact (http://pact.io/)

Setup
-----

.. code:: bash

  python setup.py install

Test
----

It is possible to run the tests locally with Docker through the following command:

.. code:: bash

  $ ./bin/test

By default this command tests the library against Python 3.6. It is possible to specify the Python version as follows:

.. code:: bash

  $ ./bin/test <ENV>

Available values for `ENV` are: :code:`py27`, :code:`py33`, :code:`py34`, :code:`py35` and :code:`py36`. It is also
possible to test all the versions at once with:

.. code:: bash

  $ ./bin/test all
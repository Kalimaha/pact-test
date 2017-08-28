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
====================

This repository contains a Python implementation for `Pact <http://pact.io/>`_. Pact is a specification for
Consumer Driven Contracts Testing. For further information about Pact project, contracts testing, pros and cons and
useful resources please refer to the `Pact website <http://pact.io/>`_.

There are two phases in Consumer Driven Contracts Testing: a Consumer sets up a contract (*it's consumer driven
after all!*), and a Provider honours it.

Providers Tests (*Set the Contracts*)
-------------------------------------

.. image:: https://img.shields.io/badge/Pact-1.0-red.svg
    :target: https://github.com/pact-foundation/pact-specification/tree/version-1
.. image:: https://img.shields.io/badge/Pact-1.1-red.svg
    :target: https://github.com/pact-foundation/pact-specification/tree/version-1.1
.. image:: https://img.shields.io/badge/Pact-2.0-red.svg
    :target: https://github.com/pact-foundation/pact-specification/tree/version-2
.. image:: https://img.shields.io/badge/Pact-3.0-red.svg
    :target: https://github.com/pact-foundation/pact-specification/tree/version-3
.. image:: https://img.shields.io/badge/Pact-4.0-red.svg
    :target: https://github.com/pact-foundation/pact-specification/tree/version-4

TBD.

Consumers Tests (*Honour Your Contracts*)
-----------------------------------------

.. image:: https://img.shields.io/badge/Pact-1.0-brightgreen.svg
    :target: https://github.com/pact-foundation/pact-specification/tree/version-1
.. image:: https://img.shields.io/badge/Pact-1.1-red.svg
    :target: https://github.com/pact-foundation/pact-specification/tree/version-1.1
.. image:: https://img.shields.io/badge/Pact-2.0-red.svg
    :target: https://github.com/pact-foundation/pact-specification/tree/version-2
.. image:: https://img.shields.io/badge/Pact-3.0-red.svg
    :target: https://github.com/pact-foundation/pact-specification/tree/version-3
.. image:: https://img.shields.io/badge/Pact-4.0-red.svg
    :target: https://github.com/pact-foundation/pact-specification/tree/version-4

Providers run Consumer Tests to verify that they are honouring their pacts with the consumers. There are few examples
of an hypothetical restaurant service implemented with the most popular Python web frameworks:

* Djanjo (*TODO*)
* `Flask <https://github.com/Kalimaha/restaurant-service-flask>`_
* Pyramid (*TODO*)

There are few things required to setup and run consumer tests.

Installation
~~~~~~~~~~~~

Pact Test is distributed through `PyPi <https://pypi.python.org/pypi/pact-test>`_ so it can be easily included in the
:code:`requirements.txt` file or normally installed with :code:`pip`:

.. code:: bash

  $ pip install pact-test

Pact Helper
~~~~~~~~~~~

This helper class is used by Pact Test to start and stop the web-app before and after the test. It also defines the
ports and endpoint to be used by the test. The following is an example of Pact Helper:

.. code:: python

    class RestaurantPactHelper(PactHelper):
        process = None

        def setup(self):
            self.process = subprocess.Popen('gunicorn start:app -w 3 -b :8080 --log-level error', shell=True)

        def tear_down(self):
            self.process.kill()

There are few rules for the helper:

* it **must** extend :code:`PactHelper` class from :code:`pact_test`
* it **must** define a :code:`setup` method
* it **must** define a :code:`tear_down` method

It is also possible to override default url (*localhost*) and port (*9999*):

.. code:: python

    class RestaurantPactHelper(PactHelper):
        test_url = '0.0.0.0'
        test_port = 5000


States
~~~~~~

When a consumer sets a pact, it defines certain states. States are basically pre-requisites to your test. Before
honouring the pacts, a provider needs to define such states. For example:

.. code:: python

    @honours_pact_with('UberEats')
    @pact_uri('http://Kalimaha.github.io/src/pacts/pact.json')
    class UberEats(ServiceConsumerTest):

        @state('some menu items exist')
        def test_get_menu_items(self):
            DB.save(MenuItem('spam'))
            DB.save(MenuItem('eggs'))

In this example, the provider stores some test data in its DB in order to make the system ready to receive mock calls
from the consumer and therefore verify the pact.

Configuration
-------------

The default configuration of Pact Test assumes the following values:

* **consumer_tests_path:** :code:`tests/service_consumers`
* **provider_tests_path:** :code:`tests/service_providers`
* **pact_broker_uri:** :code:`None`

It is possible to override such values by creating a file named :code:`.pact.json` in the project's root. The following
is an example of a valid configuration file:

.. code:: json

  {
    "consumer_tests_path": "mypath/mytests",
    "provider_tests_path": "mypath/mytests",
    "pact_broker_uri": "http://example.com/"
  }

All fields are optional: only specified fields will override default configuration values.

Development
===========

Setup
-----

.. code:: bash

  python3 setup.py install

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

Upload New Version
------------------

.. code:: bash

  $ python3 setup.py sdist upload

With `Python Wheels <http://pythonwheels.com/>`_:

.. code:: bash
  $ python3 setup.py sdist bdist_wheel
  $ twine upload dist/*

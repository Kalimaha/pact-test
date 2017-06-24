import os
import sys
import imp
import requests
from pact_test.either import Left
from pact_test.config.config_builder import Config
from pact_test.runners.service_consumers.test_suite import ServiceConsumerTestSuiteRunner  # nopep8


def test_verify(monkeypatch):
    config = Config()
    config.consumer_tests_path = os.path.join(os.getcwd(), 'tests',
                                              'resources',
                                              'service_consumers')
    sct = ServiceConsumerTestSuiteRunner(config)

    class Response(object):
        status_code = 200
        headers = {'Content-Type': 'application/json', 'Date': '12-06-2017'}

        def json(self):
            return {'spam': 'eggs'}

    def connect(_, **kwargs):
        return Response()
    monkeypatch.setattr(requests, 'request', connect)

    actual_response = sct.verify()

    assert len(actual_response) == 1
    assert actual_response[0].value['test'] == 'TestRestaurantCustomer'
    assert len(actual_response[0].value['results']) == 1

    test_outcome = actual_response[0].value['results'][0].value
    assert test_outcome['state'] == 'the breakfast is available'
    assert test_outcome['status'] == 'FAILED'
    assert len(test_outcome['errors']) == 1
    assert test_outcome['errors'][0]['message'] == 'Headers is incorrect'


def test_verify_bad_pact():
    config = Config()
    config.consumer_tests_path = os.path.join(os.getcwd(), 'tests',
                                              'resources',
                                              'service_consumers_bad_pact')
    sct = ServiceConsumerTestSuiteRunner(config)
    actual_response = sct.verify()
    assert type(actual_response[0]) is Left


def test_missing_pact_helper():
    config = Config()
    t = ServiceConsumerTestSuiteRunner(config)
    msg = 'Missing "pact_helper.py" at "tests/service_consumers".'

    assert t.verify().value == msg


def test_missing_setup_method():
    remove_pact_helper()

    config = Config()
    test_pact_helper_path = os.path.join(os.getcwd(), 'tests',
                                         'resources', 'pact_helper_no_setup')
    config.consumer_tests_path = test_pact_helper_path
    t = ServiceConsumerTestSuiteRunner(config)
    msg = 'Missing "setup" method in "pact_helper.py".'
    assert t.verify().value == msg


def test_missing_tear_down_method():
    remove_pact_helper()

    config = Config()
    test_pact_helper_path = os.path.join(os.getcwd(), 'tests', 'resources',
                                         'pact_helper_no_tear_down')
    config.consumer_tests_path = test_pact_helper_path
    t = ServiceConsumerTestSuiteRunner(config)
    msg = 'Missing "tear_down" method in "pact_helper.py".'
    assert t.verify().value == msg


def test_empty_tests_list(monkeypatch):
    config = Config()
    test_pact_helper_path = os.path.join(os.getcwd(), 'tests', 'resources',
                                         'service_consumers')
    config.consumer_tests_path = test_pact_helper_path

    def empty_list(_):
        return []
    monkeypatch.setattr(os, 'listdir', empty_list)

    t = ServiceConsumerTestSuiteRunner(config)
    msg = 'There are no consumer tests to verify.'
    assert t.collect_tests().value == msg


def test_collect_tests():
    config = Config()
    test_pact_helper_path = os.path.join(os.getcwd(), 'tests', 'resources',
                                         'service_consumers')
    config.consumer_tests_path = test_pact_helper_path
    t = ServiceConsumerTestSuiteRunner(config)

    tests = t.collect_tests().value
    assert len(tests) == 1

    test = tests[0]
    assert test.pact_uri == 'tests/resources/pact_files/simple.json'
    assert test.has_pact_with == 'Restaurant'

    state = next(test.states)
    assert state.state == 'the breakfast is available'
    assert state() == 'Spam & Eggs'


def test_invalid_test():
    path = os.path.join(os.getcwd(), 'tests', 'resources',
                        'invalid_service_consumer', 'customer.py')
    module = imp.load_source('invalid_test', path)
    test = module.TestRestaurantCustomer()

    t = ServiceConsumerTestSuiteRunner(None)
    msg = 'Missing setup for "has_pact_with"'
    assert t.verify_test(test).value.startswith(msg)


def remove_pact_helper():
    try:
        del sys.modules['pact_helper']
    except KeyError:
        pass

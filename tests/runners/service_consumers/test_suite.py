import os
import sys
import imp
import json
from pact_test.config.config_builder import Config
from pact_test.runners.service_consumers.test_suite import ServiceConsumerTestSuiteRunner  # nopep8


def test_missing_pact_helper():
    config = Config()
    t = ServiceConsumerTestSuiteRunner(config)
    msg = 'Missing "pact_helper.py" at "tests/service_consumers".'
    assert t.path_to_pact_helper().value == msg


def test_missing_setup_method():
    remove_pact_helper()

    config = Config()
    test_pact_helper_path = os.path.join(os.getcwd(), 'tests',
                                         'resources', 'pact_helper_no_setup')
    config.consumer_tests_path = test_pact_helper_path
    t = ServiceConsumerTestSuiteRunner(config)
    msg = 'Missing "setup" method in "pact_helper.py".'
    assert t.load_pact_helper().value == msg


def test_missing_tear_down_method():
    remove_pact_helper()

    config = Config()
    test_pact_helper_path = os.path.join(os.getcwd(), 'tests', 'resources',
                                         'pact_helper_no_tear_down')
    config.consumer_tests_path = test_pact_helper_path
    t = ServiceConsumerTestSuiteRunner(config)
    msg = 'Missing "tear_down" method in "pact_helper.py".'
    assert t.load_pact_helper().value == msg


def test_empty_tests_list(monkeypatch):
    config = Config()
    test_pact_helper_path = os.path.join(os.getcwd(), 'tests', 'resources',
                                         'service_consumers')
    config.consumer_tests_path = test_pact_helper_path

    def empty_list(_):
        return []
    monkeypatch.setattr(os, 'listdir', empty_list)

    t = ServiceConsumerTestSuiteRunner(config)
    assert t.collect_tests().value == 'There are no consumer tests to verify.'


def test_collect_tests():
    config = Config()
    test_pact_helper_path = os.path.join(os.getcwd(), 'tests', 'resources',
                                         'service_consumers')
    config.consumer_tests_path = test_pact_helper_path
    t = ServiceConsumerTestSuiteRunner(config)

    tests = t.collect_tests().value
    assert len(tests) == 1

    test = tests[0]()
    assert test.pact_uri == 'http://google.com/'
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


def test_verify_missing_state(mocker):
    def pact_content(_):
        s = '{"interactions": [{"providerState": "My State"}]}'
        return json.loads(s)

    path = os.path.join(os.getcwd(), 'tests', 'resources',
                        'service_consumers', 'test_restaurant_customer.py')
    module = imp.load_source('consumer_test', path)
    test = module.TestRestaurantCustomer()

    t = ServiceConsumerTestSuiteRunner(None)
    mocker.patch.object(t, 'get_pact', new=pact_content)

    msg = 'Missing implementation for state "My State".'
    assert t.verify_test(test).value == msg


def test_verify_existing_state(mocker):
    def pact_content(_):
        s = '{"interactions": [{"providerState": ' \
            '"the breakfast is available"}]}'
        return json.loads(s)

    path = os.path.join(os.getcwd(), 'tests', 'resources',
                        'service_consumers', 'test_restaurant_customer.py')
    module = imp.load_source('consumer_test', path)
    test = module.TestRestaurantCustomer()

    t = ServiceConsumerTestSuiteRunner(None)
    mocker.patch.object(t, 'get_pact', new=pact_content)
    mocker.spy(t, 'verify_state')

    t.verify_test(test)
    assert t.verify_state.call_count == 1


def remove_pact_helper():
    try:
        del sys.modules['pact_helper']
    except KeyError:
        pass

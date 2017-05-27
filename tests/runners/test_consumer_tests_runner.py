import os
import sys
import pytest
from pact_test.runners.consumer_tests_runner import ConsumerTestsRunner
from pact_test.config.config_builder import Config
from pact_test.exceptions import PactTestException


def test_missing_pact_helper():
    config = Config()
    t = ConsumerTestsRunner(config)
    msg = 'Missing "pact_helper.py" at "tests/service_consumers".'
    with pytest.raises(PactTestException) as e:
        t.path_to_pact_helper()
    assert str(e.value) == msg


def test_missing_setup_method():
    remove_pact_helper()

    config = Config()
    test_pact_helper_path = os.path.join(os.getcwd(), 'tests',
                                         'resources', 'pact_helper_no_setup')
    config.consumer_tests_path = test_pact_helper_path
    t = ConsumerTestsRunner(config)
    msg = 'Missing "setup" method in "pact_helper.py".'
    with pytest.raises(PactTestException) as e:
        t.load_pact_helper()
    assert str(e.value) == msg


def test_missing_tear_down_method():
    remove_pact_helper()

    config = Config()
    test_pact_helper_path = os.path.join(os.getcwd(), 'tests', 'resources',
                                         'pact_helper_no_tear_down')
    config.consumer_tests_path = test_pact_helper_path
    t = ConsumerTestsRunner(config)
    msg = 'Missing "tear_down" method in "pact_helper.py".'
    with pytest.raises(PactTestException) as e:
        t.load_pact_helper()
    assert str(e.value) == msg


def test_empty_tests_list(monkeypatch):
    config = Config()
    test_pact_helper_path = os.path.join(os.getcwd(), 'tests', 'resources',
                                         'service_consumers')
    config.consumer_tests_path = test_pact_helper_path

    def empty_list(_):
        return []
    monkeypatch.setattr(os, 'listdir', empty_list)

    t = ConsumerTestsRunner(config)
    with pytest.raises(PactTestException) as e:
        t.collect_tests()
    assert str(e.value) == 'There are no consumer tests to verify.'


def test_collect_tests():
    config = Config()
    test_pact_helper_path = os.path.join(os.getcwd(), 'tests', 'resources',
                                         'service_consumers')
    config.consumer_tests_path = test_pact_helper_path
    t = ConsumerTestsRunner(config)

    tests = t.collect_tests()
    assert len(tests) == 1

    test = tests[0]()
    assert test.pact_uri == 'http://google.com/'
    assert test.has_pact_with == 'Restaurant'

    state = next(test.states)
    assert state.state == 'the breakfast is available'
    assert state() == 'Spam & Eggs'


def remove_pact_helper():
    try:
        del sys.modules['pact_helper']
    except KeyError:
        pass

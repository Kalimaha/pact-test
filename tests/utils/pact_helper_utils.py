import os
from pact_test import PactHelper
from pact_test.utils.pact_helper_utils import load_pact_helper


def test_path_to_pact_helper(monkeypatch):
    monkeypatch.setattr(os.path, 'isfile', lambda _: True)

    consumer_tests_path = '/consumer_tests/'
    pact_helper = load_pact_helper(consumer_tests_path).value

    msg = 'Missing "pact_helper.py" at "/consumer_tests/pact_helper.py".'
    assert pact_helper == msg


def test_path_to_pact_helper_missing():
    consumer_tests_path = '/consumer_tests/'
    pact_helper = load_pact_helper(consumer_tests_path).value

    msg = 'Missing "pact_helper.py" at "/consumer_tests/".'
    assert pact_helper == msg


def test_load_module_missing():
    consumer_tests_path = '/consumer_tests/'
    pact_helper = load_pact_helper(consumer_tests_path).value

    assert pact_helper == 'Missing "pact_helper.py" at "/consumer_tests/".'


def test_load_user_class_missing_setup():
    consumer_tests_path = os.path.join(os.getcwd(), 'tests',
                                       'resources', 'pact_helper_no_setup')
    pact_helper = load_pact_helper(consumer_tests_path).value

    error_message = 'Missing "setup" method in "pact_helper.py".'
    assert pact_helper == error_message


def test_load_user_class_missing_tear_down():
    consumer_tests_path = os.path.join(os.getcwd(), 'tests',
                                       'resources', 'pact_helper_no_tear_down')
    pact_helper = load_pact_helper(consumer_tests_path).value

    error_message = 'Missing "tear_down" method in "pact_helper.py".'
    assert pact_helper == error_message


def test_load_pact_helper():
    consumer_tests_path = os.path.join(os.getcwd(), 'tests',
                                       'resources', 'pact_helper')
    pact_helper = load_pact_helper(consumer_tests_path).value
    assert issubclass(pact_helper.__class__, PactHelper)

import os
import sys
import imp
from pact_test import *
from pact_test.either import Left
from pact_test.config.config_builder import Config
from pact_test.runners.service_providers.test_suite import ServiceProviderTestSuiteRunner   # nopep8


def test_empty_tests_list(monkeypatch):
    config = Config()
    config.provider_tests_path = os.path.join(os.getcwd(), 'tests',
                                              'resources',
                                              'service_providers')

    def empty_list(_):
        return []
    monkeypatch.setattr(os, 'listdir', empty_list)

    t = ServiceProviderTestSuiteRunner(config)
    msg = 'There are no provider tests to verify.'
    assert t.collect_tests().value == msg


def test_collect_tests():
    config = Config()
    config.provider_tests_path = os.path.join(os.getcwd(), 'tests',
                                              'resources',
                                              'service_providers')
    t = ServiceProviderTestSuiteRunner(config)

    tests = t.collect_tests().value
    assert len(tests) == 2


def test_build_expected_response():
    mock_resp = {
        'status': 418,
        'body': {'spam': 'eggs'},
        'headers': [{'Spam': 'eggs'}]
    }

    class SimpleTest(ServiceProviderTest):
        @given('the breakfast menu is available')
        @upon_receiving('a request for a breakfast')
        @with_request('I don\'t like spam')
        @will_respond_with(mock_resp)
        def test_get_book(self):
            pass

    simple_test = SimpleTest()
    method = next(simple_test.decorated_methods)
    response = ServiceProviderTestSuiteRunner.build_expected_response(method)

    assert response.status == 418
    assert response.headers == [{'Spam': 'eggs'}]
    assert response.body == {'spam': 'eggs'}


def test_mock_server():
    config = Config()
    config.provider_tests_path = os.path.join(os.getcwd(), 'tests',
                                              'resources',
                                              'service_providers')
    t = ServiceProviderTestSuiteRunner(config)

    test_result = t.verify()
    assert type(test_result) is Left

import os
from pact_test.either import *
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


def test_missing_test_directory():
    config = Config()
    config.provider_tests_path = os.path.join(os.getcwd(), 'spam')
    t = ServiceProviderTestSuiteRunner(config)
    result = t.verify()
    assert type(result) is Left
    assert result.value.startswith("[Errno 2] No such file or directory:")

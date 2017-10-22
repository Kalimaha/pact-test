import os
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

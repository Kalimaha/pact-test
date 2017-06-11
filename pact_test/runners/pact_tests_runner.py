from pact_test.config.config_builder import Config
from pact_test.runners.service_consumers.test_suite import ServiceConsumerTestSuiteRunner
from pact_test.runners.service_providers.provider_tests_runner import ProviderTestsRunner


def verify(verify_consumers=False, verify_providers=False):
    config = Config()

    if verify_consumers:
        run_consumer_tests(config)
    if verify_providers:
        run_provider_tests(config)


def run_consumer_tests(config):
    ServiceConsumerTestSuiteRunner(config).verify()


def run_provider_tests(config):
    ProviderTestsRunner(config).verify()

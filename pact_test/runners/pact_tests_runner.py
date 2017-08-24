from pact_test.either import *
from pact_test.utils.logger import *
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
    test_results = ServiceConsumerTestSuiteRunner(config).verify()
    if type(test_results) is Left:
        error(test_results.value)
    else:
        if type(test_results.value) is Left:
            error(test_results.value.value)
        else:
            for test_result in test_results.value:
                print()
                info('Test: ' + test_result.value['test'])
                for result in test_result.value['results']:
                    info('  GIVEN ' + result.value['state'] + ' UPON RECEIVING ' + result.value['description'])
                    info('    status: ' + result.value['status'])
                    for test_error in result.value['errors']:
                        error('      expected: ' + str(test_error['expected']))
                        error('      actual:   ' + str(test_error['actual']))
                        error('      message:  ' + str(test_error['message']))
    info('')
    info('Goodbye!')
    print()


def run_provider_tests(config):
    ProviderTestsRunner(config).verify()

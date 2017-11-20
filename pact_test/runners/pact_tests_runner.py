import os
import json
import copy
from pact_test.either import *
from pact_test.utils.logger import *
from pact_test.config.config_builder import Config
from pact_test.repositories.pact_broker import upload_pact
from pact_test.utils.pact_helper_utils import format_headers
from pact_test.utils.logger import log_consumers_test_results
from pact_test.utils.logger import log_providers_test_results
from pact_test.runners.service_consumers.test_suite import ServiceConsumerTestSuiteRunner
from pact_test.runners.service_providers.test_suite import ServiceProviderTestSuiteRunner


def verify(verify_consumers=False, verify_providers=False):
    config = Config()

    if verify_consumers:
        run_consumer_tests(config)
    if verify_providers:
        run_provider_tests(config)


def run_consumer_tests(config):
    test_results = ServiceConsumerTestSuiteRunner(config).verify()
    log_consumers_test_results(test_results)


def run_provider_tests(config):
    test_results = ServiceProviderTestSuiteRunner(config).verify()
    log_providers_test_results(test_results)
    if type(test_results) is Right:
        write_pact_files(config, copy.deepcopy(test_results.value))
        upload_pacts(config, copy.deepcopy(test_results.value))


def upload_pacts(config, pacts):
    for pact in pacts:
        provider = pact['provider']['name']
        consumer = pact['consumer']['name']
        is_uploadable = all(interaction['status'] == 'PASSED' for interaction in pact['interactions'])
        if is_uploadable:
            ack = upload_pact(provider, consumer, pact, base_url=config.pact_broker_uri)
            msg = 'Pact between ' + pact['consumer']['name'] + ' and ' + pact['provider']['name']
            error(ack.value) if type(ack) is Left else info(msg + ' successfully uploaded')


def write_pact_files(config, pacts):
    pacts_directory = os.path.join(os.getcwd(), config.pacts_path)
    if not os.path.exists(pacts_directory):
        info('Creating Pacts directory at: ' + str(pacts_directory))
        os.makedirs(pacts_directory)

    for pact in pacts:
        pact_payload = format_headers(copy.deepcopy(pact))
        filename = pact_payload['consumer']['name'] + '_' + pact_payload['provider']['name'] + '.json'
        filename = filename.replace(' ', '_').lower()
        info('Writing pact to: ' + filename)
        with open(os.path.join(pacts_directory, filename), 'w+') as file:
            file.write(json.dumps(pact_payload, indent=2))

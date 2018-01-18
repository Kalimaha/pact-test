import os
import imp
import inspect
from pact_test.either import *
from pact_test.constants import *
from pact_test.utils.logger import error
from pact_test.utils.logger import debug
from pact_test.runners.service_providers.request_test import verify_request


class ServiceProviderTestSuiteRunner(object):
    def __init__(self, config):
        self.config = config

    def verify(self):
        debug('Verify providers: START')
        tests = self.collect_tests()
        if type(tests) is Right:
            debug(str(len(tests.value)) + ' test(s) found.')
            pacts = []
            for test in tests.value:
                debug('Start: ' + test.service_consumer + ' has Pact with ' + test.has_pact_with)
                test_verification = test.is_valid()
                if type(test_verification) is Right:
                    pact = self.create_pact(test)
                    if len(pact['interactions']) == 0:
                        error('Verify providers: EXIT WITH ERRORS:')
                        return Left('No pact-test methods available in test class')
                    pacts.append(pact)
                else:
                    error('Verify providers: EXIT WITH ERRORS:')
                    error(test_verification.value)
                    return test_verification
            return Right(pacts)
        error('Verify providers: EXIT WITH ERRORS:')
        error(tests.value)
        return tests

    @staticmethod
    def create_pact(test):
        interactions = []
        for decorated_method in test.decorated_methods:
            debug('  Verify interaction: ' + decorated_method.__name__)
            interactions.append(verify_request(decorated_method).value)
        pact = {
            'interactions': interactions,
            'provider': {
                'name': test.has_pact_with
            },
            'consumer': {
                'name': test.service_consumer
            }
        }
        return pact

    def collect_tests(self):
        root = self.config.provider_tests_path
        debug('Root for Provider Tests: ' + str(root))
        all_files = self.all_files()
        if type(all_files) is Right:
            files = list(filter(self.filter_rule, all_files.value))
            files = list(map(lambda f: os.path.join(root, f), files))
            tests = []
            for idx, filename in enumerate(files):
                test = imp.load_source('test' + str(idx), filename)
                for name, obj in inspect.getmembers(test):
                    if inspect.isclass(obj) and len(inspect.getmro(obj)) > 2:
                        test_parent = inspect.getmro(obj)[1].__name__
                        if test_parent == PROVIDER_TEST_PARENT:
                            tests.append(obj())

            if not files:
                return Left(MISSING_PROVIDER_TESTS)
            return Right(tests)
        return all_files

    @staticmethod
    def filter_rule(filename):
        return filename != '__init__.py' and filename.endswith('.py')

    def all_files(self):
        try:
            return Right(os.listdir(self.config.provider_tests_path))
        except Exception as e:
            return Left(str(e))

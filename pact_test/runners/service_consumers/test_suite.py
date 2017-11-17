import os
import imp
import inspect
from pact_test.either import *
from pact_test.constants import *
from pact_test.utils.logger import *
from pact_test.utils.pact_utils import get_pact
from pact_test.utils.pact_helper_utils import load_pact_helper
from pact_test.runners.service_consumers.state_test import verify_state


class ServiceConsumerTestSuiteRunner(object):
    pact_helper = None

    def __init__(self, config):
        self.config = config

    def verify(self):
        print('')
        debug('Verify consumers: START')
        pact_helper = load_pact_helper(self.config.consumer_tests_path)
        if type(pact_helper) is Right:
            self.pact_helper = pact_helper.value
            tests = self.collect_tests()
            if type(tests) is Right:
                debug(str(len(tests.value)) + ' test(s) found.')
                debug('Execute Pact Helper setup: START')
                self.pact_helper.setup()
                debug('Execute Pact Helper setup: DONE')
                test_results = Right(list(map(self.verify_test, tests.value)))
                debug('Execute Pact Helper tear down: START')
                self.pact_helper.tear_down()
                debug('Execute Pact Helper tear down: DONE')
                debug('Verify consumers: DONE')
                return test_results
            error('Verify consumers: EXIT WITH ERRORS:')
            error(tests.value)
            return tests
        error('Verify consumers: EXIT WITH ERRORS:')
        error(pact_helper.value)
        return pact_helper

    def verify_test(self, test):
        validity_check = test.is_valid()
        if type(validity_check) is Right:
            pact = get_pact(test.pact_uri)
            if type(pact) is Right:
                interactions = pact.value.get('interactions', {})
                debug(str(len(interactions)) + ' interaction(s) found')
                test_results = [verify_state(i, self.pact_helper, test) for i in interactions]
                return Right({'test': test.__class__.__name__, 'results': test_results})
            error(pact.value)
            return pact
        error(validity_check.value)
        return validity_check

    def collect_tests(self):
        root = self.config.consumer_tests_path
        files = list(filter(filter_rule, self.all_files()))
        files = list(map(lambda f: os.path.join(root, f), files))
        tests = []
        for idx, filename in enumerate(files):
            test = imp.load_source('test' + str(idx), filename)
            for name, obj in inspect.getmembers(test):
                if inspect.isclass(obj) and len(inspect.getmro(obj)) > 2:
                    test_parent = inspect.getmro(obj)[1].__name__
                    if test_parent == TEST_PARENT:
                        tests.append(obj())

        if not files:
            return Left(MISSING_TESTS)
        return Right(tests)

    def all_files(self):
        return os.listdir(self.config.consumer_tests_path)


def filter_rule(filename):
    return (filename != '__init__.py' and
            filename.endswith('.py') and
            filename.endswith('pact_helper.py') is False)

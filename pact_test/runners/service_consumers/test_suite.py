import os
import imp
import inspect
from pact_test.either import *
from pact_test.utils.pact_helper_utils import load_pact_helper
from pact_test.constants import *
from pact_test.utils.pact_utils import get_pact


class ServiceConsumerTestSuiteRunner(object):
    pact_helper = None

    def __init__(self, config):
        self.config = config

    def verify(self):
        pact_helper = load_pact_helper(self.config.consumer_tests_path)
        if type(pact_helper) is Right:
            self.pact_helper = pact_helper
            return self.collect_tests() >> self.verify_tests
        return pact_helper

    def verify_tests(self, tests):
        return list(map(self.verify_test, tests))

    def verify_test(self, test):
        validity_check = test.is_valid()
        if type(validity_check) is Right:
            pact = self.get_pact(test.pact_uri)

            pact_states = list(map(lambda i: i['providerState'], pact['interactions']))
            test_states = list(map(lambda s: s.state, test.states))

            for pact_state in pact_states:
                if pact_state not in test_states:
                    msg = MISSING_STATE + '"' + pact_state + '".'
                    return Left(msg)
                self.verify_state(test.states, pact_state)
        else:
            return validity_check

    def verify_state(self, states, provider_state):
        # for s in states:
        #     print('\t' + s.state)
        # print(providerState)
        # print('PACT HELPER SETUP')
        # print('EXECUTE STATE')
        # print('CREATE REQUEST')
        # print('EXECUTE REQUEST')
        # print('VERIFY RESPONSE')
        # print('PACT HELPER TEAR DOWN')
        pass

    @staticmethod
    def get_pact(location):         # pragma: no cover
        return get_pact(location)   # pragma: no cover

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
                    if test_parent == 'ServiceConsumerTest':
                        tests.append(obj)

        if not files:
            return Left(MISSING_TESTS)
        return Right(tests)

    def all_files(self):
        return os.listdir(self.config.consumer_tests_path)


def filter_rule(filename):
    return (filename != '__init__.py' and
            filename.endswith('.py') and
            filename.endswith('pact_helper.py') is False)

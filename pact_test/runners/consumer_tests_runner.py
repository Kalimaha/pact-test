import os
import imp
import inspect
from pact_test.constants import *
from pact_test.exceptions import PactTestException
from pact_test.utils.pact_utils import get_pact


class ConsumerTestsRunner(object):
    pact_helper = None

    def __init__(self, config):
        self.config = config

    def verify(self):
        pass

    def verify_test(self, test_class):
        test = test_class()
        test.validate()
        pact = self.get_pact(test.pact_uri)

        pact_states = list(map(lambda i: i['providerState'], pact['interactions']))
        test_states = list(map(lambda s: s.state, test.states))

        for pact_state in pact_states:
            if pact_state not in test_states:
                msg = MISSING_STATE + '"' + pact_state + '".'
                raise PactTestException(msg)
            self.verify_state(test.states, pact_state)

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
            raise PactTestException(MISSING_TESTS)
        return tests

    def all_files(self):
        return os.listdir(self.config.consumer_tests_path)

    def load_pact_helper(self):
        self.pact_helper = imp.load_source('pact_helper', self.path_to_pact_helper())
        if hasattr(self.pact_helper, 'setup') is False:
            raise PactTestException(MISSING_SETUP)
        if hasattr(self.pact_helper, 'tear_down') is False:
            raise PactTestException(MISSING_TEAR_DOWN)

    def path_to_pact_helper(self):
        path = os.path.join(self.config.consumer_tests_path, 'pact_helper.py')
        if os.path.isfile(path) is False:
            msg = MISSING_PACT_HELPER + self.config.consumer_tests_path + '".'
            raise PactTestException(msg)
        return path


def filter_rule(filename):
    return (filename != '__init__.py' and
            filename.endswith('.py') and
            filename.endswith('pact_helper.py') is False)

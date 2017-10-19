import os
import imp
import inspect
from pact_test.either import *
from pact_test.constants import *
from pact_test.utils.logger import error
from pact_test.utils.logger import debug
from pact_test.models.response import PactResponse
from pact_test.servers.mock_server import MockServer


class ServiceProviderTestSuiteRunner(object):
    def __init__(self, config):
        self.config = config
        debug(config)
        debug(self.config.provider_tests_path)

    def verify(self):
        debug('Verify providers: START')
        tests = self.collect_tests()
        if type(tests) is Right:
            debug(str(len(tests.value)) + ' test(s) found.')
            for test in tests.value:
                test_verification = test.is_valid()
                if type(test_verification) is Right:
                    for decorated_method in test.decorated_methods:
                        mock_response = self.build_expected_response(decorated_method)
                        mock_server = MockServer(mock_response=mock_response, port=9999)
                        mock_server.start()
                        debug('Server is running')
                        decorated_method()
                        mock_server.shutdown()
                        report = mock_server.report()
                        if len(report) == 0:
                            error('Verify providers: EXIT WITH ERRORS:')
                            error('  No request made for ' + str(decorated_method.__name__))
                            return Left('No request made for ' + str(decorated_method.__name__))
                error('Verify providers: EXIT WITH ERRORS:')
                error(test_verification.value)
        error('Verify providers: EXIT WITH ERRORS:')
        error(tests.value)
        return tests

    @staticmethod
    def build_expected_response(decorated_method):
        return PactResponse(
            body=decorated_method.will_respond_with.get('body'),
            status=decorated_method.will_respond_with.get('status'),
            headers=decorated_method.will_respond_with.get('headers')
        )

    def collect_tests(self):
        root = self.config.provider_tests_path
        debug(self.config)
        debug(root)
        files = list(filter(self.filter_rule, self.all_files()))
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

    @staticmethod
    def filter_rule(filename):
        return filename != '__init__.py' and filename.endswith('.py')

    def all_files(self):
        return os.listdir(self.config.provider_tests_path)

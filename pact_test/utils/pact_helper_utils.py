import os
import imp
import inspect
from pact_test.either import *
from pact_test import PactHelper
from pact_test.constants import MISSING_SETUP
from pact_test.constants import MISSING_TEAR_DOWN
from pact_test.constants import EXTEND_PACT_HELPER
from pact_test.constants import MISSING_PACT_HELPER


def load_pact_helper(consumer_tests_path):
    return _path_to_pact_helper(consumer_tests_path)\
               .concat(_load_module, 'pact_helper') \
               >> _load_user_class


def _load_user_class(user_module):
    user_class = None

    for name, obj in inspect.getmembers(user_module):
        if inspect.isclass(obj) and len(inspect.getmro(obj)) > 2 and issubclass(obj, PactHelper):
            user_class = obj()

    if user_class is None:
        return Left(EXTEND_PACT_HELPER)
    if hasattr(user_class, 'setup') is False:
        return Left(MISSING_SETUP)
    if hasattr(user_class, 'tear_down') is False:
        return Left(MISSING_TEAR_DOWN)

    return Right(user_class)


def _load_module(path, module_name):
    try:
        return Right(imp.load_source(module_name, path))
    except Exception:
        return Left(MISSING_PACT_HELPER + path + '".')


def _path_to_pact_helper(consumer_tests_path):
    path = os.path.join(consumer_tests_path, 'pact_helper.py')
    if os.path.isfile(path) is False:
        msg = MISSING_PACT_HELPER + consumer_tests_path + '".'
        return Left(msg)
    return Right(path)


def format_headers(pact):
    for interaction in pact.get('interactions', []):
        req_headers = interaction.get('request').get('headers')
        fixed_req_headers = {}
        for h in req_headers:
            fixed_req_headers.update(h)
        interaction['request']['headers'] = fixed_req_headers

        res_headers = interaction.get('response').get('headers')
        fixes_req_headers = {}
        for h in res_headers:
            fixes_req_headers.update(h)
        interaction['response']['headers'] = fixes_req_headers
    return pact

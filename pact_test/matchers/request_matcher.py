from pact_test.either import *
from pact_test.constants import FAILED


def match(actual, expected):
    return _match_path(actual, expected).concat(_match_query, expected).concat(_match_method, expected)


def _match_path(actual, expected):
    if actual.path == expected.path:
        return Right(actual)
    return Left(_build_error_message('path', expected.path, actual.path))


def _match_query(actual, expected):
    if actual.query == expected.query:
        return Right(actual)
    return Left(_build_error_message('query', expected.query, actual.query))


def _match_method(actual, expected):
    if actual.method.upper() == expected.method.upper():
        return Right(actual)
    return Left(_build_error_message('method', expected.method.upper(), actual.method.upper()))


def _build_error_message(section, expected, actual):
    return {
        'actual': actual,
        'status': FAILED,
        'expected': expected,
        'message': section.capitalize() + ' is incorrect'
    }

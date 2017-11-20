from pact_test.either import *
from pact_test.utils.logger import *
from pact_test.matchers.matcher import *
try:
    import urllib.parse as parse
except ImportError:
    import urllib as parse


def match(actual, expected):
    return _match_path(actual, expected)\
        .concat(_match_query, expected)\
        .concat(_match_method, expected)\
        .concat(_match_headers, expected)\
        .concat(_match_body, expected)


def _match_body(actual, expected):
    expected_body = expected.body
    actual_body = actual.body

    if expected_body is None and actual_body is None:
        return Right(actual)

    if is_string(expected_body) and is_string(actual_body) and expected_body == actual_body:
        return Right(actual)

    if type(expected_body) is dict \
            and type(actual_body) is dict \
            and _match_dicts_all_keys_and_values(expected_body.copy(), actual_body.copy()):
            return Right(actual)

    return Left(build_error_message('body', expected_body, actual_body))


def _match_dicts_all_keys_and_values(d1, d2):
    d1_keys = d1.keys()
    d2_keys = d2.keys()

    all_keys = set(d2_keys).issubset(set(d1_keys))
    all_values = match_dicts_all_values(d1, d2)

    return all_keys and all_values


def _match_headers(actual, expected):
    actual_dict = dict(pair for d in actual.headers for pair in sorted(d.items()))
    expected_dict = dict(pair for d in expected.headers for pair in sorted(d.items()))

    insensitive_actual = {k.upper(): v for (k, v) in sorted(actual_dict.items())}
    insensitive_expected = {k.upper(): v for (k, v) in sorted(expected_dict.items())}

    if is_subset(insensitive_expected, insensitive_actual):
        return Right(actual)
    return Left(build_error_message('headers', expected.headers, actual.headers))


def _match_path(actual, expected):
    if actual.path == expected.path:
        return Right(actual)
    return Left(build_error_message('path', expected.path, actual.path))


def _match_query(actual, expected):
    if _encode(actual.query) == _encode(expected.query):
        return Right(actual)
    return Left(build_error_message('query', expected.query, actual.query))


def _encode(str):
    return parse.quote(str, safe="%3D")


def _match_method(actual, expected):
    if actual.method.upper() == expected.method.upper():
        return Right(actual)
    return Left(build_error_message('method', expected.method.upper(), actual.method.upper()))

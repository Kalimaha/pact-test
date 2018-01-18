from pact_test.either import *
from pact_test.matchers.matcher import *


def match(interaction, pact_response):
    return _match_status(interaction, pact_response)\
        .concat(_match_headers, pact_response)\
        .concat(_match_body, pact_response)


def _match_status(interaction, pact_response):
    expected = interaction['response'].get('status')
    actual = pact_response.status

    if expected is None or actual == expected:
        return Right(interaction)
    return Left(build_error_message('status', expected, actual))


def _match_headers(interaction, pact_response):
    expected = interaction['response'].get('headers', {})
    actual = _to_dict(pact_response.headers)

    insensitive_expected = {k.upper(): v for (k, v) in expected.items()}
    insensitive_actual = {k.upper(): v for (k, v) in actual.items()}

    if is_subset(insensitive_expected, insensitive_actual):
        return Right(interaction)
    return Left(build_error_message('headers', expected, actual))


def _match_body(interaction, pact_response):
    expected = interaction['response'].get('body')
    actual = pact_response.body

    if expected is None and actual is None:
        return Right(interaction)

    if is_string(expected) and is_string(actual) and expected == actual:
        return Right(interaction)

    if type(expected) is dict and type(actual) is dict and match_dicts_all_keys_and_values(expected, actual):
            return Right(interaction)

    return Left(build_error_message('body', expected, actual))


def _to_dict(headers):
    d = {}
    for h in headers:
        d[h[0]] = h[1]
    return d

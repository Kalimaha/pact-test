from pact_test.either import *
from pact_test.constants import FAILED


def match(interaction, pact_response):
    return _match_status(interaction, pact_response)\
        .concat(_match_headers, pact_response)\
        .concat(_match_body, pact_response)


def _match_status(interaction, pact_response):
    expected = interaction['response'].get('status')
    actual = pact_response.status

    if expected is None or actual == expected:
        return Right(interaction)
    return Left(_build_error_message('status', expected, actual))


def _match_headers(interaction, pact_response):
    expected = interaction['response'].get('headers', {})
    actual = _to_dict(pact_response.headers)

    insensitive_expected = {k.upper(): v for (k, v) in expected.items()}
    insensitive_actual = {k.upper(): v for (k, v) in actual.items()}

    if _is_subset(insensitive_expected, insensitive_actual):
        return Right(interaction)
    return Left(_build_error_message('headers', expected, actual))


def _match_body(interaction, pact_response):
    expected = interaction['response'].get('body')
    actual = pact_response.body

    if _is_subset(expected, actual):
        return Right(interaction)
    return Left(_build_error_message('body', expected, actual))


def _to_dict(headers):
    d = {}
    for h in headers:
        d[h[0]] = h[1]
    return d


def _build_error_message(section, expected, actual):
    return {
        'actual': actual,
        'status': FAILED,
        'expected': expected,
        'message': section.capitalize() + ' is incorrect'
    }


def _is_subset(expected, actual):
    actual_items = actual.items() if actual else {}
    expected_items = expected.items() if expected else {}

    stripped_actual_items = map(_strip_whitespaces_after_commas, actual_items)
    stripped_expected_items = map(_strip_whitespaces_after_commas, expected_items)

    return all(item in stripped_actual_items for item in stripped_expected_items)


def _strip_whitespaces_after_commas(t):
    k = t[0]
    v = t[1].replace(', ', ',') if type(t[1]) is str else t[1]

    return k, v

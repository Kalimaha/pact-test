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

    if expected is None and actual is None:
        return Right(interaction)

    try:
        if (type(expected) is str or type(expected) is unicode) and type(actual) is str and expected == actual:
            return Right(interaction)
    except NameError:
        if type(expected) is str and type(actual) is str and expected == actual:
            return Right(interaction)

    if type(expected) is dict and type(actual) is dict:
        if _match_dicts(expected, actual):
            return Right(interaction)

    return Left(_build_error_message('body', expected, actual))


def _match_dicts(expected, actual):
    expected_keys = expected.keys()
    actual_keys = actual.keys()
    all_keys = set(actual_keys).issubset(set(expected_keys))

    all_values = True
    for (k1, v1), (k2, v2) in zip(sorted(actual.items()), sorted(expected.items())):
        all_values = all_values and (v1 == v2)

    return all_keys and all_values


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

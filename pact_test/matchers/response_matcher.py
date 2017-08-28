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

    if _is_string(expected) and _is_string(actual) and expected == actual:
        return Right(interaction)

    if type(expected) is dict and type(actual) is dict and _match_dicts_all_keys_and_values(expected, actual):
            return Right(interaction)

    return Left(_build_error_message('body', expected, actual))


def _is_string(text):
    try:
        return True if (type(text) is str or type(text) is unicode) else False
    except NameError:
        return True if type(text) is str else False


def _match_dicts_all_keys_and_values(d1, d2):
    d1_keys = d1.keys()
    d2_keys = d2.keys()

    _delete_extra_keys(d1, d2)

    all_keys = set(d2_keys).issubset(set(d1_keys))
    all_values = _match_dicts_all_values(d1, d2)

    return all_keys and all_values


def _match_dicts_all_values(d1, d2):
    all_values = True
    for (k1, v1), (k2, v2) in zip(sorted(d2.items()), sorted(d1.items())):
        all_values = all_values and (v1 == v2)
    return all_values


def _delete_extra_keys(d1, d2):
    extra_keys = list(set(d2.keys()) - set(d1.keys()))
    for extra_key in extra_keys:
        d2.pop(extra_key, None)
    for (k1, v1), (k2, v2) in zip(sorted(d1.items()), sorted(d2.items())):
        if type(v1) is dict and type(v2) is dict:
            _delete_extra_keys(v1, v2)


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

from pact_test.either import *


def match(interaction, pact_response):
    return _match_status(interaction, pact_response)\
        .concat(_match_headers, pact_response)\
        .concat(_match_body, pact_response)


def _match_status(interaction, pact_response):
    expected = interaction['response'].get('status')
    actual = pact_response.status

    if actual == expected:
        return Right(interaction)
    return Left(_build_error_message('status', expected, actual))


def _match_headers(interaction, pact_response):
    expected = interaction['response'].get('headers')
    actual = _to_dict(pact_response.headers)

    if _is_subset(expected, actual):
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
    return 'Non-matching ' + section + ' for the response. Expected:\n\n\t' + \
           str(expected) + '\n\nReceived:\n\n\t' + str(actual)


def _is_subset(expected, actual):
    actual_items = actual.items() if actual else {}
    expected_items = expected.items() if expected else {}

    return all(item in expected_items for item in actual_items)

from pact_test.either import *


def match(expected, actual):
    body = actual.data
    method = actual.method
    headers = actual.headers
    path = actual.selector[0:actual.selector.index('?')]
    query = actual.selector[actual.selector.index('?'):]

    return _match_query(expected, query)\
        .concat(_match_path, path)\
        .concat(_match_method, method)\
        .concat(_match_body, body)\
        .concat(_match_headers, headers)


def _match_body(expected, actual):
    matching_texts = actual == expected['body']
    same_type = type(expected['body']) == type(actual)
    matching_dicts = type(actual) is dict and _is_subset(actual, expected['body'])

    if same_type and (matching_dicts or matching_texts):
        return Right(expected)
    return Left(_build_error_message('body', expected['body'], actual))


def _match_query(expected, actual):
    if actual == expected['query']:
        return Right(expected)
    return Left(_build_error_message('query', expected['query'], actual))


def _match_path(expected, actual):
    if actual == expected['path']:
        return Right(expected)
    return Left(_build_error_message('path', expected['path'], actual))


def _match_method(expected, actual):
    if actual == expected['method']:
        return Right(expected)
    return Left(_build_error_message('method', expected['method'], actual))


def _match_headers(expected, actual):
    if _is_subset(actual, expected['headers']):
        return Right(expected)
    return Left(_build_error_message('headers', expected['headers'], actual))


def _build_error_message(section, expected, actual):
    return 'Non-matching ' + section + ' for the request. Expected:\n\n\t' + \
           str(expected) + '\n\nReceived:\n\n\t' + str(actual)


def _is_subset(expected, actual):
    return all(item in expected.items() for item in actual.items())

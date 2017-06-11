from pact_test.either import *
from pact_test.matchers.request_matcher import match
try:                                                    # pragma: no cover
    from urllib.request import Request, urlopen         # pragma: no cover
except:                                                 # pragma: no cover
    from urllib2 import Request, urlopen                # pragma: no cover


expected = {
    'method': 'GET',
    'path': '/books/42',
    'query': '?format=hardcover',
    'headers': {'Content-type': 'application/json'},
    'body': {'title': 'The Hitchhicker\'s Guide to the Galaxy'}
}


def build_request():
    request = Request('http://localhost')
    request.method = 'POST'
    request.selector = '/movies?format=PAL'
    request.add_header('Content', 'silly')
    request.data = {'title': 'A Fortune-Teller Told Me'}
    return request


def test_non_matching_query():
    request = build_request()
    msg = 'Non-matching query for the request. Expected:\n\n\t' + \
          str(expected['query']) + '\n\nReceived:\n\n\t' + '?format=PAL'
    assert match(expected, request).value == msg


def test_non_matching_path():
    request = build_request()
    request.selector = '/movies?format=hardcover'
    msg = 'Non-matching path for the request. Expected:\n\n\t' + \
          str(expected['path']) + '\n\nReceived:\n\n\t' + '/movies'
    assert match(expected, request).value == msg


def test_non_matching_method():
    request = build_request()
    request.selector = '/books/42?format=hardcover'
    msg = 'Non-matching method for the request. Expected:\n\n\t' + \
          str(expected['method']) + '\n\nReceived:\n\n\t' + 'POST'
    assert match(expected, request).value == msg


def test_non_matching_dict_body():
    request = build_request()
    request.selector = '/books/42?format=hardcover'
    request.method = 'GET'
    msg = 'Non-matching body for the request. Expected:\n\n\t' + \
          str(expected['body']) + '\n\nReceived:\n\n\t' + \
          str({'title': 'A Fortune-Teller Told Me'})
    assert match(expected, request).value == msg


def test_non_matching_text_body():
    request = build_request()
    request.selector = '/books/42?format=hardcover'
    request.method = 'GET'
    request.data = 'Spam & Eggs'
    expected['body'] = 'Eggs and Bacon'
    msg = 'Non-matching body for the request. Expected:\n\n\t' + \
          str(expected['body']) + '\n\nReceived:\n\n\t' + \
          'Spam & Eggs'
    assert match(expected, request).value == msg


def test_non_matching_headers():
    request = build_request()
    request.selector = '/books/42?format=hardcover'
    request.method = 'GET'
    request.data = {'title': 'The Hitchhicker\'s Guide to the Galaxy'}
    expected['body'] = {'title': 'The Hitchhicker\'s Guide to the Galaxy'}
    msg = 'Non-matching headers for the request. Expected:\n\n\t' + \
          str(expected['headers']) + '\n\nReceived:\n\n\t' + \
          str({'Content': 'silly'})
    assert match(expected, request).value == msg


def test_matching_request():
    request = build_request()
    request.selector = '/books/42?format=hardcover'
    request.method = 'GET'
    request.data = {'title': 'The Hitchhicker\'s Guide to the Galaxy'}
    request.add_header('Content-Type', 'application/json')
    assert type(match(expected, request)) is Right

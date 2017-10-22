import requests
from pact_test.models.service_provider_test import *
from pact_test.runners.service_providers.request_test import verify_request


def test_missing_request():
    port = 9998

    class MyTest(ServiceProviderTest):
        @given('spam')
        @upon_receiving('eggs')
        @with_request({'method': 'get', 'path': '/books/42/'})
        @will_respond_with({'status': 200})
        def test_get_book(self):
            pass

    t = MyTest()
    decorated_method = next(t.decorated_methods)
    test_result = verify_request(decorated_method, port)
    expected_error_message = 'Missing request(s) for "given spam, ' \
                             'upon receiving eggs"'

    assert type(test_result) is Left
    assert test_result.value == expected_error_message


def test_non_matching_http_method():
    port = 9997
    url = 'http://localhost:' + str(port) + '/books/42/'

    class MyTest(ServiceProviderTest):
        @given('spam')
        @upon_receiving('eggs')
        @with_request({'method': 'get', 'path': '/books/42/'})
        @will_respond_with({'status': 200})
        def test_get_book(self):
            requests.post(url, data='{}')

    t = MyTest()
    decorated_method = next(t.decorated_methods)
    test_result = verify_request(decorated_method, port)
    expected_error_message = {
        'actual': 'POST',
        'expected': 'GET',
        'message': 'Method is incorrect',
        'status': 'FAILED'
    }

    assert type(test_result) is Left
    assert test_result.value == expected_error_message


def test_non_matching_path():
    port = 9996
    url = 'http://localhost:' + str(port) + '/books/4242/'

    class MyTest(ServiceProviderTest):
        @given('spam')
        @upon_receiving('eggs')
        @with_request({'method': 'get', 'path': '/books/42/'})
        @will_respond_with({'status': 200})
        def test_get_book(self):
            requests.get(url)

    t = MyTest()
    decorated_method = next(t.decorated_methods)
    test_result = verify_request(decorated_method, port)
    expected_error_message = {
        'actual': '/books/4242/',
        'expected': '/books/42/',
        'message': 'Path is incorrect',
        'status': 'FAILED'
    }

    assert type(test_result) is Left
    assert test_result.value == expected_error_message


def test_non_matching_query():
    port = 9995
    url = 'http://localhost:' + str(port) + '/q?spam=eggs'

    class MyTest(ServiceProviderTest):
        @given('spam')
        @upon_receiving('eggs')
        @with_request({'method': 'get', 'path': '/q', 'query': '?eggs=bacon'})
        @will_respond_with({'status': 200})
        def test_get_book(self):
            requests.get(url)

    t = MyTest()
    decorated_method = next(t.decorated_methods)
    test_result = verify_request(decorated_method, port)
    expected_error_message = {
        'actual': '?spam=eggs',
        'expected': '?eggs=bacon',
        'message': 'Query is incorrect',
        'status': 'FAILED'
    }

    assert type(test_result) is Left
    assert test_result.value == expected_error_message


def test_non_matching_headers():
    port = 9994
    url = 'http://localhost:' + str(port) + '/'
    headers = [{'Content-Type': 'application/json'}]

    class MyTest(ServiceProviderTest):
        @given('spam')
        @upon_receiving('eggs')
        @with_request({'method': 'get', 'path': '/', 'headers': headers})
        @will_respond_with({'status': 200})
        def test_get_book(self):
            requests.get(url, headers={'spam': 'eggs'})

    t = MyTest()
    decorated_method = next(t.decorated_methods)
    test_result = verify_request(decorated_method, port)
    expected_error_message = {}

    # assert type(test_result) is Left
    # assert test_result.value == expected_error_message

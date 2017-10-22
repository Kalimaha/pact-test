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
    expected_error_message = 'HTTP methods do not match. ' \
                             'Expected "GET", got "POST".'

    assert type(test_result) is Left
    assert test_result.value == expected_error_message

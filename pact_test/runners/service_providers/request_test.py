from pact_test.either import *
from pact_test.utils.logger import debug
from pact_test.models.request import PactRequest
from pact_test.models.response import PactResponse
from pact_test.servers.mock_server import MockServer


def verify_request(decorated_method, port=9999):
    mock_response = build_expected_response(decorated_method)
    expected_request = build_expected_request(decorated_method)
    mock_server = MockServer(mock_response=mock_response, port=port)
    mock_server.start()
    debug('Server is running')
    decorated_method()
    mock_server.shutdown()
    report = mock_server.report()
    if len(report) is 0:
        return Left('Missing request(s) for "' +
                    format_message(decorated_method) + '"')
    actual_request = build_actual_request(report[0])
    return requests_match(expected_request, actual_request)


def requests_match(expected, actual):
    if expected.method.upper() != actual.method.upper():
        return Left('HTTP methods do not match. Expected "' +
                    expected.method.upper() +
                    '", got "' + actual.method.upper() + '".')


def build_expected_response(decorated_method):
    return PactResponse(
        body=decorated_method.will_respond_with.get('body'),
        status=decorated_method.will_respond_with.get('status'),
        headers=decorated_method.will_respond_with.get('headers')
    )


def build_expected_request(decorated_method):
    return PactRequest(
        method=decorated_method.with_request.get('method'),
        body=decorated_method.with_request.get('body'),
        headers=decorated_method.with_request.get('headers'),
        path=decorated_method.with_request.get('path'),
        query=decorated_method.with_request.get('query')
    )


def build_actual_request(request):
    return PactRequest(
        path=request.get('path'),
        query=request.get('query'),
        method=request.get('http_method'),
        body=request.get('data'),
        headers=request.get('headers')
    )


def format_message(decorated_method):
    return 'given ' + \
           decorated_method.given + \
           ', upon receiving ' + \
           decorated_method.upon_receiving

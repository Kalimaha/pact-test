import json
from pact_test.either import *
from pact_test.utils.logger import *
from pact_test.models.request import PactRequest
from pact_test.models.response import PactResponse
from pact_test.servers.mock_server import MockServer
from pact_test.matchers.request_matcher import match


def verify_request(decorated_method, port=9999):
    mock_response = build_expected_response(decorated_method)
    expected_request = build_expected_request(decorated_method)

    mock_server = MockServer(mock_response=mock_response, port=port)
    mock_server.start()
    decorated_method()
    mock_server.shutdown()
    report = mock_server.report()

    if len(report) is 0:
        out = {
            'status': 'FAILED',
            'providerState': decorated_method.given,
            'description': decorated_method.upon_receiving,
            'message': 'Missing request(s) for "' + format_message(decorated_method) + '"',
            'expected': expected_request.__dict__,
            'actual': None
        }
        return Left(out)

    actual_request = build_actual_request(report[0])
    matching_result = match(actual_request, expected_request)

    if type(matching_result) is Right:
        resp = mock_response.__dict__
        resp['body'] = json.loads(mock_response.__dict__['body'])
        out = {
            'status': 'PASSED',
            'providerState': decorated_method.given,
            'description': decorated_method.upon_receiving,
            'request': actual_request.__dict__,
            'response': resp
        }
        return Right(out)
    else:
        reason = matching_result.value.copy()
        reason.update({
            'providerState': decorated_method.given,
            'description': decorated_method.upon_receiving
        })
        return Left(reason)


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
        method=request.get('method'),
        body=request.get('body'),
        headers=request.get('headers')
    )


def format_message(decorated_method):
    return 'given ' + \
           decorated_method.given + \
           ', upon receiving ' + \
           decorated_method.upon_receiving

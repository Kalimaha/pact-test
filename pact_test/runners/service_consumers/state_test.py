import json
from pact_test.either import *
try:                                                    # pragma: no cover
    from urllib.request import Request, urlopen         # pragma: no cover
except:                                                 # pragma: no cover
    from urllib2 import Request, urlopen                # pragma: no cover


def verify_state(interaction, pact_helper, test_instance):
    pact_helper.setup()
    request = _create_request(pact_helper.test_url, pact_helper.test_port, interaction['request'])
    if type(request) is Right:
        response = _parse_response(request.value)
    pact_helper.tear_down()
    return Right(_build_test_result())


def _verify_request(expected_request, request):
    pass


def _create_request(url, port, request_body):
    request_port = '80' if port is None else str(port)
    request_url = 'http://' + url + ':' + request_port

    request = Request(request_url)
    request.method = request_body['method']
    request.selector = request_body['path'] + request_body['query']
    request_headers = request_body.get('headers', {})
    for header in request_headers:
        request.add_header(header, request_headers[header])
    return Right(request)


def _parse_response(request):
    try:
        response = urlopen(request)
        response_body = response.read()
        response_type = _get_response_type(response).value
        if 'application/json' in response_type:
            return Right(json.loads(response_body))
        return Right(str(response_body.decode('utf-8')))
    except Exception as e:
        return Left(str(e))


def _get_response_type(response):                           # pragma: no cover
    try:                                                    # pragma: no cover
        return Right(response.getheader('Content-type'))    # pragma: no cover
    except:                                                 # pragma: no cover
        return Right(response.headers['Content-Type'])      # pragma: no cover


def _build_test_result(status='PASSED', reason=None):
    return {'status': status, 'reason': reason}

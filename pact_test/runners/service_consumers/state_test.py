from pact_test.either import *
try:
    from urllib.request import Request, urlopen
except:
    from urllib2 import Request, urlopen


def verify_state(interaction, pact_helper, test_instance):
    pact_helper.set_up()
    pact_helper.tear_down()
    return Right(build_test_result())


def create_request(request_body):
    request = Request('http://demo7688835.mockable.io')
    request.method = request_body['method']
    request.selector = request_body['path'] + request_body['query']
    request_headers = request_body.get('headers', {})
    for header in request_headers:
        request.add_header(header, request_headers[header])
    return request


def build_test_result(status='PASSED', reason=None):
    return {'status': status, 'reason': reason}

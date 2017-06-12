import json
from pact_test.models.response import PactResponse

from pact_test.utils.http_utils import build_request_from_interaction
try:                                                # pragma: no cover
    from urllib.request import Request, urlopen     # pragma: no cover
except:                                             # pragma: no cover
    from urllib2 import Request, urlopen            # pragma: no cover


TEXT = 'text'


def execute_interaction_request(url, port, interaction):
    request = _pact2python_request(url, port, interaction)
    return _python2pact_response(urlopen(request))


def _python2pact_response(response):
    status = _parse_status(response)
    headers = _parse_headers(response)
    content_type = _get_content_type(headers)

    return PactResponse(
        headers=headers,
        status=status,
        body=_parse_body(response, content_type)
    )


def _parse_status(response):
    try:
        status = response.status
    except AttributeError:
        status = response.code
    return status


def _parse_headers(response):
    try:
        headers = response.getheaders()
    except AttributeError:
        headers = []
        for h in response.headers.headers:
            key_value = h.split(':')
            key = key_value[0].strip()
            val = key_value[1].strip()
            headers.append((key, val))
    return headers


def _parse_body(response, content_type):
    body = response.read().decode('utf-8')
    if content_type == TEXT:
        return body
    return json.loads(body)


def _get_content_type(headers):
    content_type = TEXT
    types = list(filter(lambda h: h[0].upper() == 'CONTENT-TYPE', headers))
    if types:
        content_type = types[0][1]
    return content_type


def _pact2python_request(url, port, interaction):
    pact_request = build_request_from_interaction(interaction)

    request_port = str(port) if port else '80'
    request_url = 'http://' + url + ':' + request_port

    request = Request(request_url)
    request.data = bytearray().extend(map(ord, json.dumps(pact_request.body)))
    request.method = pact_request.method
    for key, value in pact_request.headers:
        request.add_header(key, value)
    request.selector = pact_request.path + pact_request.query

    return request

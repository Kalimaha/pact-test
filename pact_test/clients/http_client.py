import requests
from pact_test.either import *
from pact_test.constants import *
from pact_test.models.response import PactResponse


def execute_interaction_request(url, port, interaction):
    url = _build_url(url, port, interaction)
    method = interaction[REQUEST].get('method', 'GET')
    server_response = _server_response(method, url=url)

    if type(server_response) is Right:
        headers = _parse_headers(server_response.value)
        content_type = _get_content_type(headers)
        return Right(PactResponse(
            status=server_response.value.status_code,
            headers=headers,
            body=_parse_body(server_response.value, content_type)
        ))

    return server_response


def _server_response(method, url):
    try:
        return Right(requests.request(method, url=url))
    except Exception as e:
        return Left(str(e))


def _parse_body(server_response, content_type):
    if JSON in content_type:
        return server_response.json()
    else:
        return server_response.text()


def _parse_headers(server_response):
    headers = []
    server_headers = server_response.headers or []
    for key in server_headers:
        headers.append((key, server_headers[key]))
    return headers


def _build_url(url, port, interaction):
    path = interaction[REQUEST].get('path', '')
    query = interaction[REQUEST].get('query', '')

    test_port = str(port) if port else str(80)
    return 'http://' + url + ':' + test_port + path + query


def _get_content_type(headers):
    content_type = TEXT
    types = list(filter(lambda h: h[0].upper() == 'CONTENT-TYPE', headers))
    if types:
        content_type = types[0][1]
    return content_type

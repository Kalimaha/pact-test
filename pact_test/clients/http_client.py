import requests
from pact_test.models.response import PactResponse


TEXT = 'text'
JSON = 'application/json'


def execute_interaction_request(url, port, interaction):
    url = _build_url(url, port, interaction)

    server_response = requests.request('GET', url=url)
    headers = _parse_headers(server_response)
    content_type = _get_content_type(headers)

    return PactResponse(
        status=server_response.status_code,
        headers=headers,
        body=_parse_body(server_response, content_type)
    )


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
    path = interaction['request'].get('path', '')
    query = interaction['request'].get('query', '')

    test_port = str(port) if port else str(80)
    test_url = 'http://' + url + ':' + test_port + path + query

    return test_url


def _get_content_type(headers):
    content_type = TEXT
    types = list(filter(lambda h: h[0].upper() == 'CONTENT-TYPE', headers))
    if types:
        content_type = types[0][1]
    return content_type

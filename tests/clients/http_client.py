import requests
from pact_test.clients.http_client import _build_url
from pact_test.clients.http_client import _parse_headers
from pact_test.clients.http_client import execute_interaction_request


def test_execute_interaction_request(mocker):
    class Response(object):
        status_code = 200
        headers = {'Content-Type': 'application/json', 'Date': '12-06-2017'}

        def json(self):
            return {'spam': 'eggs'}

    mocker.patch.object(requests, 'request', lambda x, **kwargs: Response())
    url = 'montypython.com'
    port = None
    interaction = {'request': {'path': '/spam/eggs'}}
    response = execute_interaction_request(url, port, interaction)

    assert response.status == 200
    assert len(response.headers) > 1
    assert response.body == {'spam': 'eggs'}


def test_execute_interaction_request_text(mocker):
    class Response(object):
        status_code = 200
        headers = {'Date': '12-06-2017'}

        def text(self):
            return 'Spam & Eggs'

    mocker.patch.object(requests, 'request', lambda x, **kwargs: Response())
    url = 'montypython.com'
    port = None
    interaction = {'request': {'path': '/spam/eggs'}}
    response = execute_interaction_request(url, port, interaction)

    assert response.status == 200
    assert response.headers == [('Date', '12-06-2017')]
    assert response.body == 'Spam & Eggs'


def test_parse_headers():
    headers = [('Content-Type', 'spam')]
    server_headers = {'Content-Type': 'spam'}

    class Response(object):
        headers = server_headers

    assert _parse_headers(Response()) == headers


def test_build_url():
    url = 'montypython.com'
    port = None
    interaction = {'request': {}}
    url = _build_url(url, port, interaction)

    assert url == 'http://montypython.com:80'


def test_build_url_with_path():
    url = 'montypython.com'
    port = None
    interaction = {'request': {'path': '/spam/eggs'}}
    url = _build_url(url, port, interaction)

    assert url == 'http://montypython.com:80/spam/eggs'


def test_build_url_with_query():
    url = 'montypython.com'
    port = None
    interaction = {'request': {'query': '?spam=eggs'}}
    url = _build_url(url, port, interaction)

    assert url == 'http://montypython.com:80?spam=eggs'

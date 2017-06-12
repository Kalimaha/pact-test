import json
from pact_test.models.request import PactRequest
from pact_test.clients.http_client import _parse_body
from pact_test.clients.http_client import _get_content_type
from pact_test.clients.http_client import _pact2python_request
from pact_test.clients.http_client import execute_interaction_request
try:                                                    # pragma: no cover
    from urllib.request import Request, urlopen         # pragma: no cover
except:                                                 # pragma: no cover
    from urllib2 import Request, urlopen                # pragma: no cover


def test_execute_interaction_request(mocker):
    url = 'echo.jsontest.com'
    port = None
    interaction = {'request': {'path': '/spam/eggs'}}
    mocker.spy(PactRequest, '__init__')
    response = execute_interaction_request(url, port, interaction)

    assert PactRequest.__init__.call_count == 1
    assert response.status == 200
    assert len(response.headers) > 1
    assert response.body == {'spam': 'eggs'}


def test_get_content_type():
    headers = [
        ('Server', 'Spam'),
        ('Content-Type', 'application/json'),
        ('Date', '12-06-2017')
    ]
    content_type = _get_content_type(headers)

    assert content_type == 'application/json'


def test_get_default_content_type():
    headers = [
        ('Server', 'Spam'),
        ('Date', '12-06-2017')
    ]
    content_type = _get_content_type(headers)

    assert content_type == 'text'


def test_pact2python_request():
    url = 'localhost'
    port = 9999
    body = {'spam': 'eggs'}
    headers = {'Content-type': 'spam', 'Date': 'today'}
    interaction = {
        'request': {
            'method': 'POST',
            'path': '/spam',
            'query': '?spam=eggs',
            'body': body,
            'headers': headers
        }
    }
    request = _pact2python_request(url, port, interaction)
    assert request.method == 'POST'
    assert request.selector == '/spam?spam=eggs'
    assert request.headers == headers
    assert request.data == bytearray().extend(map(ord, json.dumps(body)))

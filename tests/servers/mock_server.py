import requests
from pact_test.models.response import PactResponse
from pact_test.servers.mock_server import MockServer


def test_response_with_headers():
    r = PactResponse(headers=[{'spam': 'eggs'}])
    s = MockServer(port=1234, mock_response=r)
    s.start()
    response = requests.get('http://localhost:1234/')
    s.shutdown()
    stored_request = s.report()[0]
    custom_header = False
    for h in response.headers:
        if 'spam' in h:
            custom_header = True
    assert custom_header is True


def test_no_requests():
    s = MockServer()
    s.start()
    s.shutdown()
    assert s.report() == []


def test_get_request():
    s = MockServer(port=1235)
    s.start()
    requests.get('http://localhost:1235/')
    s.shutdown()
    stored_request = s.report()[0]
    assert stored_request['method'] == 'GET'
    assert stored_request['path'] == '/'
    assert stored_request['body'] is None


def test_post_request():
    s = MockServer(port=1236)
    s.start()
    requests.post('http://localhost:1236/', data='{"spam": "eggs"}')
    s.shutdown()
    stored_request = s.report()[0]
    assert stored_request['method'] == 'POST'
    assert stored_request['path'] == '/'
    assert stored_request['body'] == {'spam': 'eggs'}


def test_put_request():
    s = MockServer(port=1237)
    s.start()
    requests.put('http://localhost:1237/', data='{"spam": "eggs"}')
    s.shutdown()
    stored_request = s.report()[0]
    assert stored_request['method'] == 'PUT'
    assert stored_request['path'] == '/'
    assert stored_request['body'] == {'spam': 'eggs'}


def test_delete_request():
    s = MockServer(port=1238)
    s.start()
    requests.delete('http://localhost:1238/', data='{"spam": "eggs"}')
    s.shutdown()
    stored_request = s.report()[0]
    assert stored_request['method'] == 'DELETE'
    assert stored_request['path'] == '/'
    assert stored_request['body'] == {'spam': 'eggs'}

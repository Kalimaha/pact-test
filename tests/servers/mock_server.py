import requests
from pact_test.servers.mock_server import MockServer


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
    assert stored_request['http_method'] == 'GET'
    assert stored_request['path'] == '/'
    assert stored_request['data'] is None


def test_post_request():
    s = MockServer(port=1236)
    s.start()
    requests.post('http://localhost:1236/', data='{"spam": "eggs"}')
    s.shutdown()
    stored_request = s.report()[0]
    assert stored_request['http_method'] == 'POST'
    assert stored_request['path'] == '/'
    assert stored_request['data'] == {'spam': 'eggs'}


def test_put_request():
    s = MockServer(port=1237)
    s.start()
    requests.put('http://localhost:1237/', data='{"spam": "eggs"}')
    s.shutdown()
    stored_request = s.report()[0]
    assert stored_request['http_method'] == 'PUT'
    assert stored_request['path'] == '/'
    assert stored_request['data'] == {'spam': 'eggs'}


def test_delete_request():
    s = MockServer(port=1238)
    s.start()
    requests.delete('http://localhost:1238/', data='{"spam": "eggs"}')
    s.shutdown()
    stored_request = s.report()[0]
    assert stored_request['http_method'] == 'DELETE'
    assert stored_request['path'] == '/'
    assert stored_request['data'] == {'spam': 'eggs'}

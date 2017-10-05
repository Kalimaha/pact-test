import pytest
from pact_test.constants import *
from pact_test.servers.mock_server import MockServer


def test_initialize_request():
    req = {
        'query': '?special_offer',
        'headers': {'Content-Type': 'application/json'},
        'body': {'id': 42},
        'path': '/items',
        'method': 'POST'
    }
    s = MockServer(req, {})

    assert s.request.__class__.__name__ == 'PactRequest'
    assert s.request.method == 'POST'
    assert s.request.body == {'id': 42}
    assert s.request.path == '/items'
    assert s.request.query == '?special_offer'


def test_initialize_response():
    res = {
        'status': 201,
        'headers': {'Content-Type': 'application/json'},
        'body': {'id': 42}
    }
    s = MockServer({}, res)

    assert s.response.__class__.__name__ == 'PactResponse'
    assert s.response.status == 201
    assert s.response.body == {'id': 42}
    assert s.response.headers == {'Content-Type': 'application/json'}


def test_empty_request():
    req = None
    res = {}

    with pytest.raises(Exception) as e:
        MockServer(req, res)

    assert str(e.value) == MISSING_REQUEST


def test_empty_response():
    req = {}
    res = None

    with pytest.raises(Exception) as e:
        MockServer(req, res)

    assert str(e.value) == MISSING_RESPONSE


def test_flask_app():
    req = {}
    res = {}
    s = MockServer(req, res)

    assert s.app is not None
    assert s.app.__class__.__name__ == 'Flask'


def test_endpoint():
    req = {'path': '/test_path'}
    s = MockServer(req, {})

    rules = list(s.app.url_map.iter_rules())

    assert rules[0].rule == '/test_path'
    assert rules[0].endpoint == 'spy'
    assert rules[0].methods == {'GET', 'HEAD', 'OPTIONS'}


def test_matching_request():
    req = {}
    res = {
        'body': {'id': 42},
        'status': 201,
        'headers': {'Content-Type': 'application/json'}
    }
    s = MockServer(req, res)

    assert s.spy().response == res['body']
    assert s.spy().status_code == 201
    assert s.spy().headers['Content-Type'] == 'application/json'


def test_non_matching_request():
    class FailingMockServer(MockServer):
        def is_matching_request(self):
            return False

    req = {}
    res = {}
    s = FailingMockServer(req, res)
    expected_message = 'Request is not matching the expectation'

    with s.app.test_request_context():
        assert s.spy().status_code == 500
        assert s.spy().response['message'] == expected_message
        assert type(s.spy().response['expected']) is dict
        assert type(s.spy().response['actual']) is dict

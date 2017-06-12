from pact_test.models.request import PactRequest


def test_default_body():
    r = PactRequest()
    assert r.body is None


def test_default_headers():
    r = PactRequest()
    assert r.headers == []


def test_default_method():
    r = PactRequest()
    assert r.method == 'GET'


def test_default_path():
    r = PactRequest()
    assert r.path == ''


def test_default_query():
    r = PactRequest()
    assert r.query == ''


def test_custom_query():
    r = PactRequest(query='?type=spam')
    assert r.query == '?type=spam'

    r.query = '?type=eggs'
    assert r.query == '?type=eggs'


def test_custom_path():
    r = PactRequest(path='/spam/')
    assert r.path == '/spam/'

    r.path = '/eggs/'
    assert r.path == '/eggs/'


def test_custom_method():
    r = PactRequest(method='POST')
    assert r.method == 'POST'

    r.method = 'PUT'
    assert r.method == 'PUT'


def test_custom_headers():
    headers = [('Content-Type', 'text')]
    r = PactRequest(headers=headers)
    assert r.headers == headers

    headers = [('Content-Type', 'application/json')]
    r.headers = headers
    assert r.headers == headers


def test_custom_body():
    body = {'spam': 'eggs'}
    r = PactRequest(body=body)
    assert r.body == body

    body = {'spam': 'spam'}
    r.body = body
    assert r.body == body

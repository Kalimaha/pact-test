from pact_test.utils.http import build_request_from_pact


def test_request_method():
    pact = {'request': {'method': 'POST'}}
    request = build_request_from_pact(pact)

    assert request.method == 'POST'


def test_request_missing_method():
    pact = {'request': {}}
    request = build_request_from_pact(pact)

    assert request.method == 'GET'


def test_request_path():
    pact = {'request': {'path': '/spam'}}
    request = build_request_from_pact(pact)

    assert request.path == '/spam'


def test_request_missing_path():
    pact = {'request': {}}
    request = build_request_from_pact(pact)

    assert request.path == ''


def test_request_query():
    pact = {'request': {'query': '?spam=eggs'}}
    request = build_request_from_pact(pact)

    assert request.query == '?spam=eggs'


def test_request_missing_query():
    pact = {'request': {}}
    request = build_request_from_pact(pact)

    assert request.query == ''


def test_request_headers():
    headers = {'Content-Type': 'application/json'}
    pact = {'request': {'headers': headers}}
    request = build_request_from_pact(pact)

    assert request.headers == [('Content-Type', 'application/json')]


def test_request_missing_headers():
    pact = {'request': {}}
    request = build_request_from_pact(pact)

    assert request.headers == []


def test_request_body():
    body = {'spam': 'eggs'}
    pact = {'request': {'body': body}}
    request = build_request_from_pact(pact)

    assert request.body == body


def test_request_missing_body():
    pact = {'request': {}}
    request = build_request_from_pact(pact)

    assert request.body is None

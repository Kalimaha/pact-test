from pact_test.utils.http import build_request_from_interaction
from pact_test.utils.http import build_response_from_interaction


def test_response_status():
    interaction = {'response': {'status': 200}}
    response = build_response_from_interaction(interaction)

    assert response.status == 200


def test_response_missing_status():
    interaction = {'response': {}}
    response = build_response_from_interaction(interaction)

    assert response.status == 500


def test_response_body():
    body = {'spam': 'eggs'}
    interaction = {'response': {'body': body}}
    response = build_response_from_interaction(interaction)

    assert response.body == body


def test_response_missing_body():
    interaction = {'response': {}}
    response = build_response_from_interaction(interaction)

    assert response.body is None


def test_response_headers():
    headers = {'Content-Type': 'spam'}
    interaction = {'response': {'headers': headers}}
    response = build_response_from_interaction(interaction)

    assert response.headers == [('Content-Type', 'spam')]


def test_response_missing_headers():
    interaction = {'response': {}}
    response = build_response_from_interaction(interaction)

    assert response.headers == []


def test_request_method():
    interaction = {'request': {'method': 'POST'}}
    request = build_request_from_interaction(interaction)

    assert request.method == 'POST'


def test_request_missing_method():
    interaction = {'request': {}}
    request = build_request_from_interaction(interaction)

    assert request.method == 'GET'


def test_request_path():
    interaction = {'request': {'path': '/spam'}}
    request = build_request_from_interaction(interaction)

    assert request.path == '/spam'


def test_request_missing_path():
    interaction = {'request': {}}
    request = build_request_from_interaction(interaction)

    assert request.path == ''


def test_request_query():
    interaction = {'request': {'query': '?spam=eggs'}}
    request = build_request_from_interaction(interaction)

    assert request.query == '?spam=eggs'


def test_request_missing_query():
    interaction = {'request': {}}
    request = build_request_from_interaction(interaction)

    assert request.query == ''


def test_request_headers():
    headers = {'Content-Type': 'application/json'}
    interaction = {'request': {'headers': headers}}
    request = build_request_from_interaction(interaction)

    assert request.headers == [('Content-Type', 'application/json')]


def test_request_missing_headers():
    interaction = {'request': {}}
    request = build_request_from_interaction(interaction)

    assert request.headers == []


def test_request_body():
    body = {'spam': 'eggs'}
    interaction = {'request': {'body': body}}
    request = build_request_from_interaction(interaction)

    assert request.body == body


def test_request_missing_body():
    interaction = {'request': {}}
    request = build_request_from_interaction(interaction)

    assert request.body is None

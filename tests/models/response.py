from pact_test.models.response import PactResponse


def test_default_body():
    r = PactResponse()
    assert r.body is None


def test_deafult_headers():
    r = PactResponse()
    assert r.headers == []


def test_default_status():
    r = PactResponse()
    assert r.status == 500


def test_custom_body():
    body = {'spam': 'eggs'}
    r = PactResponse(body=body)
    assert r.body == body

    body = {'spam': 'spam'}
    r.body = body
    assert r.body == body


def test_custom_headers():
    headers = [('Content-Type', 'text')]
    r = PactResponse(headers=headers)
    assert r.headers == headers

    headers = [('Content-Type', 'application/json')]
    r.headers = headers
    assert r.headers == headers


def test_custom_status():
    r = PactResponse(status=200)
    assert r.status == 200

    r.status = 201
    assert r.status == 201

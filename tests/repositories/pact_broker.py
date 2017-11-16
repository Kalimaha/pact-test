import requests
from pact_test.either import *
from pact_test.repositories.pact_broker import upload_pact
from pact_test.repositories.pact_broker import next_version
from pact_test.repositories.pact_broker import get_latest_version


def test_upload_pact(mocker):
    class GetResponse(object):
        status_code = 200

        def json(self):
            return {'_embedded': {'versions': [{'number': '1.0.41'}]}}

    class PutResponse(object):
        status_code = 200

        def json(self):
            return {}

    mocker.patch.object(requests, 'put', lambda x, **kwargs: PutResponse())
    mocker.patch.object(requests, 'get', lambda x, **kwargs: GetResponse())

    out = upload_pact('provider', 'consumer', {})
    assert type(out) is Right


def test_next_version():
    assert next_version('1.0.41') == '1.0.42'


def test_get_latest_version(mocker):
    class Response(object):
        status_code = 200

        def json(self):
            return {'_embedded': {'versions': [{'number': 42}]}}

    mocker.patch.object(requests, 'get', lambda x, **kwargs: Response())

    latest_version = get_latest_version('eggs')
    assert type(latest_version) is Right
    assert latest_version.value == 42


def test_missing_latest_version(mocker):
    class Response(object):
        status_code = 404

    mocker.patch.object(requests, 'get', lambda x, **kwargs: Response())

    latest_version = get_latest_version('eggs')
    assert type(latest_version) is Right
    assert latest_version.value == '1.0.0'


def test_wrong_url():
    latest_version = get_latest_version('eggs', base_url='http://host:9999/')
    msg = 'Failed to establish a new connection with http://host:9999/'

    assert type(latest_version) is Left
    assert latest_version.value == msg

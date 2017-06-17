import os
import requests
from pact_test.either import Left
from pact_test.utils.pact_utils import get_pact


def test_get_pact_from_url(mocker):
    class FakeResponse(object):
        def json(self):
            return {'spam': 'eggs'}

    mocker.patch.object(requests, 'get')
    requests.get.return_value = FakeResponse()

    url = 'http://montyphyton.com/'
    url_content = {'spam': 'eggs'}
    assert get_pact(url).value == url_content


def test_get_pact_from_url_with_errors(mocker):
    def bad_url(_):
        raise Exception('Boom!')
    mocker.patch.object(requests, 'get', new=bad_url)

    assert get_pact('http://montyphyton.com/').value == 'Boom!'


def test_get_pact_from_file():
    filename = os.path.join(os.getcwd(), 'tests', 'resources',
                            'pact_files', 'file.json')
    file_content = {'spam': 'eggs'}

    assert get_pact(filename).value == file_content


def test_get_pact_from_file_with_errors():
    filename = os.path.join(os.getcwd())
    assert type(get_pact(filename)) is Left

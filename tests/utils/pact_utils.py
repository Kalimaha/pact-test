import os
try:
    from urllib.request import urlopen
except ImportError:
    from urllib import urlopen
from pact_test.utils import pact_utils


def test_get_pact_from_url(monkeypatch):
    def fake_website(_):
        return '{"spam": "eggs"}'
    monkeypatch.setattr(pact_utils, '__url_content', fake_website)

    url = 'http://montyphyton.com/'
    url_content = {'spam': 'eggs'}

    assert pact_utils.__get_pact_from_url(url) == url_content


def test_get_pact_from_file():
    filename = os.path.join(os.getcwd(), 'tests', 'resources',
                            'pact_files', 'file.json')
    file_content = {'spam': 'eggs'}

    assert pact_utils.__get_pact_from_file(filename) == file_content


def test_generic_get_pact_from_url(monkeypatch):
    def fake_website(_):
        return '{"spam": "eggs"}'
    monkeypatch.setattr(pact_utils, '__url_content', fake_website)

    url = 'http://montyphyton.com/'
    url_content = {'spam': 'eggs'}

    assert pact_utils.get_pact(url) == url_content


def test_generic_get_pact_from_file():
    filename = os.path.join(os.getcwd(), 'tests', 'resources',
                            'pact_files', 'file.json')
    file_content = {'spam': 'eggs'}

    assert pact_utils.get_pact(filename) == file_content

import os
import imp
import json
import pytest
import urllib.request
from urllib.request import Request
from pact_test.executors.provider_executor import ProviderExecutor


def test_verify_pact(mocker):
    class Marker(object):
        args = ['a menu exists']

    class Item(object):
        def get_marker(self, name):
            return Marker()

    pact_file = simple_pact()
    executor = ProviderExecutor(Item())
    mocker.patch.object(executor, 'fetch_pact_file')
    mocker.patch.object(executor, 'verify_interaction')
    executor.fetch_pact_file.return_value = pact_file
    executor.verify_interaction.return_value = True

    assert executor.verify_pact() is True


def test_verify_interaction(monkeypatch):
    class FakeReader(object):
        def decode(self):
            return str({
                "id": 42,
                "name": "Spam, Eggs and Bacon",
                "ingredients": ["spam", "eggs", "bacon"]
            }).replace("'", "\"")

    class FakeResponse(object):
        status = 200
        reason = 'OK'

        def getheaders(self):
            return [
                ("Content-Type", "application/json"),
                ("Pragma", "no-cache")
            ]

        def read(self):
            return FakeReader()

    executor = ProviderExecutor(None)
    interaction = simple_pact()['interactions'][0]

    def urlopen(url):
        return FakeResponse()
    monkeypatch.setattr(urllib.request, 'urlopen', urlopen)

    assert executor.verify_interaction(interaction) is True


def test_body_matches():
    executor = ProviderExecutor(None)
    consumer_body = {"name": "Spam, Eggs and Bacon"}
    response_body = {
        "name": "Spam, Eggs and Bacon",
        "ingredients": ["spam", "eggs", "bacon"],
        "vegan": False,
        "vegetarian": False
    }

    assert executor.body_matches(consumer_body, response_body) is True


def test_headers_match():
    executor = ProviderExecutor(None)
    consumer_headers = {
        "Content-Type": "application/json",
        "Pragma": "no-cache"
    }
    response_headers = [
        ('Content-Type', 'application/json'),
        ('Content-Length', '292'),
        ('Access-Control-Allow-Credentials', 'true'),
        ('Pragma', 'no-cache')
    ]

    assert executor.headers_match(consumer_headers, response_headers) is True


def test_reason_matches():
    executor = ProviderExecutor(None)
    consumer_reason = "I'm a teapot."
    response_reason = "I'm a teapot."

    assert executor.reason_matches(consumer_reason, response_reason) is True


def test_status_matches():
    executor = ProviderExecutor(None)
    consumer_status = 418
    response_status = 418

    assert executor.status_matches(consumer_status, response_status) is True


def test_build_request():
    executor = ProviderExecutor(None)
    consumer_request = {
        "method": "POST",
        "path": "/menu/42",
        "query": "?vegan=false",
        "headers": {
            "Content-Type": "application/json"
        },
        "body": {
            "alligator": {
                "name": "Mary"
            }
        }
    }
    request = executor.build_request(consumer_request)
    assert request.get_method() == 'POST'
    assert request.full_url == 'http://localhost:1234/menu/42?vegan=false'
    assert request.headers == {"Content-type": "application/json"}
    assert request.data == {"alligator": {"name": "Mary"}}


def test_load_interactions():
    class Marker(object):
        args = [os.getcwd() + '/tests/resources/simple_pact.json']

    class Item(object):
        def get_marker(self, name):
            return Marker()

    executor = ProviderExecutor(Item())
    expected_interactions = simple_pact()['interactions']

    assert executor.load_interactions() == expected_interactions


def test_fetch_remote_pact_file(monkeypatch):
    class Marker(object):
        args = ['http://test.com/simple_pact.json']

    class Item(object):
        def get_marker(self, name):
            return Marker()

    def url_open(_):
        return open(os.getcwd() + '/tests/resources/simple_pact.json')
    monkeypatch.setattr(urllib.request, 'urlopen', url_open)

    assert ProviderExecutor(Item()).fetch_pact_file() == simple_pact()


def test_fetch_local_pact_file():
    class Marker(object):
        args = [os.getcwd() + '/tests/resources/simple_pact.json']

    class Item(object):
        def get_marker(self, name):
            return Marker()

    assert ProviderExecutor(Item()).fetch_pact_file() == simple_pact()


def test_set_up(mocker):
    class PactHelper(object):
        def set_up(self):
            pass

    pact_helper = PactHelper()
    mocker.spy(pact_helper, 'set_up')

    executor = ProviderExecutor(None)
    mocker.patch.object(executor, 'set_up', new=pact_helper.set_up)

    executor.set_up()
    assert pact_helper.set_up.call_count == 1


def test_tear_down(mocker):
    class PactHelper(object):
        def tear_down(self):
            pass

    pact_helper = PactHelper()
    mocker.spy(pact_helper, 'tear_down')

    executor = ProviderExecutor(FakePyFuncItem())
    mocker.patch.object(executor, 'tear_down', new=pact_helper.tear_down)

    executor.set_up()
    executor.tear_down()
    assert pact_helper.tear_down.call_count == 1


def test_load_pact_helper():
    executor = ProviderExecutor(FakePyFuncItem())

    helper_path = os.getcwd() + '/tests/resources/pact_helper.py'
    pact_helper = executor.load_pact_helper(helper_path)

    assert pact_helper is not None


def test_pact_helper_has_no_setup_method():
    executor = ProviderExecutor(FakePyFuncItem())

    helper_path = os.getcwd() + '/tests/resources/pact_helper_no_setup.py'

    err_msg = 'Module pact_helper MUST have a set_up method.'
    try:
        executor.load_pact_helper(helper_path)
    except Exception as e:
        assert str(e) == err_msg


def test_pact_helper_has_no_teardown_method():
    executor = ProviderExecutor(FakePyFuncItem())

    helper_path = os.getcwd() + '/tests/resources/pact_helper_no_teardown.py'

    err_msg = 'Module pact_helper MUST have a tear_down method.'
    try:
        executor.load_pact_helper(helper_path)
    except Exception as e:
        assert str(e) == err_msg


def test_pact_helper_path(monkeypatch):
    executor = ProviderExecutor(FakePyFuncItem())

    def list_files(dir):
        return ['spam.py', 'eggs.py', 'pact_helper.py']
    monkeypatch.setattr(os, 'listdir', list_files)

    helper_path = os.getcwd() + '/tests/resources/pact_helper.py'
    assert executor.pact_helper_path() == helper_path


def test_pact_helper_not_found(monkeypatch):
    executor = ProviderExecutor(FakePyFuncItem())

    def list_files(dir):
        return ['spam.py', 'eggs.py', 'bacon.py']
    monkeypatch.setattr(os, 'listdir', list_files)

    err_msg = 'Could\'n find "pact_helper.py" script in Pact test directory.'
    try:
        executor.pact_helper_path()
    except Exception as e:
        assert str(e) == err_msg


def test_valid_setup():
    assert ProviderExecutor(FakePyFuncItem()).is_valid()


def test_missing_markers(mocker):
    def get_marker(name):
        return FakeMarker(name, name) if name is 'state' else None

    pyfuncitem = FakePyFuncItem()
    mocker.patch.object(pyfuncitem, 'get_marker', new=get_marker)

    assert ProviderExecutor(pyfuncitem).is_valid() is False


def test_missing_values(mocker):
    def get_marker(name):
        return FakeMarker(name, None) if name is 'state' else None

    pyfuncitem = FakePyFuncItem()
    mocker.patch.object(pyfuncitem, 'get_marker', new=get_marker)

    assert ProviderExecutor(pyfuncitem).is_valid() is False


class FakeMarker(object):
    def __init__(self, marker_name, marker_value):
        self.args = [marker_name + '_VALUE']


class FakePyFuncItem(object):
    fspath = os.getcwd() + '/tests/resources/my_test.py'

    def get_marker(self, marker_name):
        return FakeMarker(marker_name, marker_name)


def simple_pact():
    path_to_pact = os.getcwd() + '/tests/resources/simple_pact.json'
    with open(path_to_pact) as f:
        pact = json.load(f)
    return pact

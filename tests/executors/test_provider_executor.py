import os
import imp
import pytest
from pytest_pact.executors.provider_executor import ProviderExecutor


def test_set_up(mocker):
    class PactHelper(object):
        def set_up(self):
            pass

    pact_helper = PactHelper()
    mocker.spy(pact_helper, 'set_up')

    executor = ProviderExecutor(FakePyFuncItem())
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


def test_load_pact_helper(monkeypatch):
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

from pact_test.utils.pact_utils import *


def test_standard_executor(mocker):
    pyfuncitem = FakePyFuncItem()
    mocker.patch.object(pyfuncitem, 'get_marker')
    pyfuncitem.get_marker.return_value = None

    assert type(executor(pyfuncitem)).__name__ is 'StandardExecutor'


def test_consumer_executor(mocker):
    def get_marker(marker_name):
        return pymarker if marker_name == HAS_PACT_WITH else None

    pyfuncitem = FakePyFuncItem()
    mocker.patch.object(pyfuncitem, 'get_marker', new=get_marker)

    pymarker = FakeMarker()
    mocker.patch.object(pymarker, 'args')
    pymarker.args.return_value = ['Books Service']

    assert type(executor(pyfuncitem)).__name__ is 'ConsumerExecutor'


def test_provider_executor(mocker):
    def get_marker(marker_name):
        return pymarker if marker_name == HONOURS_PACT_WITH else None

    pyfuncitem = FakePyFuncItem()
    mocker.patch.object(pyfuncitem, 'get_marker', new=get_marker)

    pymarker = FakeMarker()
    mocker.patch.object(pymarker, 'args')
    pymarker.args.return_value = ['Hallo world!']

    assert type(executor(pyfuncitem)).__name__ is 'ProviderExecutor'


def test_is_standard_test(mocker):
    pyfuncitem = FakePyFuncItem()
    mocker.patch.object(pyfuncitem, 'get_marker')
    pyfuncitem.get_marker.return_value = None

    assert pact_type(pyfuncitem) is None


def test_is_consumer_test(mocker):
    def get_marker(marker_name):
        return pymarker if marker_name == HAS_PACT_WITH else None

    pyfuncitem = FakePyFuncItem()
    mocker.patch.object(pyfuncitem, 'get_marker', new=get_marker)

    pymarker = FakeMarker()
    mocker.patch.object(pymarker, 'args')
    pymarker.args.return_value = ['Hallo world!']

    assert pact_type(pyfuncitem) == CONSUMER


def test_is_provider_test(mocker):
    def get_marker(marker_name):
        return pymarker if marker_name == HONOURS_PACT_WITH else None

    pyfuncitem = FakePyFuncItem()
    mocker.patch.object(pyfuncitem, 'get_marker', new=get_marker)

    pymarker = FakeMarker()
    mocker.patch.object(pymarker, 'args')
    pymarker.args.return_value = ['Hallo world!']

    assert pact_type(pyfuncitem) == PROVIDER


class FakePyFuncItem(object):
    def get_marker(self, marker_name):
            return None


class FakeMarker(object):
    args = []

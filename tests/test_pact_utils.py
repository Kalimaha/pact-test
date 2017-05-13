from pytest_pact.pact_utils import *


def test_standard_executor():

    class FakePyFuncItem(object):
        def get_marker(self, marker_name):
            return None

    pyfuncitem = FakePyFuncItem()
    assert type(executor(pyfuncitem)).__name__ is 'StandardExecutor'


def test_consumer_executor():

    class FakeMarker(object):
        args = ['Books Service']

    class FakePyFuncItem(object):
        def get_marker(self, marker_name):
            return FakeMarker() if marker_name == HAS_PACT_WITH else None

    pyfuncitem = FakePyFuncItem()
    assert type(executor(pyfuncitem)).__name__ is 'ConsumerExecutor'


def test_provider_executor():

    class FakeMarker(object):
        args = ['Library App']

    class FakePyFuncItem(object):
        def get_marker(self, marker_name):
            return FakeMarker() if marker_name == HONOURS_PACT_WITH else None

    pyfuncitem = FakePyFuncItem()
    assert type(executor(pyfuncitem)).__name__ is 'ProviderExecutor'


def test_is_standard_test():

    class FakePyFuncItem(object):
        def get_marker(self, marker_name):
            return None

    pyfuncitem = FakePyFuncItem()
    assert pact_type(pyfuncitem) is None


def test_is_consumer_test():

    class FakeMarker(object):
        args = ['Books Service']

    class FakePyFuncItem(object):
        def get_marker(self, marker_name):
            return FakeMarker() if marker_name == HAS_PACT_WITH else None

    pyfuncitem = FakePyFuncItem()
    assert pact_type(pyfuncitem) == CONSUMER


def test_is_provider_test():

    class FakeMarker(object):
        args = ['Library App']

    class FakePyFuncItem(object):
        def get_marker(self, marker_name):
            return FakeMarker() if marker_name == HONOURS_PACT_WITH else None

    pyfuncitem = FakePyFuncItem()
    assert pact_type(pyfuncitem) == PROVIDER

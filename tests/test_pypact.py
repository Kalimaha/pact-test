from pact import *


def test_read_existing_marker():
    expected_marker = 'some books exist'

    class FakeMarker(object):
        args = [expected_marker]

    class FakePyFuncItem(object):
        def get_marker(self, marker_name):
            return FakeMarker()

    pyfuncitem = FakePyFuncItem()
    marker_name = 'given'
    assert read_marker(pyfuncitem, marker_name) == expected_marker


def test_read_non_existing_marker():

    class FakePyFuncItem(object):
        def get_marker(self, marker_name):
            return None

    pyfuncitem = FakePyFuncItem()
    marker_name = 'given'
    assert read_marker(pyfuncitem, marker_name) is None


def test_is_standard_test():

    class FakePyFuncItem(object):
        def get_marker(self, marker_name):
            return None

    pyfuncitem = FakePyFuncItem()
    assert consumer_or_provider(pyfuncitem) is None


def test_is_consumer_test():

    class FakeMarker(object):
        args = ['Books Service']

    class FakePyFuncItem(object):
        def get_marker(self, marker_name):
            return FakeMarker() if marker_name == HAS_PACT_WITH else None

    pyfuncitem = FakePyFuncItem()
    assert consumer_or_provider(pyfuncitem) == CONSUMER


def test_is_provider_test():

    class FakeMarker(object):
        args = ['Library App']

    class FakePyFuncItem(object):
        def get_marker(self, marker_name):
            return FakeMarker() if marker_name == HONOURS_PACT_WITH else None

    pyfuncitem = FakePyFuncItem()
    assert consumer_or_provider(pyfuncitem) == PROVIDER

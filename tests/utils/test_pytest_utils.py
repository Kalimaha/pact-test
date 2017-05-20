from pact_test.utils.pytest_utils import *


def test_read_existing_marker():
    class FakeMarker(object):
        args = ['My Value']

    class FakePyFuncItem(object):
        def get_marker(self, marker_name):
            return FakeMarker()

    pyfuncitem = FakePyFuncItem()
    assert read_marker(pyfuncitem, 'My Marker') == 'My Value'


def test_read_non_existing_marker():

    class FakePyFuncItem(object):
        def get_marker(self, marker_name):
            return None

    pyfuncitem = FakePyFuncItem()
    assert read_marker(pyfuncitem, 'My Marker') is None

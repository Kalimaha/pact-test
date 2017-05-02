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
    assert read_marker(pyfuncitem, marker_name) == ''

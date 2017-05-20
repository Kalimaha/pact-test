from pact_test.executors.consumer_executor import ConsumerExecutor


def test_valid_setup():
    class FakeMarker(object):
        def __init__(self, marker_name):
            self.args = [marker_name + '_VALUE']

    class FakePyFuncItem(object):
        def get_marker(self, marker_name):
            return FakeMarker(marker_name)
    pyfuncitem = FakePyFuncItem()
    assert ConsumerExecutor(pyfuncitem).is_valid()


def test_missing_markers():
    class FakeMarker(object):
        def __init__(self, marker_name):
            self.args = [marker_name + '_VALUE']

    class FakePyFuncItem(object):
        def get_marker(self, marker_name):
            return FakeMarker(marker_name) if marker_name is 'state' else None
    pyfuncitem = FakePyFuncItem()
    assert ConsumerExecutor(pyfuncitem).is_valid() is False


def test_null_values():
    class FakeMarker(object):
        def __init__(self, marker_name):
            self.args = [42] if marker_name is 'state' else [None]

    class FakePyFuncItem(object):
        def get_marker(self, marker_name):
            return FakeMarker(marker_name)
    pyfuncitem = FakePyFuncItem()
    assert ConsumerExecutor(pyfuncitem).is_valid() is False

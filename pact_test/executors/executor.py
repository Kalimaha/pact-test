from pact_test.utils.pytest_utils import read_marker


class Executor(object):
    REQUIRED_PARAMETERS = []

    def __init__(self, pyfuncitem):
        self.pyfuncitem = pyfuncitem

    def set_up(self):
        pass

    def tear_down(self):
        pass

    def is_valid(self):
        check = {}
        for marker in self.REQUIRED_PARAMETERS:
            marker_value = read_marker(self.pyfuncitem, marker)
            if marker_value is not None:
                check[marker] = marker_value
        valid_keys = sorted(check.keys()) == sorted(self.REQUIRED_PARAMETERS)
        valid_values = all(v is not None for v in check.values())
        return valid_keys and valid_values

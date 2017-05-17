import os
import sys
import imp
from pytest_pact.executors.executor import Executor
from pytest_pact.pact_markers import STATE
from pytest_pact.pact_markers import PACT_URI
from pytest_pact.pact_markers import HONOURS_PACT_WITH


class ProviderExecutor(Executor):
    REQUIRED_PARAMETERS = [STATE, PACT_URI, HONOURS_PACT_WITH]
    PACT_HELPER = 'pact_helper.py'
    PACT_HELPER_NOT_FOUND = 'Could\'n find "pact_helper.py" script in Pact test directory.'
    SET_UP_NOT_FOUND = 'Module pact_helper MUST have a set_up method'
    TEAR_DOWN_NOT_FOUND = 'Module pact_helper MUST have a tear_down method'
    pact_helper = None

    def set_up(self):
        path_to_pact_helper = self.pact_helper_path()
        self.pact_helper = self.load_pact_helper(path_to_pact_helper)
        self.pact_helper.set_up()

    def tear_down(self):
        self.pact_helper.tear_down()

    def load_pact_helper(self, path_to_pact_helper):
        pact_helper = imp.load_source('pact_helper', path_to_pact_helper)
        if hasattr(pact_helper, 'set_up') is False: raise Exception(self.SET_UP_NOT_FOUND)
        if hasattr(pact_helper, 'tear_down') is False: raise Exception(self.TEAR_DOWN_NOT_FOUND)
        return pact_helper

    def pact_helper_path(self):
        test_dir = os.path.dirname(self.pyfuncitem.fspath)
        files = [f for f in os.listdir(test_dir) if f == self.PACT_HELPER]
        if not files: raise Exception(self.PACT_HELPER_NOT_FOUND)
        pact_helper_path = os.path.join(test_dir, files[0])
        return pact_helper_path

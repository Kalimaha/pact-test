from pytest_pact.executor import Executor
from pytest_pact.pact_markers import STATE
from pytest_pact.pact_markers import PACT_URI
from pytest_pact.pact_markers import HONOURS_PACT_WITH


class ProviderExecutor(Executor):
    REQUIRED_PARAMETERS = [STATE, PACT_URI, HONOURS_PACT_WITH]

    def set_up(self):
        pass

    def tear_down(self):
        pass

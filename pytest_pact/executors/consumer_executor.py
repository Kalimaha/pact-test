from pytest_pact.executors.executor import Executor
from pytest_pact.pact_markers import SERVICE_CONSUMER
from pytest_pact.pact_markers import HAS_PACT_WITH
from pytest_pact.pact_markers import BASE_URI
from pytest_pact.pact_markers import GIVEN
from pytest_pact.pact_markers import UPON_RECEIVING
from pytest_pact.pact_markers import WITH_REQUEST
from pytest_pact.pact_markers import WILL_RESPOND_WITH


class ConsumerExecutor(Executor):
    REQUIRED_PARAMETERS = [SERVICE_CONSUMER, HAS_PACT_WITH, BASE_URI,
                           GIVEN, UPON_RECEIVING, WITH_REQUEST,
                           WILL_RESPOND_WITH]

    def set_up(self):
        pass

    def tear_down(self):
        pass

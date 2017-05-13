import pytest
from pytest_pact.pytest_utils import read_marker
from pytest_pact.pact_markers import CONSUMER
from pytest_pact.pact_markers import PROVIDER
from pytest_pact.pact_markers import HAS_PACT_WITH
from pytest_pact.pact_markers import HONOURS_PACT_WITH
from pytest_pact.standard_executor import StandardExecutor
from pytest_pact.consumer_executor import ConsumerExecutor
from pytest_pact.provider_executor import ProviderExecutor


def executor(pyfuncitem):
    executor_type = pact_type(pyfuncitem)
    executor = None
    if executor_type is CONSUMER:
        executor = ConsumerExecutor(pyfuncitem)
    elif executor_type is PROVIDER:
        executor = ProviderExecutor(pyfuncitem)
    else:
        executor = StandardExecutor(pyfuncitem)
    return executor


def pact_type(pyfuncitem):
    if is_consumer(pyfuncitem):
        return CONSUMER
    elif is_provider(pyfuncitem):
        return PROVIDER
    return None


def is_consumer(pyfuncitem):
    return read_marker(pyfuncitem, HAS_PACT_WITH) is not None


def is_provider(pyfuncitem):
    return read_marker(pyfuncitem, HONOURS_PACT_WITH) is not None

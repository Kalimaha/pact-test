import pytest


state = pytest.mark.state
given = pytest.mark.given
base_uri = pytest.mark.base_uri
pact_uri = pytest.mark.pact_uri
with_request = pytest.mark.with_request
has_pact_with = pytest.mark.has_pact_with
upon_receiving = pytest.mark.upon_receiving
will_respond_with = pytest.mark.will_respond_with
service_consumer = pytest.mark.service_consumer
honours_pact_with = pytest.mark.honours_pact_with


@pytest.hookimpl(hookwrapper=True)
def pytest_pyfunc_call(pyfuncitem):
    # print(describe_consumer_pact(pyfuncitem))

    # pypact = PyPact()
    # pypact.executor(pyfuncitem)



    outcome = yield
    # outcome.excinfo may be None or a (cls, val, tb) tuple
    print(outcome)

    res = outcome.get_result()  # will raise if outcome was exception
    # postprocess result
    print(res)


def consumer_or_provider(pyfuncitem):
    pass

class PyPactConsumer(object):
    pass

class PyPactProvider(object):
    pass


def describe_consumer_pact(pyfuncitem):
    s = ''
    s += 'Given ' + read_marker(pyfuncitem, 'given') + ', '
    s += 'upon receiving ' + read_marker(pyfuncitem, 'upon_receiving') + ' '
    s += 'from ' + read_marker(pyfuncitem, 'service_consumer') + ' '
    s += 'with:\n\n' + read_marker(pyfuncitem, 'with_request') + '\n\n'
    s += read_marker(pyfuncitem, 'has_pact_with') + ' will respond with:\n\n'
    s += read_marker(pyfuncitem, 'will_respond_with')
    return s

def read_marker(pyfuncitem, marker_name):
    marker = pyfuncitem.get_marker(marker_name)
    return str(marker.args[0]) if marker else ''

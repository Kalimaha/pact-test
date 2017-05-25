from pact_test.models.service_consumer_test import state
from pact_test.models.service_consumer_test import pact_uri
from pact_test.models.service_consumer_test import has_pact_with
from pact_test.models.service_consumer_test import ServiceConsumerTest


def test_default_pact_uri():
    t = ServiceConsumerTest()
    assert t.pact_uri is None


def test_pact_uri_decorator():
    @pact_uri('http://montypython.com/')
    class MyTest(ServiceConsumerTest):
        pass

    t = MyTest()
    assert t.pact_uri == 'http://montypython.com/'


def test_default_has_pact_with():
    t = ServiceConsumerTest()
    assert t.has_pact_with is None


def test_has_pact_with_decorator():
    @has_pact_with('Library App')
    class MyTest(ServiceConsumerTest):
        pass

    t = MyTest()
    assert t.has_pact_with == 'Library App'


def test_decorators():
    @has_pact_with('Library App')
    @pact_uri('http://montypython.com/')
    class MyTest(ServiceConsumerTest):
        pass

    t = MyTest()
    assert t.has_pact_with == 'Library App'
    assert t.pact_uri == 'http://montypython.com/'


def test_states():
    class MyTest(ServiceConsumerTest):
        @state('Default state')
        def setup(self):
            return 42

    t = MyTest()
    default_state = next(t.states)

    assert default_state is not None
    assert default_state.state == 'Default state'
    assert default_state() == 42

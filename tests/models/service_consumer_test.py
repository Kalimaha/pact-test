from pact_test import state
from pact_test import pact_uri
from pact_test import has_pact_with
from pact_test import ServiceConsumerTest


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


def test_missing_pact_uri():
    @has_pact_with('Restaurant Customer')
    class MyTest(ServiceConsumerTest):
        @state('the breakfast is available')
        def setup(self):
            return 42

    msg = 'Missing setup for "pact_uri"'
    assert MyTest().is_valid().value.startswith(msg)


def test_missing_has_pact_with():
    @pact_uri('http://montypython.com/')
    class MyTest(ServiceConsumerTest):
        @state('the breakfast is available')
        def setup(self):
            return 42

    msg = 'Missing setup for "has_pact_with"'
    assert MyTest().is_valid().value.startswith(msg)

from pact_test import given
from pact_test import with_request
from pact_test import has_pact_with
from pact_test import upon_receiving
from pact_test import service_consumer
from pact_test import will_respond_with
from pact_test import ServiceProviderTest
from pact_test.either import *


def test_default_service_consumer_value():
    t = ServiceProviderTest()
    assert t.service_consumer is None


def test_decorator_service_consumer_value():
    @service_consumer('Library App')
    class MyTest(ServiceProviderTest):
        pass

    t = MyTest()
    assert t.service_consumer == 'Library App'


def test_default_has_pact_with_value():
    t = ServiceProviderTest()
    assert t.has_pact_with is None


def test_decorator_has_pact_with_value():
    @has_pact_with('Books Service')
    class MyTest(ServiceProviderTest):
        pass

    t = MyTest()
    assert t.has_pact_with == 'Books Service'


def test_class_decorators():
    @service_consumer('Library App')
    @has_pact_with('Books Service')
    class MyTest(ServiceProviderTest):
        pass

    t = MyTest()
    assert t.service_consumer == 'Library App'
    assert t.has_pact_with == 'Books Service'


def test_method_decorators():
    class MyTest(ServiceProviderTest):
        @given('the breakfast menu is available')
        @upon_receiving('a request for a breakfast')
        @with_request('I don\'t like spam')
        @will_respond_with('Spam & Eggs')
        def make_me_breakfast(self):
            return 'Spam & Eggs'

    t = MyTest()
    decorated_method = next(t.decorated_methods)

    assert decorated_method is not None
    assert decorated_method.given == 'the breakfast menu is available'
    assert decorated_method.upon_receiving == 'a request for a breakfast'
    assert decorated_method.with_request == 'I don\'t like spam'
    assert decorated_method.will_respond_with == 'Spam & Eggs'
    assert decorated_method() == 'Spam & Eggs'


def test_missing_method_decorators():
    class MyTest(ServiceProviderTest):
        @given('the breakfast menu is available')
        def make_me_breakfast(self):
            return 'Spam & Eggs'

    t = MyTest()
    try:
        next(t.decorated_methods)
        assert False
    except StopIteration:
        assert True


def test_missing_service_consumer():
    @has_pact_with('Restaurant Customer')
    class MyTest(ServiceProviderTest):
        pass

    msg = 'Missing setup for "service_consumer"'
    assert MyTest().is_valid().value.startswith(msg)


def test_missing_has_pact_with():
    @service_consumer('Restaurant Customer')
    class MyTest(ServiceProviderTest):
        pass

    msg = 'Missing setup for "has_pact_with"'
    assert MyTest().is_valid().value.startswith(msg)


def test_valid_test():
    @service_consumer('Spam')
    @has_pact_with('Eggs')
    class MyTest(ServiceProviderTest):
        pass

    assert type(MyTest().is_valid()) is Right

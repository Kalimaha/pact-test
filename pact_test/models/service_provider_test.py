from pact_test.either import *
from pact_test.constants import *


class ServiceProviderTest(object):
    service_consumer = None
    has_pact_with = None

    @property
    def decorated_methods(self):
        for attr in dir(self):
            obj = getattr(self, attr)
            check = (
                        callable(obj)
                        and hasattr(obj, 'given')
                        and hasattr(obj, 'upon_receiving')
                        and hasattr(obj, 'with_request')
                        and hasattr(obj, 'will_respond_with')
                    )
            if check:
                yield obj

    def is_valid(self):
        if self.service_consumer is None:
            msg = MISSING_SERVICE_CONSUMER + __file__
            return Left(msg)
        if self.has_pact_with is None:
            msg = MISSING_HAS_PACT_WITH + __file__
            return Left(msg)
        return Right(True)


def service_consumer(service_consumer_value):
    def wrapper(calling_class):
        setattr(calling_class, 'set_service_consumer',
                eval('set_service_consumer(calling_class, "' + service_consumer_value + '")'))
        return calling_class
    return wrapper


def set_service_consumer(self, service_consumer_value):
    self.service_consumer = service_consumer_value


def has_pact_with(has_pact_with_value):
    def wrapper(calling_class):
        setattr(calling_class, 'set_has_pact_with',
                eval('set_has_pact_with(calling_class, "' + has_pact_with_value + '")'))
        return calling_class
    return wrapper


def set_has_pact_with(self, has_pact_with_value):
    self.has_pact_with = has_pact_with_value


def given(given_value):
    def decorate(function):
        function.given = given_value
        return function
    return decorate


def upon_receiving(upon_receiving_value):
    def decorate(function):
        function.upon_receiving = upon_receiving_value
        return function
    return decorate


def with_request(with_request_value):
    def decorate(function):
        function.with_request = with_request_value
        return function
    return decorate


def will_respond_with(will_respond_with_value):
    def decorate(function):
        function.will_respond_with = will_respond_with_value
        return function
    return decorate

from pact_test.either import *
from pact_test.constants import *


class ServiceConsumerTest(object):
    pact_uri = None
    honours_pact_with = None

    @property
    def states(self):
        for attr in dir(self):
            obj = getattr(self, attr)
            if callable(obj) and hasattr(obj, 'state'):
                yield obj

    def is_valid(self):
        if self.pact_uri is None:
            msg = MISSING_PACT_URI + __file__
            return Left(msg)
        if self.honours_pact_with is None:
            msg = MISSING_HONOURS_PACT_WITH + __file__
            return Left(msg)
        return Right(True)


def pact_uri(pact_uri_value):
    def wrapper(calling_class):
        setattr(calling_class, 'set_pact_uri',
                eval('set_pact_uri(calling_class, "' + pact_uri_value + '")'))
        return calling_class
    return wrapper


def set_pact_uri(self, pact_uri_value):
    self.pact_uri = pact_uri_value


def honours_pact_with(honours_pact_with_value):
    def wrapper(calling_class):
        setattr(calling_class, 'set_honours_pact_with',
                eval('set_honours_pact_with(calling_class, "' + honours_pact_with_value + '")'))
        return calling_class
    return wrapper


def set_honours_pact_with(self, honours_pact_with_value):
    self.honours_pact_with = honours_pact_with_value


def state(state_value):
    def decorate(function):
        function.state = state_value
        return function
    return decorate

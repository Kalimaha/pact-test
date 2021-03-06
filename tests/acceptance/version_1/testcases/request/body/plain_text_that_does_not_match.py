from pact_test.either import Left
from pact_test.models.request import PactRequest
from pact_test.matchers.request_matcher import match
from tests.acceptance.acceptance_test_loader import load_acceptance_test


def test():
    data = load_acceptance_test(__file__)

    actual = PactRequest(**data['actual'])
    expected = PactRequest(**data['expected'])

    actual.headers = [{'Content-Type': 'text/plain'}]
    expected.headers = [{'Content-Type': 'text/plain'}]

    test_result = match(actual, expected)
    assert type(test_result) is Left

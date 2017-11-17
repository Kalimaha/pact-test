from pact_test.either import Right
from pact_test.models.request import PactRequest
from pact_test.matchers.request_matcher import match
from tests.acceptance.acceptance_test_loader import load_acceptance_test


def test_status_matches():
    data = load_acceptance_test(__file__)

    actual = PactRequest(**data['actual'])
    expected = PactRequest(**data['expected'])

    test_result = match(actual, expected)
    assert type(test_result) is Right

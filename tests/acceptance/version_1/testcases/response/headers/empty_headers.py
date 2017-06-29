from pact_test.either import Right
from pact_test.models.response import PactResponse
from pact_test.matchers.response_matcher import match
from tests.acceptance.acceptance_test_loader import load_acceptance_test


def test_different_status():
    data = load_acceptance_test(__file__)

    response = PactResponse(headers=[])
    interaction = {'response': {'headers': data['expected']['headers']}}
    test_result = match(interaction, response)

    assert type(test_result) is Right

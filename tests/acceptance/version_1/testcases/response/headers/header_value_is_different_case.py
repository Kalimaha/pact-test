from pact_test.either import Left
from pact_test.models.response import PactResponse
from pact_test.matchers.response_matcher import match
from tests.acceptance.acceptance_test_loader import load_acceptance_test


def test_different_value_case():
    data = load_acceptance_test(__file__)

    response = PactResponse(headers=[('Accept', 'Alligators')])
    interaction = {'response': {'headers': data['expected']['headers']}}
    test_result = match(interaction, response)

    assert type(test_result) is Left

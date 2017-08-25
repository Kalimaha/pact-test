from pact_test.either import Left
from pact_test.models.response import PactResponse
from pact_test.matchers.response_matcher import match
from tests.acceptance.acceptance_test_loader import load_acceptance_test


def test_missing_index():
    data = load_acceptance_test(__file__)

    response = PactResponse(body={'alligator': {'favouriteColours': ['red']}})
    interaction = {'response': {'body': data['expected']['body']}}
    test_result = match(interaction, response)

    assert type(test_result) is Left

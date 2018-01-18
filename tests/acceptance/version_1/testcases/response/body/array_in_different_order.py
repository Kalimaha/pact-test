from pact_test.either import Left
from pact_test.models.response import PactResponse
from pact_test.matchers.response_matcher import match
from tests.acceptance.acceptance_test_loader import load_acceptance_test


def test_array_in_different_order():
    data = load_acceptance_test(__file__)

    response = PactResponse(body={
        'alligator': {
            'favouriteColours': ['blue', 'red']
        }
    })
    interaction = {'response': {'body': data['expected']['body']}}
    test_result = match(interaction, response)

    assert type(test_result) is Left

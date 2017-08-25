from pact_test.either import Right
from pact_test.models.response import PactResponse
from pact_test.matchers.response_matcher import match
from tests.acceptance.acceptance_test_loader import load_acceptance_test


def test_matches():
    data = load_acceptance_test(__file__)

    response = PactResponse(body={
        'alligator': {
            'feet': 4,
            'name': 'Mary',
            'favouriteColours': [
                'red',
                'blue'
            ]
        }
    })
    interaction = {'response': {'body': data['expected']['body']}}
    test_result = match(interaction, response)

    assert type(test_result) is Right

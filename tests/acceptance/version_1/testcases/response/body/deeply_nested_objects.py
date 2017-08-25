import pytest
from pact_test.either import Right
from pact_test.models.response import PactResponse
from pact_test.matchers.response_matcher import match
from tests.acceptance.acceptance_test_loader import load_acceptance_test


@pytest.mark.skip(reason="requires further investigation")
def test_nested_objects():
    data = load_acceptance_test(__file__)

    response = PactResponse(body={
        'object1': {
            'object2': {
                'object4': {
                    'object5': {
                        'name': 'Mary',
                        'friends': ['Fred', 'John'],
                        'gender': 'F'
                    },
                    'object6': {
                        'phoneNumber': 1234567890
                    }
                }
            },
            'color': 'red'
        }
    })
    interaction = {'response': {'body': data['expected']['body']}}
    test_result = match(interaction, response)

    assert type(test_result) is Right

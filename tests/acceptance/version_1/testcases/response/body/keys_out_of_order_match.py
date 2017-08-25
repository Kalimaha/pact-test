import pytest
from pact_test.either import Right
from pact_test.models.response import PactResponse
from pact_test.matchers.response_matcher import match
from tests.acceptance.acceptance_test_loader import load_acceptance_test


@pytest.mark.skip(reason="requires further investigation")
def test_different_values():
    data = load_acceptance_test(__file__)

    response = PactResponse(body={
        'favouriteColours': ['red', 'blue'],
        'favouriteNumber': 7
    })
    interaction = {'response': {'body': data['expected']['body']}}
    test_result = match(interaction, response)

    assert type(test_result) is Right

from pact_test.constants import *
from pact_test.models.response import PactResponse
from pact_test.matchers.response_matcher import match
from tests.acceptance.acceptance_test_loader import load_acceptance_test


def test_different_status():
    data = load_acceptance_test(__file__)

    response = PactResponse(status=400)
    interaction = {'response': {'status': data['expected']['status']}}
    test_result = match(interaction, response).value

    assert test_result == {
        'status': FAILED,
        'message': 'Status is incorrect',
        'expected': data['expected']['status'],
        'actual': 400
    }

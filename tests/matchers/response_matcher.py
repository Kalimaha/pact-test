from pact_test.either import Right
from pact_test.models.response import PactResponse
from pact_test.matchers.response_matcher import match


interaction = {
    'response': {
        'status': 418,
        'headers': {'Content-Type': 'spam'},
        'body': {'spam': 'eggs'}
    }
}


def valid_response():
    return PactResponse(
        status=418,
        headers=[('Content-Type', 'spam')],
        body={'spam': 'eggs'}
    )


def test_non_matching_status():
    pact_response = PactResponse(status=200)
    msg = {
        'status': 'FAILED',
        'message': 'Status is incorrect',
        'expected': 418,
        'actual': 200
    }

    assert match(interaction, pact_response).value == msg


def test_non_matching_headers():
    pact_response = PactResponse(status=418, headers=[('Date', '12-06-2017')])
    msg = {
        'status': 'FAILED',
        'message': 'Headers is incorrect',
        'expected': {'Content-Type': 'spam'},
        'actual': {'Date': '12-06-2017'}
    }

    assert match(interaction, pact_response).value == msg


def test_non_matching_body():
    pact_response = PactResponse(
        status=418,
        headers=[('Content-Type', 'spam')],
        body={'spam': 'spam'}
    )
    msg = {
        'status': 'FAILED',
        'message': 'Body is incorrect',
        'expected': {'spam': 'eggs'},
        'actual': {'spam': 'spam'}
    }
    assert match(interaction, pact_response).value == msg


def test_matching_response():
    pact_response = valid_response()

    assert type(match(interaction, pact_response)) is Right

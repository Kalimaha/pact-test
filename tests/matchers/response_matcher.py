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
    msg = 'Non-matching status for the response. Expected:\n\n\t' + \
          str(418) + '\n\nReceived:\n\n\t' + str(200)

    assert match(interaction, pact_response).value == msg


def test_non_matching_headers():
    pact_response = PactResponse(status=418, headers=[('Date', '12-06-2017')])
    msg = 'Non-matching headers for the response. Expected:\n\n\t' + \
          str({'Content-Type': 'spam'}) + '\n\nReceived:\n\n\t' + \
          str({'Date': '12-06-2017'})

    assert match(interaction, pact_response).value == msg


def test_non_matching_body():
    pact_response = PactResponse(
        status=418,
        headers=[('Content-Type', 'spam')],
        body={'spam': 'spam'}
    )
    msg = 'Non-matching body for the response. Expected:\n\n\t' + \
          str({'spam': 'eggs'}) + '\n\nReceived:\n\n\t' + \
          str({'spam': 'spam'})
    assert match(interaction, pact_response).value == msg


def test_matching_response():
    pact_response = valid_response()

    assert type(match(interaction, pact_response)) is Right

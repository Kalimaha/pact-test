from pact_test.either import *
from pact_test.constants import *
from pact_test.utils.logger import error
from pact_test.matchers.response_matcher import match
from pact_test.clients.http_client import execute_interaction_request


def verify_state(interaction, pact_helper, test_instance):
    state = find_state(interaction, interaction['description'], test_instance)
    if type(state) is Right:
        state.value()
        output = _execute_request(pact_helper, interaction)
        if type(output) is Right:
            response_verification = match(interaction, output.value)
            output = _build_state_response(state, interaction['description'], response_verification)
            return output
        error(output.value)
        return output
    error(state.value)
    return state


def _execute_request(pact_helper, interaction):
    url = pact_helper.test_url
    port = pact_helper.test_port
    return execute_interaction_request(url, port, interaction)


def _build_state_response(state, description, response_verification):
    if type(response_verification) is Right:
        return Right(_format_message(state.value.state, description, PASSED, []))
    else:
        errors = [response_verification.value]
        return Left(_format_message(state.value.state, description, FAILED, errors))


def find_state(interaction, description, test_instance):
    state = interaction[PROVIDER_STATE]
    for s in test_instance.states:
        if s.state == state:
            return Right(s)
    message = 'Missing state implementation for "' + state + '"'
    return Left(_format_message(state, description, FAILED, [message]))


def _format_message(state, description, status, errors):
    return {'state': state, 'description': description, 'status': status, 'errors': errors}

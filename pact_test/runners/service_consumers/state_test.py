from pact_test.matchers.response_matcher import match
from pact_test.clients.http_client import execute_interaction_request


def verify_state(interaction, pact_helper, test_instance):
    """
        1. PactHelper.setup() per far partire il servizio
        2. state() per preparare il sistema
        3. creare richiesta basata su Pact
        4. eseguire richiesta
        5. verificare risposta
        6. PactHelper.tear_down() per fermare il servizio
    """
    pact_helper.setup()
    # EXECUTE state() HERE
    response = execute_interaction_request(pact_helper.test_url, pact_helper.test_port, interaction)
    # VERIFY response HERE
    response_verification = None
    pact_helper.tear_down()
    return response_verification

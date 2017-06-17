from pact_test.models.request import PactRequest
from pact_test.models.response import PactResponse


REQUEST = 'request'
RESPONSE = 'response'


def build_request_from_interaction(interaction):
    request = interaction[REQUEST]

    return PactRequest(
        body=request.get('body', None),
        path=request.get('path', None),
        query=request.get('query', None),
        method=request.get('method', None),
        headers=_build_headers_from_pact(interaction, REQUEST)
    )


def build_response_from_interaction(interaction):
    response = interaction[RESPONSE]

    return PactResponse(
        body=response.get('body', None),
        status=response.get('status', None),
        headers=_build_headers_from_pact(interaction, RESPONSE)
    )


def _build_headers_from_pact(pact, request_or_response):
    headers = []
    pact_headers = pact[request_or_response].get('headers', None)
    for h in (h for h in (pact_headers if pact_headers else [])):
        headers.append((h, pact_headers[h]))
    return headers

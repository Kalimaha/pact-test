from pact_test.models.request import PactRequest


def build_request_from_pact(pact):
    return PactRequest(
        body=pact['request'].get('body', None),
        path=pact['request'].get('path', None),
        query=pact['request'].get('query', None),
        method=pact['request'].get('method', None),
        headers=_build_request_headers_from_pact(pact),
    )


def _build_request_headers_from_pact(pact):
    headers = []
    pact_headers = pact['request'].get('headers', None)
    for h in (h for h in (pact_headers if pact_headers else [])):
        headers.append((h, pact_headers[h]))
    return headers

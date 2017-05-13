import pytest


state = pytest.mark.state
given = pytest.mark.given
base_uri = pytest.mark.base_uri
pact_uri = pytest.mark.pact_uri
with_request = pytest.mark.with_request
has_pact_with = pytest.mark.has_pact_with
upon_receiving = pytest.mark.upon_receiving
will_respond_with = pytest.mark.will_respond_with
service_consumer = pytest.mark.service_consumer
honours_pact_with = pytest.mark.honours_pact_with

CONSUMER = 'CONSUMER'
PROVIDER = 'PROVIDER'
HAS_PACT_WITH = 'has_pact_with'
HONOURS_PACT_WITH = 'honours_pact_with'
STATE = 'state'
GIVEN = 'given'
BASE_URI = 'base_uri'
PACT_URI = 'pact_uri'
WITH_REQUEST = 'with_request'
UPON_RECEIVING = 'upon_receiving'
WILL_RESPOND_WITH = 'will_respond_with'
SERVICE_CONSUMER = 'service_consumer'

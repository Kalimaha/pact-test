import requests
from pact_test.models.service_provider_test import *


@service_consumer('Library App')
@has_pact_with('Books Service')
class SimpleTest(ServiceProviderTest):

    @given('a book exists')
    @upon_receiving('a request for a book')
    @with_request({'method': 'get', 'path': '/books/42/'})
    @will_respond_with({'status': 200})
    def test_get_book(self):
        requests.get('http://localhost:9999/books/42')

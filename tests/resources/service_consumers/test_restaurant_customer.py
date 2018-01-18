from pact_test.models.service_consumer_test import *


@honours_pact_with('Restaurant')
@pact_uri('tests/resources/pact_files/simple.json')
class TestRestaurantCustomer(ServiceConsumerTest):

    @state('the breakfast is available')
    def test_get_breakfast(self):
        return 'Spam & Eggs'

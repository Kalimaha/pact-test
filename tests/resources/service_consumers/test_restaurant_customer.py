from pact_test.models.service_consumer_test import *


@has_pact_with('Restaurant')
@pact_uri('http://google.com/')
class TestRestaurantCustomer(ServiceConsumerTest):

    @state('the breakfast is available')
    def test_get_breakfast(self):
        return 'Spam & Eggs'

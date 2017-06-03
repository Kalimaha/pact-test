from pact_test.models.service_consumer_test import state
from pact_test.models.service_consumer_test import ServiceConsumerTest
from pact_test.runners.service_consumers.state_test import verify_state
from pact_test.runners.service_consumers.state_test import create_request
from pact_test.runners.service_consumers.state_test import build_test_result


def test_build_test_result():
    status = 'Spam'
    reason = 'Eggs'
    expected_response = {'status': status, 'reason': reason}
    assert build_test_result(status, reason) == expected_response


def test_build_test_result_default():
    expected_response = {'status': 'PASSED', 'reason': None}
    assert build_test_result() == expected_response


def test_verify_state(mocker):
    test_instance = TestLibraryApp()
    pact_helper = PactHelper()

    mocker.spy(pact_helper, 'set_up')
    mocker.spy(pact_helper, 'tear_down')

    response = verify_state(interaction, pact_helper, test_instance).value
    expected_response = {'status': 'PASSED', 'reason': None}

    assert response == expected_response
    assert pact_helper.set_up.call_count == 1
    assert pact_helper.tear_down.call_count == 1


def test_create_request():
    request_body = interaction['request']
    request = create_request(request_body)

    assert request.method == request_body['method']
    assert request.selector == request_body['path'] + request_body['query']
    assert request.headers == request_body.get('headers', {})


class PactHelper(object):
    @staticmethod
    def set_up():
        pass

    @staticmethod
    def tear_down():
        pass


interaction = {
    'providerState': 'some books exist',
    'request': {
        'method': 'GET',
        'path': '/books/42',
        'query': '?type=hardcover',
        'headers': {
            'Content-type': 'application/json'
        }
    },
    'response': {
        'status': 200,
        'body': {
            'id': 42,
            'title': 'The Hitchhicker\'s Guide to the Galaxy'
        }
    }
}


class TestLibraryApp(ServiceConsumerTest):
    @state('some books exist')
    def test_get_book(self):
        pass

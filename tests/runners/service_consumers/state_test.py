from pact_test import state
from pact_test import PactHelper
from pact_test import ServiceConsumerTest
from pact_test.runners.service_consumers.state_test import verify_state
from pact_test.runners.service_consumers.state_test import _create_request
from pact_test.runners.service_consumers.state_test import _parse_response


class MyPactHelper(PactHelper):
    def setup(self):
        pass

    def tear_down(self):
        pass


class TestLibraryApp(ServiceConsumerTest):
    @state('some books exist')
    def test_get_book(self):
        pass

test_instance = TestLibraryApp()
pact_helper = MyPactHelper()


def test_verify_state(mocker):
    test_instance = TestLibraryApp()
    pact_helper = MyPactHelper()

    mocker.spy(pact_helper, 'setup')
    mocker.spy(pact_helper, 'tear_down')

    response = verify_state(interaction, pact_helper, test_instance).value
    expected_response = {'status': 'PASSED', 'reason': None}

    assert response == expected_response
    assert pact_helper.setup.call_count == 1
    assert pact_helper.tear_down.call_count == 1
    assert pact_helper.tear_down.call_count == 1


def test_create_request():
    request_body = interaction['request']
    request = _create_request(pact_helper.test_url, pact_helper.test_port,
                              request_body).value

    assert request.method == request_body['method']
    assert request.selector == request_body['path'] + request_body['query']
    assert request.headers == request_body.get('headers', {})


def test_parse_text_response():
    request = _create_request('api.ipify.org', None, interaction['request'])
    response = _parse_response(request.value).value
    assert type(response) is str


def test_parse_json_response():
    request = _create_request('ip.jsontest.com', None, interaction['request'])
    response = _parse_response(request.value).value
    assert type(response) is dict


interaction = {
    'providerState': 'some books exist',
    'request': {
        'method': 'GET',
        'path': '',
        'query': '',
        'headers': {
            'Content-type': 'application/json'
        },
        'body': {
            'title': 'The Hitchhicker\'s Guide to the Galaxy'
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

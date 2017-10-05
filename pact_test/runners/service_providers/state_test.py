from pact_test.factories.mock_server_factory import MockServerFactory


def verify_state(decorated_method):
    mock_server = MockServerFactory(decorated_method.with_request, decorated_method.will_respond_with)

    mock_server.start()
    decorated_method()
    mock_server.shutdown()

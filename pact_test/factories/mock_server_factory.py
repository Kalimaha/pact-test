from threading import Thread
from werkzeug.serving import make_server
from pact_test.servers.mock_server import MockServer


class MockServerFactory(Thread):

    def __init__(self, expected_request, mock_response, base_url='127.0.0.1', port=5000):
        Thread.__init__(self)
        self.mock_server = MockServer(expected_request, mock_response)
        self.server = make_server(base_url, port, self.mock_server.app)
        self.context = self.mock_server.app.app_context()
        self.context.push()

    def run(self):
        self.server.serve_forever()

    def shutdown(self):
        self.server.shutdown()

    def request(self):
        return self.mock_server.request

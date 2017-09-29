import requests
from pact_test.factories.mock_server_factory import MockServerFactory


def test_factory():
    req = {'method': 'get', 'path': '/books/42'}
    res = {'status': 200}
    server = MockServerFactory(req, res)
    server.start()
    response = requests.get('http://localhost:5000/books/42')
    server.shutdown()
    assert response.status_code == 200

import json
from threading import Thread
from pact_test.models.response import PactResponse
try:
    import socketserver as SocketServer
    import http.server as SimpleHTTPServer
except ImportError:
    import SocketServer
    import SimpleHTTPServer


ARCHIVE = []


def build_proxy(mock_response=PactResponse()):
    class Proxy(SimpleHTTPServer.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            SimpleHTTPServer.SimpleHTTPRequestHandler.__init__(self, *args, **kwargs)
            self.mock_response = mock_response

        def do_GET(self):
            data = self.read_request_data(self)
            self.handle_request('GET', data)

        def do_POST(self):
            data = self.read_request_data(self)
            self.handle_request('POST', data)

        def do_PUT(self):
            data = self.read_request_data(self)
            self.handle_request('PUT', data)

        def do_DELETE(self):
            data = self.read_request_data(self)
            self.handle_request('DELETE', data)

        @staticmethod
        def read_request_data(other_self):
            header_value = other_self.headers.get('Content-Length')
            data_length = int(header_value) if header_value is not None else None
            return other_self.rfile.read(data_length) if data_length is not None else None

        def format_request(self, http_method, data):
            path_and_query = self.path.split('?')
            path = path_and_query[0]
            query = '?' + path_and_query[1] if len(path_and_query) == 2 else ''

            return {
                'method': http_method,
                'path': path,
                'query': query,
                'body': json.loads(data.decode('utf-8')) if data is not None else data,
                'headers': list(dict([(key, value)]) for key, value in self.headers.items())
            }

        def handle_request(self, http_method, data):
            info = self.format_request(http_method, data)
            ARCHIVE.append(info)
            self.respond()

        def respond(self):
            self.send_response(int(mock_response.status))
            for header in mock_response.headers:
                for key, value in header.items():
                    self.send_header(key, value)
            self.end_headers()
            self.wfile.write(str(mock_response.body).encode())

    return Proxy


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    def __init__(self, server_address, RequestHandlerClass):
        self.allow_reuse_address = True
        SocketServer.TCPServer.__init__(self, server_address, RequestHandlerClass)


class MockServer(object):

    def __init__(self, mock_response=PactResponse(), base_url='0.0.0.0', port=1234):
        self.port = port
        self.base_url = base_url
        self.server = ThreadedTCPServer((self.base_url, self.port), build_proxy(mock_response))
        self.server_thread = Thread(target=self.server.serve_forever)
        self.server_thread.daemon = True
        global ARCHIVE
        ARCHIVE = []

    def start(self):
        self.server_thread.start()

    def shutdown(self):
        self.server.shutdown()
        self.server.server_close()

    @staticmethod
    def report():
        return ARCHIVE

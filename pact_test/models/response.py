class PactResponse(object):
    body = None
    headers = []
    status = 500

    def __init__(self, status=None, body=None, headers=None):
        self.body = body or self.body
        self.status = status or self.status
        self.headers = headers or self.headers

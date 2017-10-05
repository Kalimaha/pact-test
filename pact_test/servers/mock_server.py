from flask import Flask
from flask import request
from flask import Response
from pact_test.constants import *
from pact_test.models.request import PactRequest
from pact_test.models.response import PactResponse


class MockServer(object):

    def __init__(self, req, res):
        if req is None:
            raise Exception(MISSING_REQUEST)

        if res is None:
            raise Exception(MISSING_RESPONSE)

        self.request = self.build_request(req)
        self.response = self.build_response(res)

        self.app = Flask(__name__)
        self.app.add_url_rule(self.request.path, view_func=self.spy, methods=[self.request.method, ])

    def spy(self):
        return self.success() if self.is_matching_request() else self.failure()

    def success(self):
        return Response(
            response=self.response.body,
            status=self.response.status,
            headers=self.response.headers
        )

    def failure(self):
        print('=== === === INSIDE failure === === ===')
        return Response(
            status=500,
            response={
                'message': 'Request is not matching the expectation',
                'expected': {
                    'body': self.request.body,
                    'headers': self.request.headers
                },
                'actual': {
                    'body': request.data,
                    'headers': request.headers
                }
            }
        )

    def is_matching_request(self):
        return True

    @staticmethod
    def build_request(user_request):
        return PactRequest(
            body=user_request.get('body'),
            path=user_request.get('path') or '/',
            query=user_request.get('query'),
            method=user_request.get('method'),
            headers=user_request.get('headers')
        )

    @staticmethod
    def build_response(user_response):
        return PactResponse(
            status=user_response.get('status'),
            body=user_response.get('body'),
            headers=user_response.get('headers')
        )

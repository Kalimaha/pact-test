import os
import sys
import imp
import json
import urllib.parse
import urllib.request
from urllib.request import Request
from pact_test.utils.pytest_utils import read_marker
from pact_test.executors.executor import Executor
from pact_test.pact_markers import STATE
from pact_test.pact_markers import PACT_URI
from pact_test.pact_markers import HONOURS_PACT_WITH


class ProviderExecutor(Executor):
    REQUIRED_PARAMETERS = [STATE, PACT_URI, HONOURS_PACT_WITH]
    PACT_HELPER = 'pact_helper.py'
    PACT_HELPER_NOT_FOUND = 'Could\'n find "pact_helper.py" script in Pact test directory.'
    SET_UP_NOT_FOUND = 'Module pact_helper MUST have a set_up method'
    TEAR_DOWN_NOT_FOUND = 'Module pact_helper MUST have a tear_down method'
    MISSING_STATE_SETUP = 'Missing state setup'
    BASE_URL = 'http://localhost:1234'

    def set_up(self):
        path_to_pact_helper = self.pact_helper_path()
        self.pact_helper = self.load_pact_helper(path_to_pact_helper)
        self.pact_helper.set_up()

    def verify_pact(self):
        interactions = self.load_interactions()
        state = read_marker(self.pyfuncitem, STATE)
        for interaction in interactions:
            if interaction['providerState'] == state:
                return self.verify_interaction(interaction)

    def verify_interaction(self, interaction):
        req = self.build_request(interaction['request'])
        response = urllib.request.urlopen(req)
        consumer_response = interaction['response']

        response_headers = response.getheaders()
        response_status = response.status
        response_reason = response.reason
        response_body = json.loads(response.read().decode())

        status_matches = self.status_matches(consumer_response['status'], response_status)
        headers_match = self.headers_match(consumer_response['headers'], response_headers)
        body_matches = self.body_matches(consumer_response['body'], response_body)

        return status_matches and headers_match and body_matches

    def body_matches(self, consumer_body, response_body):
        return consumer_body.items() <= response_body.items()

    def headers_match(self, consumer_headers, response_headers):
        return consumer_headers.items() <= dict(response_headers).items()

    def reason_matches(self, consumer_reason, response_reason):
        return consumer_reason == response_reason

    def status_matches(self, consumer_status, response_status):
        return consumer_status == response_status

    def build_request(self, consumer_request):
        url = urllib.parse.urljoin(self.BASE_URL, consumer_request['path'])
        url += consumer_request.get('query', '')
        method = consumer_request.get('method', 'GET')
        headers = consumer_request.get('headers', {})
        data = consumer_request.get('body', {})
        return Request(url=url, method=method, headers=headers, data=data)

    def load_interactions(self):
        return self.fetch_pact_file()['interactions']

    def fetch_pact_file(self):
        pact_uri = read_marker(self.pyfuncitem, PACT_URI)
        if pact_uri.startswith(('http://', 'https://')):
            with urllib.request.urlopen(pact_uri) as f:
                pact = json.load(f)
        else:
            with open(pact_uri) as f:
                pact = json.load(f)
        return pact

    def tear_down(self):
        self.pact_helper.tear_down()

    def load_pact_helper(self, path_to_pact_helper):
        pact_helper = imp.load_source('pact_helper', path_to_pact_helper)
        if hasattr(pact_helper, 'set_up') is False: raise Exception(self.SET_UP_NOT_FOUND)
        if hasattr(pact_helper, 'tear_down') is False: raise Exception(self.TEAR_DOWN_NOT_FOUND)
        return pact_helper

    def pact_helper_path(self):
        test_dir = os.path.dirname(self.pyfuncitem.fspath)
        files = [f for f in os.listdir(test_dir) if f == self.PACT_HELPER]
        if not files: raise Exception(self.PACT_HELPER_NOT_FOUND)
        pact_helper_path = os.path.join(test_dir, files[0])
        return pact_helper_path

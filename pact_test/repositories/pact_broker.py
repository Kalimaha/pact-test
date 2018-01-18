import json
import requests
from pact_test.either import *
from pact_test.utils.logger import *
from pact_test.utils.pact_helper_utils import format_headers


PACT_BROKER_URL = 'http://localhost:9292/'


def upload_pact(provider_name, consumer_name, pact, base_url=PACT_BROKER_URL):
    pact = format_headers(pact)
    current_version = get_latest_version(consumer_name, base_url)
    if type(current_version) is Right:
        v = next_version(current_version.value)
        try:
            url = base_url + 'pacts/provider/' + provider_name + '/consumer/' + consumer_name + '/version/' + v
            payload = json.dumps(pact)
            headers = {'content-type': 'application/json'}
            response = requests.put(url, data=payload, headers=headers)
            return Right(response.json())
        except requests.exceptions.ConnectionError as e:
            msg = 'Failed to establish a new connection with ' + base_url
            return Left(msg)
    return current_version


def get_latest_version(consumer_name, base_url=PACT_BROKER_URL):
    try:
        url = base_url + 'pacticipants/' + consumer_name + '/versions/'
        response = requests.get(url)
        if response.status_code is not 200:
            return Right('1.0.0')
        return Right(response.json()['_embedded']['versions'][0]['number'])
    except requests.exceptions.ConnectionError as e:
        msg = 'Failed to establish a new connection with ' + base_url
        return Left(msg)


def next_version(current_version='1.0.0'):
    versions = current_version.split('.')
    next_minor = str(1 + int(versions[-1]))
    return '.'.join([versions[0], versions[1], next_minor])

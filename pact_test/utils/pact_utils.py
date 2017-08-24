import json
import requests
from pact_test.either import *
from pact_test.utils.logger import debug


def get_pact(location):
    if location.startswith(('http', 'https')):
        return __get_pact_from_url(location)
    return __get_pact_from_file(location)


def __get_pact_from_file(filename):
    debug('Get pact from file "' + str(filename) + '"')
    try:
        with open(filename) as file_content:
            return Right(json.loads(file_content.read()))
    except Exception as e:
        return Left(str(e))


def __get_pact_from_url(url):
    debug('Get pact from URL "' + str(url) + '"')
    try:
        return Right(requests.get(url).json())
    except Exception as e:
        return Left(str(e))

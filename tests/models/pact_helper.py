from pact_test import PactHelper


pact_helper = PactHelper()


def test_default_url():
    assert pact_helper.test_url == 'localhost'


def test_default_port():
    assert pact_helper.test_port == 9999

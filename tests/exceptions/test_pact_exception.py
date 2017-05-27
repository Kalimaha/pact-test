from pact_test.exceptions import PactTestException


def test_message():
    try:
        raise PactTestException('Pact Error')
    except PactTestException as e:
        assert str(e) == 'Pact Error'

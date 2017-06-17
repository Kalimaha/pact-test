from pact_test.runners import pact_tests_runner


def test_consumer_tests(mocker):
    mocker.spy(pact_tests_runner, 'run_consumer_tests')
    pact_tests_runner.verify(verify_consumers=True)
    assert pact_tests_runner.run_consumer_tests.call_count == 1


def test_provider_tests(mocker):
    mocker.spy(pact_tests_runner, 'run_provider_tests')
    pact_tests_runner.verify(verify_providers=True)
    assert pact_tests_runner.run_provider_tests.call_count == 1


def test_default_setup(mocker):
    mocker.spy(pact_tests_runner, 'run_consumer_tests')
    mocker.spy(pact_tests_runner, 'run_provider_tests')
    pact_tests_runner.verify()
    assert pact_tests_runner.run_consumer_tests.call_count == 0
    assert pact_tests_runner.run_provider_tests.call_count == 0

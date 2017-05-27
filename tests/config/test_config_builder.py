import os
from pact_test.config.config_builder import Config


def test_default_consumer_tests_path():
    config = Config()
    assert config.consumer_tests_path == 'tests/service_consumers'


def test_default_provider_tests_path():
    config = Config()
    assert config.provider_tests_path == 'tests/service_providers'


def test_default_pact_broker_uri():
    config = Config()
    assert config.pact_broker_uri is None


def test_custom_consumer_tests_path():
    class TestConfig(Config):
        def path_to_user_config_file(self):
            return os.path.join(os.getcwd(), 'tests',
                                'resources', 'config',
                                'consumer_only.json')

    config = TestConfig()
    assert config.pact_broker_uri is None
    assert config.consumer_tests_path == 'mypath/mytests'
    assert config.provider_tests_path == 'tests/service_providers'


def test_custom_provider_tests_path():
    class TestConfig(Config):
        def path_to_user_config_file(self):
            return os.path.join(os.getcwd(), 'tests',
                                'resources', 'config',
                                'provider_only.json')

    config = TestConfig()
    assert config.pact_broker_uri is None
    assert config.provider_tests_path == 'mypath/mytests'
    assert config.consumer_tests_path == 'tests/service_consumers'


def test_custom_pact_broker_uri():
    class TestConfig(Config):
        def path_to_user_config_file(self):
            return os.path.join(os.getcwd(), 'tests',
                                'resources', 'config',
                                'pact_broker_only.json')

    config = TestConfig()
    assert config.pact_broker_uri == 'mypath/mytests'
    assert config.provider_tests_path == 'tests/service_providers'
    assert config.consumer_tests_path == 'tests/service_consumers'


def test_user_settings():
    class TestConfig(Config):
        def path_to_user_config_file(self):
            return os.path.join(os.getcwd(), 'tests',
                                'resources', 'config',
                                '.pact.json')

    config = TestConfig()
    assert config.pact_broker_uri == 'mypath/mybroker'
    assert config.provider_tests_path == 'mypath/myprovider'
    assert config.consumer_tests_path == 'mypath/myconsumer'

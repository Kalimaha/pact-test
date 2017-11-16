import os
import json


class Config(object):
    pact_broker_uri = 'http://localhost:9292/'
    consumer_tests_path = 'tests/service_consumers'
    provider_tests_path = 'tests/service_providers'
    pacts_path = 'pacts'
    CONFIGURATION_FILE = '.pact.json'

    def __init__(self):
        user_config_file = self.path_to_user_config_file()
        if os.path.isfile(user_config_file):
            with open(user_config_file) as f:
                self.load_user_settings(f)

    def load_user_settings(self, user_settings_file):
        settings = json.loads(user_settings_file.read())
        [self.custom_or_default(settings, key) for key in settings.keys()]

    def path_to_user_config_file(self):
        return os.path.join(os.getcwd(), self.CONFIGURATION_FILE)

    def custom_or_default(self, user_settings, key):
        setattr(self, key, user_settings.get(key, getattr(self, key)))

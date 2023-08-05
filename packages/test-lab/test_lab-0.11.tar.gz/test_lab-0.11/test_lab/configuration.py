import json
import os


class Configuration(object):
    def __init__(self, path_or_json):
        if isinstance(path_or_json, dict):
            self.json = path_or_json
        elif path_or_json and os.path.isfile(path_or_json):
            self.json = json.load(open(path_or_json))
        else:
            raise RuntimeError('Cannot load configuration json')

    def get(self, client, key, default=None):
        if client not in self.json['clients'] and default is None:
            raise RuntimeError('Cannot find parameter [clients]->[{}]->[{}] in configuration json'.format(client, key))
        if key not in self.json['clients'][client] and default is None:
            raise RuntimeError('Cannot find parameter [clients]->[{}]->[{}] in configuration json'.format(client, key))
        return self.json['clients'][client].get(key, default)

    def get_scenario_config_value(self, scenario, key):
        for test_config in self.json['scenarios']:
            if test_config['name'] == scenario and key in test_config:
                return test_config[key]
        return None

    def get_scenario_app_args(self, scenario):
        value = str(self.get_scenario_config_value(scenario, 'app_args'))
        value = value.format(name=scenario)
        return value

    def get_scenario_timeout(self, scenario):
        return self.get_scenario_config_value(scenario, 'timeout')

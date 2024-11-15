import os
import json

class Config:
    def __init__(self):
        self.configuration = self.load_config()

    def load_config(self):
        possible_paths = [
            os.path.join(os.path.dirname(os.path.dirname(__file__)), 'configuration.json'),
            os.path.join(os.path.dirname(__file__), 'config', 'configuration.json'),
            os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')), 'configuration.json'),
            os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')), 'config', 'configuration.json'),
            os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')), 'configuration.json'),
            os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')), 'config', 'configuration.json'),
        ]

        for config_path in possible_paths:
            if os.path.exists(config_path):
                with open(config_path, 'r') as config_file:
                    return json.load(config_file)

        raise FileNotFoundError(f"Config file 'configuration.json' not found in the project's root directory. Tried to load from: {', '.join(possible_paths)}")    
    
    def __getitem__(self, key):
        return self.configuration[key]

    def get(self, key, default=None):
        return self.configuration.get(key, default)

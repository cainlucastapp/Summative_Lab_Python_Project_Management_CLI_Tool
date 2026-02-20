
import json
import os


def load_settings(filepath="./settings.json"):
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r') as file:
                return json.load(file)
        except (json.JSONDecodeError, IOError) as error:
            print(f"Error loading settings: {error}")
    return {}


def get_settings(key, default=None):
    settings = load_settings()
    return settings.get(key, default)
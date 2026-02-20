
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


def load_data(filepath):
    if not os.path.exists(filepath):
        return []
    try:
        with open(filepath, 'r') as file:
            return json.load(file)
    except (json.JSONDecodeError, IOError) as error:
        print(f"Error loading data from {filepath}: {error}")
        return []
    

def save_data(filepath, data):
    # Ensure the directory exists
    directory = os.path.dirname(filepath)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)
        
    try:
        with open(filepath, 'w') as file:
            return json.dump(data, file, indent=2)
    except (IOError) as error:
        print(f"Error saving data to {filepath}: {error}")
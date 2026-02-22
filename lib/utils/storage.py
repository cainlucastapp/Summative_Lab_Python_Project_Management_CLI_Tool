# utils/storage.py

# Requires
import json
import os


# Load settings from JSON file
def load_settings(filepath="./settings.json"):
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r') as file:
                return json.load(file)
        except (json.JSONDecodeError, IOError) as error:
            print(f"Error loading settings: {error}")
    return {}


# Get a specific setting by key
def get_settings(key, default=None):
    settings = load_settings()
    return settings.get(key, default)


# Load data from JSON file
def load_data(filepath):
    # Return empty list if file does not exist
    if not os.path.exists(filepath):
        return []
    
    try:
        with open(filepath, 'r') as file:
            return json.load(file)
    except (json.JSONDecodeError, IOError) as error:
        print(f"Error loading data from {filepath}: {error}")
        return []
    

# Save data to JSON file
def save_data(filepath, data):
    # Create directory if it does not exist
    directory = os.path.dirname(filepath)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)
    
    try:
        with open(filepath, 'w') as file:
            return json.dump(data, file, indent=2)
    except (IOError) as error:
        print(f"Error saving data to {filepath}: {error}")
import json
import os

def load_config():
    config = None

    # Correct way to construct the path relative to the current file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(current_dir, '..', 'simulation_config.json')
    config_path = os.path.normpath(config_path)  # Normalize the path to resolve any '..'

    print("Configuration Path:", config_path)

    try:
        with open(config_path, 'r') as config_file:
            config = json.load(config_file)
    except FileNotFoundError:
        print(f"Failed to open the configuration file at {config_path}. Please check the file path.")

    return config

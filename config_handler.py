import json

CONFIG_FILE = "config.json"

def load_config():
    with open(CONFIG_FILE, 'r') as file:
        return json.load(file)

def get_datasphere_host():
    config = load_config()
    return config.get("datasphere_host", None)

def set_datasphere_host(new_host):
    config = load_config()
    config["datasphere_host"] = new_host
    with open(CONFIG_FILE, 'w') as file:
        json.dump(config, file, indent=4)
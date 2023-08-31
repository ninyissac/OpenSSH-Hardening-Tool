from configparser import ConfigParser, ExtendedInterpolation
import os

config = ConfigParser(interpolation=ExtendedInterpolation())

# Path to the configuration file
# CONFIG_PATH = "program/config.ini"
CONFIG_PATH = os.environ.get("CONFIG_PATH")
config.read(CONFIG_PATH)

# Extract information about contexts and program details
contexts_config = {}
for k, v in config.items("contexts"):
    contexts_config[k] = v

program_name = contexts_config["name"]
program_description = contexts_config["description"]
contexts = contexts_config["contexts"].split(",")

# Extract context-specific settings
context_config = {}
for c in contexts:
    c = c.strip()
    context_config[c] = {}

    for k, v in config.items(c):
        context_config[c][k] = v

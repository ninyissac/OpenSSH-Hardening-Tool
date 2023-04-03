from configparser import ConfigParser, ExtendedInterpolation
import os

config = ConfigParser(interpolation=ExtendedInterpolation())

# CONFIG_PATH = "program/config.ini"

CONFIG_PATH = os.environ.get("CONFIG_PATH")

config.read(CONFIG_PATH)

default_config = {}
for k, v in config.items("default"):
    default_config[k] = v

program_name = default_config["name"]
program_description = default_config["description"]

contexts = default_config["contexts"].split(",")

context_config = {}
for c in contexts:
    c = c.strip()
    context_config[c] = {}

    for k, v in config.items(c):
        context_config[c][k] = v


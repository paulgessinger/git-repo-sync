import yaml
from schema import Schema, And, Use, Optional


schema = Schema({})

def load_config(path):
    with open(path, "r") as f:
        conf = yaml.load(f)

    return conf


import yaml
from schema import Schema, And, Use, Optional


schema = Schema([{'src': str,
                   'dest': str,
                   'branches': [str]}])

def load_config(path):
    with open(path, "r") as f:
        conf = yaml.load(f)

    assert schema.validate(conf)

    return conf


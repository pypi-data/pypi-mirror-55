import os
import json
import jsonschema

__configurations_file_path__ = './configurations.json'
__loaded_configurations__ = None


def __load_configurations__():
    global __loaded_configurations__

    if __loaded_configurations__ is not None:
        return

    if not os.path.exists(__configurations_file_path__):
        raise FileExistsError("Configuration file '%s' not found" % __configurations_file_path__)

    with open(__configurations_file_path__) as json_file:
        __loaded_configurations__ = json.load(json_file)


def __validate_configurations__():
    global __loaded_configurations__

    if __loaded_configurations__ is None:
        raise ImportError("Can't validate configurations (Not loaded yet")

    schema_file_path = os.path.dirname(os.path.realpath(__file__)) + '/configurationSchema.json'

    with open(schema_file_path) as json_file:
        schema = json.load(json_file)

        jsonschema.validate(instance=__loaded_configurations__, schema=schema)


def get(module, key):
    global __loaded_configurations__

    if __loaded_configurations__ is None:
        __load_configurations__()
        __validate_configurations__()

    if module not in __loaded_configurations__:
        raise KeyError("Configuration module '%s' not found" % module)

    if key not in __loaded_configurations__[module]:
        raise KeyError("Configuration '%s' not found under module '%s'" % (key, module))

    return __loaded_configurations__[module][key]

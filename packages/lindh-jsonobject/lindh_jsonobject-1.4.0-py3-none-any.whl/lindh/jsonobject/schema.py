import logging
import json


_schemas = {}


def register_schema(klass):
    logging.debug("Registered schema %s", klass.__name__)
    _schemas[klass.__name__] = klass


def get_schema(schema):
    return _schemas.get(schema)


def wrap_raw_json(json_string):
    if json_string is None:
        return None
    d = json.loads(json_string)
    return wrap_dict(d)


def wrap_dict(d):
    if d is None:
        return None
    schema = d.get('*schema')
    klass = get_schema(schema)
    if klass is None:
        raise NameError("No such schema '%s'" % schema)
    return klass(d)

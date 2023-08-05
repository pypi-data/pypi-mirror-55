# Flask imports
from flask import request, abort, BadRequest

# JSON SChema Imports
from jsonschema import validate, ValidationError

# Default extensions
from extensions import DefaultsExtension


def validate_json(f):
    # Validate the json
    try:
        request.get_json()
    except BadRequest, e:
        msg = "payload must be a valid json"
        return abort(400, {"error": msg})


def validate_schema(schema=None, force=False, fill_defaults=False):
    # Validate the schema of the json
    data = request.get_json(force=force)

    if data is None:
        return abort(400, 'Failed to decode JSON object')

    try:
        if fill_defaults:
            DefaultsExtension(schema).validate(data)
        else:
            validate(data, schema)
    except ValidationError as e:
        return abort(400, e)

"""JSON Schema validation service."""

import jsonschema


def validate_json(data: dict, schema: dict) -> list[dict]:
    errors = []
    validator = jsonschema.Draft202012Validator(schema)
    for error in validator.iter_errors(data):
        errors.append({
            "path": ".".join(str(p) for p in error.absolute_path) or "$",
            "message": error.message,
            "severity": "error",
        })
    return errors

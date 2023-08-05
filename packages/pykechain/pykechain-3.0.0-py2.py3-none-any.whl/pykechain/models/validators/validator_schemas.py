from pykechain.enums import PropertyVTypes, PropertyRepresentation

#
# Validators and Validator Effects
#

effects_jsonschema_stub = {
    "type": "object",
    "additionalProperties": False,
    "required": ["effect", "config"],
    "properties": {
        "effect": {"type": ["string", "null"]},
        "config": {"type": "object"}
    }
}

validator_jsonschema_stub = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "object",
    "title": "Single Validator JSON schema",
    "additionalProperties": False,
    "required": ["vtype", "config"],
    "properties": {
        "vtype": {"type": "string", "enum": PropertyVTypes.values()},
        "config": {
            "type": "object",
            "properties": {
                "on_valid": {"type": "array", "items": effects_jsonschema_stub},
                "on_invalid": {"type": "array", "items": effects_jsonschema_stub}
            }
        }
    }
}

validators_options_json_schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "Validators JSON schema",
    "type": "array",
    "items": validator_jsonschema_stub
}

#
# Representation of a property configurations
#

representation_jsonschema_stub = {
    "type": "object",
    "additionalProperties": False,
    "required": ["rtype", "config"],
    "properties": {
        "rtype": {"type": "string", "enum": PropertyRepresentation.values()},
        "config": {"type": "object"}
    }
}

representation_options_json_schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "Validators JSON schema",
    "type": "array",
    "items": representation_jsonschema_stub
}

#
# Property Value Options json schema
#

options_json_schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "Toplevel Property Options JSON schema",
    "type": "object",
    "additionalProperties": True,
    "properties": {
        # Validators
        "validators": validators_options_json_schema,

        # Reference Property additional options to hide columns and store filters
        "propmodels_excl": {"type": "array"},
        "propmodels_incl": {"type": "array"},
        "prefilters": {"type": "object"},

        # Representations
        "representation": representation_options_json_schema,
    }
}

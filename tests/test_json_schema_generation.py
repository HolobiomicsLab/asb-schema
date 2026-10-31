"""Representation fixes belong to schema generation, not patched output copies."""

import json
from pathlib import Path

import jsonschema
import pytest


@pytest.mark.parametrize("domain", ("metabolomics", "proteomics", "genomics", "astronomy"))
def test_generator_preserves_object_and_optional_enum_constraints(domain):
    from asb_schema.jsonschemagen import ASBJsonSchemaGenerator

    source = f"""
id: https://example.org/{domain}
name: synthetic_contract
prefixes:
  linkml: https://w3id.org/linkml/
imports:
  - linkml:types
default_range: string
enums:
  Choice:
    permissible_values:
      first:
      second:
classes:
  OpenObject:
    class_uri: linkml:Any
    annotations:
      json_schema_type: object
  Envelope:
    tree_root: true
    attributes:
      optional_choice:
        range: Choice
      required_choice:
        range: Choice
        required: true
      choices:
        range: Choice
        multivalued: true
      records:
        range: OpenObject
        multivalued: true
        inlined: true
        inlined_as_list: true
"""
    schema = json.loads(ASBJsonSchemaGenerator(source, not_closed=True).serialize())
    validator = jsonschema.validators.validator_for(schema)(schema)
    valid = {"optional_choice": None, "required_choice": "first", "choices": ["second"],
             "records": [{"arbitrary": {"values": [1, None, True]}}]}
    validator.validate(valid)
    for field, bad_values in {
        "optional_choice": ("other", 3, True, [], {}),
        "required_choice": (None, "other"),
        "choices": ([None], ["other"]),
        "records": (["text"], [None], [[]], [True], [3]),
    }.items():
        for bad in bad_values:
            assert list(validator.iter_errors({**valid, field: bad})), (field, bad)


@pytest.mark.parametrize("name", ("asb_card", "asb_capsule", "asb_trace", "asb_skill_bundle",
                                  "asb_skill_collection", "asb_skill_collection_registry"))
def test_checked_in_json_schema_equals_source_generation(name):
    from asb_schema.jsonschemagen import ASBJsonSchemaGenerator

    root = Path(__file__).resolve().parents[1] / "src/asb_schema"
    generated = json.loads(ASBJsonSchemaGenerator(str(root / f"{name}.yaml"), not_closed=True).serialize())
    stored = json.loads((root / f"{name}.schema.json").read_text())
    assert generated == stored

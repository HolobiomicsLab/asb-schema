"""Cards written by the reference pipeline validate closed against ASBTaskCard.

The fixtures in tests/fixtures/reference/ are one card from a heuristic build of
the reference pipeline's minimal example package and three released benchmark
cards of asb-skill-collections (epigenomics, metabolomics and transcriptomics
v1). Their source_package is made relative and one e-mail address quoted from
the source article is removed; every key and every other value is as written.

Closed validation is the documented conformance check: an undeclared key, at
the top level or in a nested object, is an error.
"""

import inspect
import json
from pathlib import Path

import jsonschema
import pytest
from linkml.validator import Validator
from linkml.validator.plugins import JsonschemaValidationPlugin

from asb_schema import get_json_schema_path, get_schema_path

FIXTURES = sorted((Path(__file__).parent / "fixtures" / "reference").glob("*.json"))


def _load(path):
    return json.loads(path.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def linkml_validator():
    # Same plugin and options as the documented command:
    # linkml-validate --target-class ASBTaskCard --allow-null-for-optional-enums
    if "allow_null_for_optional_enums" not in inspect.signature(JsonschemaValidationPlugin).parameters:
        pytest.skip("--allow-null-for-optional-enums needs linkml 1.11 or later")
    plugin = JsonschemaValidationPlugin(closed=True, allow_null_for_optional_enums=True)
    return Validator(get_schema_path("asb_card"), validation_plugins=[plugin])


@pytest.fixture(scope="module")
def closed_json_schema_validator():
    schema = json.loads(Path(get_json_schema_path("asb_card")).read_text())
    target = {"$schema": schema["$schema"], "$ref": "#/$defs/ASBTaskCard", "$defs": schema["$defs"]}
    return jsonschema.Draft201909Validator(target)


def test_fixture_set_covers_heuristic_and_released_cards():
    names = [path.name for path in FIXTURES]
    assert sum(name.startswith("heuristic_") for name in names) == 1
    assert sum(name.startswith("released_") for name in names) == 3


@pytest.mark.parametrize("path", FIXTURES, ids=lambda path: path.stem)
def test_reference_card_validates_closed_with_linkml(path, linkml_validator):
    report = linkml_validator.validate(_load(path), "ASBTaskCard")
    errors = [result.message for result in report.results if result.severity.name == "ERROR"]
    assert errors == []


@pytest.mark.parametrize("path", FIXTURES, ids=lambda path: path.stem)
def test_reference_card_validates_against_closed_json_schema(path, closed_json_schema_validator):
    errors = [error.message for error in closed_json_schema_validator.iter_errors(_load(path))]
    assert errors == []


@pytest.mark.parametrize("path", [p for p in FIXTURES if p.name.startswith("released_")], ids=lambda path: path.stem)
def test_released_card_validates_closed_without_null_enum_option(path):
    plugin = JsonschemaValidationPlugin(closed=True)
    report = Validator(get_schema_path("asb_card"), validation_plugins=[plugin]).validate(_load(path), "ASBTaskCard")
    assert [result.message for result in report.results if result.severity.name == "ERROR"] == []


def test_undeclared_key_is_still_rejected(linkml_validator):
    card = _load(FIXTURES[0])
    card["not_a_card_slot"] = "value"
    report = linkml_validator.validate(card, "ASBTaskCard")
    assert any("not_a_card_slot" in result.message for result in report.results)

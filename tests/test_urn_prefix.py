"""The LinkML files use the urn:asb: prefix and contain no urn:scitask: identifier."""

import yaml
from pathlib import Path

SCHEMA_DIR = Path(__file__).parent.parent / "src/asb_schema"


def test_no_urn_scitask_in_any_yaml():
    for yml in SCHEMA_DIR.glob("*.yaml"):
        text = yml.read_text()
        assert "urn:scitask" not in text, f"{yml.name} still contains urn:scitask:"


def test_asb_urn_prefix_declared():
    """Either the top schema or one of the sub-schemas should map an `asb` prefix
    we can use for urn:asb: nodes. We just check the prefix string is bound."""
    found = False
    for yml in SCHEMA_DIR.glob("*.yaml"):
        data = yaml.safe_load(yml.read_text()) or {}
        prefixes = data.get("prefixes", {}) or {}
        if "asb" in prefixes:
            found = True
            assert prefixes["asb"].startswith("https://w3id.org/holobiomicslab/asb-schema/")
    assert found, "No 'asb' prefix declared in any asb-schema LinkML file"

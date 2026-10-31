"""IDEAS-I: SkillCollectionRegistry — catalogue root."""

import yaml
from pathlib import Path

SCHEMA = Path(__file__).parent.parent / "src/asb_schema/asb_skill_collection_registry.yaml"


def test_file_exists_and_parses():
    assert SCHEMA.is_file()
    data = yaml.safe_load(SCHEMA.read_text())
    assert data["name"] == "asb_skill_collection_registry_v0_2"


def test_registry_is_tree_root():
    data = yaml.safe_load(SCHEMA.read_text())
    assert data["classes"]["SkillCollectionRegistry"].get("tree_root") is True


def test_registry_slots():
    data = yaml.safe_load(SCHEMA.read_text())
    slots = set(data["classes"]["SkillCollectionRegistry"].get("slots") or [])
    expected = {
        "registry_iri",
        "registry_title",
        "registry_description",
        "registry_maintainers",
        "collections",
        "external_repos",
        "generated_at",
    }
    missing = expected - slots
    assert not missing, f"SkillCollectionRegistry missing slots: {missing}"


def test_external_repos_off_by_default():
    """IDEAS-I + spec §9.2 + §15: external_repos[] is reserved but not enabled in v1."""
    data = yaml.safe_load(SCHEMA.read_text())
    slot = data["slots"]["external_repos"]
    # We mark it nice_to_have to encode "reserved, off in v1"
    assert slot.get("annotations", {}).get("importance") == "nice_to_have"
    desc = (slot.get("description") or "").lower()
    assert "reserved" in desc or "v1" in desc, "external_repos description must flag it as v1-reserved"

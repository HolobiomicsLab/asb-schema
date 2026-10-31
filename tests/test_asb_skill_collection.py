"""IDEAS-B: SkillCollection LinkML class — release unit, tree_root."""
import yaml
from pathlib import Path

SCHEMA = Path(__file__).parent.parent / "src/asb_schema/asb_skill_collection.yaml"


def test_file_exists_and_parses():
    assert SCHEMA.is_file(), "asb_skill_collection.yaml missing"
    data = yaml.safe_load(SCHEMA.read_text())
    assert data["name"] == "asb_skill_collection_v0_3"
    assert data["version"] == "0.3.0"


def test_skill_collection_is_tree_root():
    data = yaml.safe_load(SCHEMA.read_text())
    assert data["classes"]["SkillCollection"].get("tree_root") is True


def test_skill_collection_required_slot_list():
    data = yaml.safe_load(SCHEMA.read_text())
    slots = list(data["classes"]["SkillCollection"].get("slots") or [])
    expected = {
        "iri", "slug", "version", "title", "description", "license",
        "contributors", "doi", "released_at",
        "skills", "tools",
        "edam_topics",
        "source_collections", "catalogue_membership",
        "ro_crate_path",
    }
    missing = expected - set(slots)
    assert not missing, f"SkillCollection missing slots: {missing}"


def test_skill_collection_contributors_is_person():
    data = yaml.safe_load(SCHEMA.read_text())
    contrib = data["slots"]["contributors"]
    assert contrib["range"] == "Person"
    assert contrib.get("multivalued") is True


def test_person_class_present_with_orcid():
    data = yaml.safe_load(SCHEMA.read_text())
    person = data["classes"]["Person"]
    attrs = set((person.get("attributes") or {}).keys())
    assert {"name", "orcid", "affiliation"}.issubset(attrs), (
        f"Person missing slots: {attrs}"
    )


def test_skill_collection_imports_skill_bundle():
    data = yaml.safe_load(SCHEMA.read_text())
    assert "asb_skill_bundle" in (data.get("imports") or [])

"""Smoke tests for the asb-schema LinkML sub-package (post-Wave1 rename)."""

import yaml
from pathlib import Path

SCHEMA_DIR = Path(__file__).parent.parent / "src/asb_schema"

CARD_SCHEMA = SCHEMA_DIR / "asb_card.yaml"
CAPSULE_SCHEMA = SCHEMA_DIR / "asb_capsule.yaml"
BUNDLE_SCHEMA = SCHEMA_DIR / "asb_skill_bundle.yaml"
TOP_SCHEMA = SCHEMA_DIR / "asb.yaml"
COLLECTION_SCHEMA = SCHEMA_DIR / "asb_skill_collection.yaml"
COLLECTION_REGISTRY_SCHEMA = SCHEMA_DIR / "asb_skill_collection_registry.yaml"


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------


def _all_mappings(defn: dict) -> bool:
    """Return True if the slot definition has at least one ontology mapping."""
    return bool(
        defn.get("exact_mappings")
        or defn.get("narrow_mappings")
        or defn.get("close_mappings")
        or defn.get("broad_mappings")
    )


def _slots_from_attrs(classes: dict) -> dict:
    """Collect inline attribute definitions from all classes."""
    attrs = {}
    for cls_name, cls_def in classes.items():
        if not isinstance(cls_def, dict):
            continue
        for attr_name, attr_def in (cls_def.get("attributes") or {}).items():
            attrs[f"{cls_name}.{attr_name}"] = attr_def or {}
    return attrs


# ===========================================================================
# Top-level schema tests
# ===========================================================================


def test_top_schema_is_valid_yaml():
    data = yaml.safe_load(TOP_SCHEMA.read_text())
    assert data["name"] == "asb_standard"
    assert data["version"] == "0.2.0"


def test_top_schema_imports_all_sub_schemas():
    data = yaml.safe_load(TOP_SCHEMA.read_text())
    imports = data.get("imports", [])
    for needle in (
        "asb_card",
        "asb_capsule",
        "asb_skill_bundle",
        "asb_skill_collection",
        "asb_skill_collection_registry",
    ):
        assert needle in imports, f"Top schema must import {needle}"


# ===========================================================================
# asb_card.yaml
# ===========================================================================


def test_card_schema_is_valid_yaml():
    data = yaml.safe_load(CARD_SCHEMA.read_text())
    assert data["name"] == "asb_card_v0_3"
    assert "classes" in data
    assert "slots" in data


def test_card_required_classes_present():
    data = yaml.safe_load(CARD_SCHEMA.read_text())
    classes = data.get("classes", {})
    required_classes = [
        "ASBTaskCard",
        "AvailableArtifact",
        "EvidenceSnippet",
        "EvaluationStrategy",
        "TypedArtifact",
        "ExecutionProfile",
        "ProvenanceLinks",
        "TaskPort",
    ]
    for cls in required_classes:
        assert cls in classes, f"Class '{cls}' missing from asb_card schema"


def test_card_tree_root():
    data = yaml.safe_load(CARD_SCHEMA.read_text())
    classes = data.get("classes", {})
    assert classes.get("ASBTaskCard", {}).get("tree_root") is True


def test_card_required_slots_present():
    data = yaml.safe_load(CARD_SCHEMA.read_text())
    slots = data.get("slots", {})
    required_slots = [
        "task_id",
        "title",
        "source_package",
        "research_question",
        "finding",
        "task_description",
        "inputs",
        "expected_outputs",
        "tools",
        "skills",
        "workflow_description",
        "evaluation_strategy",
        "created_at",
        "schema_version",
        "scitask_version",
        "crossref_doi",
        "domain",
        "keywords",
        "data_accessions",
        "methodology_summary",
        "provenance_source",
        "reproducibility_tier",
        "expected_artifact_name",
        "synthesized_from",
    ]
    for s in required_slots:
        assert s in slots, f"Slot '{s}' missing from asb_card schema"


def test_card_slot_importance_covers_all_tiers():
    data = yaml.safe_load(CARD_SCHEMA.read_text())
    slots = data.get("slots", {})
    importance_values = set()
    for name, defn in slots.items():
        ann = (defn or {}).get("annotations", {})
        if "importance" in ann:
            importance_values.add(ann["importance"])
    assert importance_values.issuperset({"must_have", "should_have", "nice_to_have"}), (
        f"Missing importance tiers. Found: {importance_values}"
    )


def test_card_every_slot_has_ontology_mapping():
    data = yaml.safe_load(CARD_SCHEMA.read_text())
    slots = data.get("slots", {})
    missing = [name for name, defn in slots.items() if not _all_mappings(defn or {})]
    assert len(missing) == 0, f"Top-level slots missing ontology mappings: {missing}"


def test_card_every_attribute_has_ontology_mapping():
    data = yaml.safe_load(CARD_SCHEMA.read_text())
    classes = data.get("classes", {})
    missing = []
    for key, defn in _slots_from_attrs(classes).items():
        if not _all_mappings(defn):
            missing.append(key)
    assert len(missing) == 0, f"Class attributes missing ontology mappings: {missing}"


def test_card_slot_count_at_least_20():
    data = yaml.safe_load(CARD_SCHEMA.read_text())
    slots = data.get("slots", {})
    assert len(slots) >= 20, f"Expected >=20 top-level slots, found {len(slots)}"


# ===========================================================================
# asb_capsule.yaml
# ===========================================================================


def test_capsule_schema_is_valid_yaml():
    data = yaml.safe_load(CAPSULE_SCHEMA.read_text())
    assert data["name"] == "asb_capsule_v0_2"
    assert "classes" in data


def test_capsule_required_classes_present():
    data = yaml.safe_load(CAPSULE_SCHEMA.read_text())
    classes = data.get("classes", {})
    required_classes = ["SciTaskCapsule", "ArtifactProvenanceEntry"]
    for cls in required_classes:
        assert cls in classes, f"Class '{cls}' missing from asb_capsule schema"


def test_capsule_tree_root():
    data = yaml.safe_load(CAPSULE_SCHEMA.read_text())
    classes = data.get("classes", {})
    assert classes.get("SciTaskCapsule", {}).get("tree_root") is True


def test_capsule_required_slots_present():
    data = yaml.safe_load(CAPSULE_SCHEMA.read_text())
    slots = data.get("slots", {})
    required = ["capsule_task_id", "capsule_card", "capsule_created_at", "ro_crate_version"]
    for s in required:
        assert s in slots, f"Slot '{s}' missing from asb_capsule schema"


def test_capsule_every_slot_has_ontology_mapping():
    data = yaml.safe_load(CAPSULE_SCHEMA.read_text())
    slots = data.get("slots", {})
    missing = [name for name, defn in slots.items() if not _all_mappings(defn or {})]
    assert len(missing) == 0, f"Capsule slots missing ontology mappings: {missing}"


def test_capsule_every_attribute_has_ontology_mapping():
    data = yaml.safe_load(CAPSULE_SCHEMA.read_text())
    classes = data.get("classes", {})
    missing = []
    for key, defn in _slots_from_attrs(classes).items():
        if not _all_mappings(defn):
            missing.append(key)
    assert len(missing) == 0, f"Capsule attributes missing ontology mappings: {missing}"


def test_capsule_card_slot_range_is_asb_task_card():
    data = yaml.safe_load(CAPSULE_SCHEMA.read_text())
    slot = data.get("slots", {}).get("capsule_card", {})
    assert slot.get("range") == "ASBTaskCard", f"capsule_card.range must be ASBTaskCard (was {slot.get('range')!r})"


# ===========================================================================
# asb_skill_bundle.yaml
# ===========================================================================


def test_bundle_schema_is_valid_yaml():
    data = yaml.safe_load(BUNDLE_SCHEMA.read_text())
    assert data["name"] == "asb_skill_bundle_v0_2"
    assert "classes" in data


def test_bundle_required_classes_present():
    data = yaml.safe_load(BUNDLE_SCHEMA.read_text())
    classes = data.get("classes", {})
    required_classes = ["SkillBundle", "ToolRecord", "PaperReference"]
    for cls in required_classes:
        assert cls in classes, f"Class '{cls}' missing from asb_skill_bundle schema"


def test_bundle_tree_root():
    data = yaml.safe_load(BUNDLE_SCHEMA.read_text())
    classes = data.get("classes", {})
    assert classes.get("SkillBundle", {}).get("tree_root") is True


def test_bundle_required_slots_present():
    data = yaml.safe_load(BUNDLE_SCHEMA.read_text())
    slots = data.get("slots", {})
    required = [
        "slug",
        "skill_name",
        "skill_description",
        "skill_tools",
        "edam_topics",
        "edam_operation",
        "bundle_version",
    ]
    for s in required:
        assert s in slots, f"Slot '{s}' missing from asb_skill_bundle schema"


def test_bundle_every_slot_has_ontology_mapping():
    data = yaml.safe_load(BUNDLE_SCHEMA.read_text())
    slots = data.get("slots", {})
    missing = [name for name, defn in slots.items() if not _all_mappings(defn or {})]
    assert len(missing) == 0, f"Bundle slots missing ontology mappings: {missing}"


def test_bundle_every_attribute_has_ontology_mapping():
    data = yaml.safe_load(BUNDLE_SCHEMA.read_text())
    classes = data.get("classes", {})
    missing = []
    for key, defn in _slots_from_attrs(classes).items():
        if not _all_mappings(defn):
            missing.append(key)
    assert len(missing) == 0, f"Bundle attributes missing ontology mappings: {missing}"


def test_bundle_slot_importance_covers_all_tiers():
    data = yaml.safe_load(BUNDLE_SCHEMA.read_text())
    slots = data.get("slots", {})
    importance_values = set()
    for name, defn in slots.items():
        ann = (defn or {}).get("annotations", {})
        if "importance" in ann:
            importance_values.add(ann["importance"])
    assert importance_values.issuperset({"must_have", "should_have", "nice_to_have"}), (
        f"Missing importance tiers in bundle. Found: {importance_values}"
    )


def test_bundle_has_asb_skill_and_asb_tool():
    data = yaml.safe_load(BUNDLE_SCHEMA.read_text())
    classes = data.get("classes", {})
    for cls in ("ASBSkill", "ASBTool"):
        assert cls in classes, f"{cls} missing from asb_skill_bundle schema"


def test_asb_skill_required_slots():
    data = yaml.safe_load(BUNDLE_SCHEMA.read_text())
    skill_slots = list((data["classes"]["ASBSkill"].get("slots") or []))
    expected = {
        "slug",
        "skill_name",
        "description",
        "when_to_use",
        "related_tools",
        "source_task_ids",
        "source_papers",
        "merged_aliases",
        "merged_alias_records",
        "edam_operation",
        "edam_topics",
        "kb_path",
        "bundle_dir",
    }
    missing = expected - set(skill_slots)
    assert not missing, f"ASBSkill missing slots: {missing}"


def test_asb_tool_required_slots():
    data = yaml.safe_load(BUNDLE_SCHEMA.read_text())
    tool_slots = list((data["classes"]["ASBTool"].get("slots") or []))
    expected = {
        "slug",
        "tool_name",
        "canonical_url",
        "related_skills",
        "source_task_ids",
        "source_paper_doi",
        "source_paper_title",
        "evidence_spans",
        "version_used",
        "install",
        "resolution_attempts",
        "edam_operation",
        "edam_topics",
    }
    missing = expected - set(tool_slots)
    assert not missing, f"ASBTool missing slots: {missing}"

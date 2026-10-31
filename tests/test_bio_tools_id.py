"""IDEAS-G: bio_tools_id is a reserved slot on ASBTool (not populated in v1)."""

import yaml
from pathlib import Path

BUNDLE_SCHEMA = Path(__file__).parent.parent / "src/asb_schema/asb_skill_bundle.yaml"


def test_bio_tools_id_slot_declared():
    data = yaml.safe_load(BUNDLE_SCHEMA.read_text())
    slot = data["slots"]["bio_tools_id"]
    assert slot["range"] == "string"
    # Slot mapping must point at bio.tools or schema:identifier with bio.tools context.
    mappings = slot.get("close_mappings") or slot.get("exact_mappings") or []
    assert mappings, "bio_tools_id must declare at least one ontology mapping"


def test_asb_tool_includes_bio_tools_id():
    data = yaml.safe_load(BUNDLE_SCHEMA.read_text())
    slots = set(data["classes"]["ASBTool"].get("slots") or [])
    assert "bio_tools_id" in slots

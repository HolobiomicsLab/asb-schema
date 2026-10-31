"""IDEAS-F: ToolAffordance is a mixin with reserved (unpopulated) slots.

Per spec §15: 'No WoT ActionAffordance requirement in v1 — slot reserved in
LinkML, populated when ecosystem standardizes.' This test guards the slot
reservation; it does NOT assert that ASBTool uses the mixin (it doesn't, yet).
"""

import yaml
from pathlib import Path

BUNDLE_SCHEMA = Path(__file__).parent.parent / "src/asb_schema/asb_skill_bundle.yaml"


def test_tool_affordance_is_declared_mixin():
    data = yaml.safe_load(BUNDLE_SCHEMA.read_text())
    cls = data["classes"]["ToolAffordance"]
    assert cls.get("mixin") is True
    desc = (cls.get("description") or "").lower()
    assert "wot" in desc or "actionaffordance" in desc


def test_tool_affordance_reserved_slots():
    data = yaml.safe_load(BUNDLE_SCHEMA.read_text())
    cls = data["classes"]["ToolAffordance"]
    slots = set(cls.get("slots") or [])
    expected = {"input_schema", "output_schema", "precondition", "effect", "side_effect_free"}
    missing = expected - slots
    assert not missing, f"ToolAffordance missing reserved slots: {missing}"


def test_tool_affordance_slots_marked_nice_to_have():
    data = yaml.safe_load(BUNDLE_SCHEMA.read_text())
    for slot_name in ("input_schema", "output_schema", "precondition", "effect", "side_effect_free"):
        slot = data["slots"][slot_name]
        assert slot.get("annotations", {}).get("importance") == "nice_to_have", (
            f"{slot_name} should be nice_to_have (slot reservation only)"
        )

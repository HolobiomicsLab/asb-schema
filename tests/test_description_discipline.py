"""IDEAS-D / spec §5: ASBSkill.description must obey description-discipline rules.

Rules (spec §5):
  - length: 50-300 chars
  - leads with "Use when ..."
  - no banned marketing tokens
"""
import json
import subprocess
import sys
import tempfile
import textwrap
from pathlib import Path

import yaml
import pytest

SCHEMA_DIR = Path(__file__).parent.parent / "src/asb_schema"
BUNDLE_SCHEMA = SCHEMA_DIR / "asb_skill_bundle.yaml"


def _slot_description(data):
    return data["slots"]["description"]


def test_description_slot_has_length_bounds():
    data = yaml.safe_load(BUNDLE_SCHEMA.read_text())
    slot = _slot_description(data)
    assert slot.get("minimum_value") == 50
    assert slot.get("maximum_value") == 300


def test_description_slot_has_use_when_pattern():
    data = yaml.safe_load(BUNDLE_SCHEMA.read_text())
    slot = _slot_description(data)
    pattern = slot.get("pattern") or ""
    assert pattern.lower().startswith("^[uu]se when") or "use when" in pattern.lower()


def test_description_slot_required():
    data = yaml.safe_load(BUNDLE_SCHEMA.read_text())
    slot = _slot_description(data)
    assert slot.get("required") is True


def test_description_slot_lists_banned_tokens_in_annotations():
    """Banned-token check is not a native LinkML constraint, so we encode it
    as an annotation that downstream lint scripts can read."""
    data = yaml.safe_load(BUNDLE_SCHEMA.read_text())
    slot = _slot_description(data)
    banned = (slot.get("annotations") or {}).get("banned_tokens")
    assert banned is not None, "description.annotations.banned_tokens missing"
    tokens = banned if isinstance(banned, list) else str(banned).split(",")
    tokens = [t.strip().lower() for t in tokens]
    for needed in ("revolutionary", "cutting-edge", "best-in-class", "powerful", "amazing"):
        assert needed in tokens, f"banned_tokens missing {needed!r}: {tokens}"


@pytest.mark.skipif(
    subprocess.run([sys.executable, "-c", "import linkml.validators.jsonschemavalidator"]).returncode != 0,
    reason="linkml not importable in this env",
)
def test_too_short_description_is_rejected_by_linkml(tmp_path):
    """End-to-end check: a 49-char description fails LinkML validation."""
    instance = {
        "slug": "x",
        "skill_name": "x",
        "description": "Use when X.",   # 13 chars — too short
        "edam_topics": [],
        "edam_operation": "http://edamontology.org/operation_3215",
        "bundle_version": "0.2.0",
    }
    inst = tmp_path / "instance.json"
    inst.write_text(json.dumps(instance))
    result = subprocess.run(
        [
            sys.executable, "-m", "linkml.validators.jsonschemavalidator",
            "-s", str(BUNDLE_SCHEMA),
            "-C", "ASBSkill",
            str(inst),
        ],
        capture_output=True, text=True,
    )
    assert result.returncode != 0, (
        f"LinkML should have rejected the short description; output:\n{result.stdout}\n{result.stderr}"
    )

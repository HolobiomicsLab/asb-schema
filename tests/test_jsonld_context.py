"""IDEAS-H: JSON-LD @context generation targets the w3id ASB-Skill IRI."""
import json
import subprocess
import sys
from pathlib import Path

import pytest

SCHEMA_DIR = Path(__file__).parent.parent / "src/asb_schema"
CONTEXT = SCHEMA_DIR / "context.jsonld"
BUNDLE_SCHEMA = SCHEMA_DIR / "asb_skill_bundle.yaml"


def _ensure_context_built():
    """Regenerate context.jsonld from the LinkML source. Skip on tooling absence."""
    proc = subprocess.run(
        [sys.executable, "-m", "linkml.generators.jsonldcontextgen", str(BUNDLE_SCHEMA)],
        capture_output=True, text=True,
    )
    if proc.returncode != 0:
        pytest.skip(f"linkml jsonldcontextgen not runnable: {proc.stderr[:200]}")
    CONTEXT.write_text(proc.stdout)


def test_context_jsonld_present_or_generable():
    if not CONTEXT.exists():
        _ensure_context_built()
    assert CONTEXT.is_file()


def test_context_jsonld_parses_as_json():
    if not CONTEXT.exists():
        _ensure_context_built()
    data = json.loads(CONTEXT.read_text())
    assert "@context" in data


def test_context_jsonld_declares_holobiomicslab_namespace():
    if not CONTEXT.exists():
        _ensure_context_built()
    text = CONTEXT.read_text()
    assert "w3id.org/holobiomicslab/asb-" in text, (
        "context.jsonld must reference the w3id.org/holobiomicslab/asb-* namespace family"
    )


def test_context_jsonld_keys_include_core_asb_terms():
    if not CONTEXT.exists():
        _ensure_context_built()
    ctx = json.loads(CONTEXT.read_text())["@context"]
    # Sanity: at minimum these LinkML slot names appear as JSON-LD keys.
    keys = set(ctx.keys()) if isinstance(ctx, dict) else set()
    for key in ("ASBSkill", "ASBTool"):
        assert key in keys, f"@context missing term {key}"

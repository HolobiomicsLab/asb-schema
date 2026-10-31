"""IDEAS-E: MergeAuditRecord has the full audit slot set."""
import yaml
from pathlib import Path

BUNDLE_SCHEMA = Path(__file__).parent.parent / "src/asb_schema/asb_skill_bundle.yaml"


def test_merge_audit_record_full_slot_set():
    data = yaml.safe_load(BUNDLE_SCHEMA.read_text())
    cls = data["classes"]["MergeAuditRecord"]
    attrs = set((cls.get("attributes") or {}).keys())
    expected = {
        "alias", "target_slug",
        "jaccard_score", "embedding_cosine", "edam_match", "llm_judge_verdict",
        "method", "decision", "decided_at", "decided_by",
    }
    missing = expected - attrs
    assert not missing, f"MergeAuditRecord missing slots: {missing}"


def test_merge_audit_decision_is_enum():
    data = yaml.safe_load(BUNDLE_SCHEMA.read_text())
    decision = data["classes"]["MergeAuditRecord"]["attributes"]["decision"]
    # LinkML enum_range is the preferred way to bind an enum to a slot.
    assert decision.get("range") == "MergeDecisionEnum", (
        f"decision.range must be MergeDecisionEnum (got {decision.get('range')!r})"
    )
    enum = data.get("enums", {}).get("MergeDecisionEnum", {})
    pv = set((enum.get("permissible_values") or {}).keys())
    assert pv == {"auto_merge", "manual_merge", "kept_separate", "needs_review"}, (
        f"MergeDecisionEnum values wrong: {pv}"
    )

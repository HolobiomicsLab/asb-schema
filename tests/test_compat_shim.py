"""asb_schema.compat maps the legacy scitask_* and Sci* names to asb_* and ASB*.

Each lookup emits a DeprecationWarning, so code written against the former
names keeps working while it is updated.
"""

import warnings

import pytest


def test_compat_module_importable():
    import asb_schema.compat  # noqa: F401


def test_legacy_schema_name_alias_for_scitask_card():
    from asb_schema.compat import legacy_schema_name

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        out = legacy_schema_name("scitask_card")
    assert out == "asb_card"
    assert any(issubclass(rec.category, DeprecationWarning) for rec in w), (
        f"DeprecationWarning expected; got {[r.category for r in w]}"
    )


def test_legacy_schema_name_alias_for_skill_bundle():
    from asb_schema.compat import legacy_schema_name

    with warnings.catch_warnings(record=True):
        warnings.simplefilter("always")
        assert legacy_schema_name("scitask_skill_bundle") == "asb_skill_bundle"
        assert legacy_schema_name("scitask_capsule") == "asb_capsule"


@pytest.mark.parametrize(
    "legacy,new",
    [
        ("SciTaskCard", "ASBTaskCard"),
        ("SciSkill", "ASBSkill"),
        ("SciTool", "ASBTool"),
    ],
)
def test_legacy_class_name_alias(legacy, new):
    from asb_schema.compat import legacy_class_name

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        out = legacy_class_name(legacy)
    assert out == new
    assert any(issubclass(rec.category, DeprecationWarning) for rec in w)


def test_module_attribute_access_emits_warning():
    """Accessing `asb_schema.compat.SciTaskCard` returns the new name and warns."""
    import asb_schema.compat as compat

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        value = getattr(compat, "SciTaskCard")
    assert value == "ASBTaskCard"
    assert any(issubclass(rec.category, DeprecationWarning) for rec in w)


def test_unknown_legacy_class_raises_attribute_error():
    import asb_schema.compat as compat

    with pytest.raises(AttributeError):
        _ = compat.NotARealLegacyName

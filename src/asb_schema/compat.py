"""Legacy names of the ``scitask_*`` -> ``asb_*`` rename.

Maps the former schema basenames and class names to the current ones and
emits a ``DeprecationWarning`` on every lookup, so code written against the
former names keeps working while it is updated.
"""

from __future__ import annotations

import warnings
from typing import Final

__all__ = ["legacy_schema_name", "legacy_class_name"]

_SCHEMA_ALIASES: Final[dict[str, str]] = {
    "scitask": "asb",
    "scitask_card": "asb_card",
    "scitask_capsule": "asb_capsule",
    "scitask_skill_bundle": "asb_skill_bundle",
    "scitask_skill_collection": "asb_skill_collection",
    "scitask_skill_collection_registry": "asb_skill_collection_registry",
}

_CLASS_ALIASES: Final[dict[str, str]] = {
    "SciTaskCard": "ASBTaskCard",
    "SciSkill": "ASBSkill",
    "SciTool": "ASBTool",
}


def _warn(legacy: str, new: str) -> None:
    warnings.warn(
        f"{legacy!r} is deprecated; use {new!r} instead.",
        DeprecationWarning,
        stacklevel=3,
    )


def legacy_schema_name(legacy: str) -> str:
    """Map a legacy ``scitask_*`` schema basename to its ``asb_*`` replacement.

    Emits ``DeprecationWarning`` on every call.
    """
    if legacy not in _SCHEMA_ALIASES:
        raise KeyError(f"Unknown legacy schema name: {legacy!r}")
    new = _SCHEMA_ALIASES[legacy]
    _warn(legacy, new)
    return new


def legacy_class_name(legacy: str) -> str:
    """Map a legacy ``Sci*`` class name to its ``ASB*`` replacement.

    Emits ``DeprecationWarning`` on every call. The shim returns the *new
    name string*, not a class object: the package ships LinkML schemas, not
    Python classes.
    """
    if legacy not in _CLASS_ALIASES:
        raise KeyError(f"Unknown legacy class name: {legacy!r}")
    new = _CLASS_ALIASES[legacy]
    _warn(legacy, new)
    return new


def __getattr__(name: str) -> str:
    """Module-level fallback: ``from asb_schema.compat import SciTaskCard`` works."""
    if name in _CLASS_ALIASES:
        return legacy_class_name(name)
    if name in _SCHEMA_ALIASES:
        return legacy_schema_name(name)
    raise AttributeError(f"module 'asb_schema.compat' has no attribute {name!r}")

"""ASB Standard LinkML schema package (v0.4.0; replaces the legacy package in earlier releases)."""

from importlib.resources import files

__version__ = "0.4.0"

PACKAGE_DIR = files(__name__)

KNOWN_SCHEMAS = (
    "asb_card",
    "asb_capsule",
    "asb_skill_bundle",
    "asb_skill_collection",
    "asb_skill_collection_registry",
)


def schema_path(filename: str):
    """Return the Path to a bundled schema file (legacy helper)."""
    return PACKAGE_DIR / filename


def get_schema_path(name: str) -> str:
    """Return the path to a bundled LinkML schema file.

    Args:
        name: one of KNOWN_SCHEMAS
    """
    if name not in KNOWN_SCHEMAS:
        raise ValueError(f"Unknown schema {name!r}; valid: {KNOWN_SCHEMAS}")
    return str(PACKAGE_DIR.joinpath(f"{name}.yaml"))


def get_json_schema_path(name: str) -> str:
    """Return the path to a bundled JSON Schema file."""
    if name not in KNOWN_SCHEMAS:
        raise ValueError(f"Unknown schema {name!r}; valid: {KNOWN_SCHEMAS}")
    return str(PACKAGE_DIR.joinpath(f"{name}.schema.json"))


def get_jsonld_context_path() -> str:
    """Return the path to the bundled JSON-LD @context emitted from the LinkML schema."""
    return str(PACKAGE_DIR.joinpath("context.jsonld"))

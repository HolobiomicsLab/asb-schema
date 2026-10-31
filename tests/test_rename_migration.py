"""Rename invariants: package, LinkML filenames, distribution name.

The checkout directory name is not checked: a clone or a fork may live in any
directory, and the distribution name in pyproject.toml is what users install.
"""
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent


def test_python_package_is_asb_schema():
    assert (REPO_ROOT / "src" / "asb_schema" / "__init__.py").is_file()
    assert not (REPO_ROOT / "src" / "scitask_schema").exists()


def test_linkml_filenames_renamed():
    pkg = REPO_ROOT / "src" / "asb_schema"
    for name in ("asb.yaml", "asb_card.yaml", "asb_capsule.yaml", "asb_skill_bundle.yaml"):
        assert (pkg / name).is_file(), f"Missing {name}"
    for legacy in ("scitask.yaml", "scitask_card.yaml", "scitask_capsule.yaml", "scitask_skill_bundle.yaml"):
        assert not (pkg / legacy).exists(), f"Legacy file still present: {legacy}"


def test_pyproject_name_and_package_data():
    tomllib = pytest.importorskip("tomllib")  # standard library from Python 3.11
    pyproject = tomllib.loads((REPO_ROOT / "pyproject.toml").read_text())
    assert pyproject["project"]["name"] == "asb-schema"
    pkg_data = pyproject["tool"]["setuptools"]["package-data"]
    assert "asb_schema" in pkg_data
    assert "scitask_schema" not in pkg_data


def test_init_exposes_new_schema_names():
    text = (REPO_ROOT / "src" / "asb_schema" / "__init__.py").read_text()
    for needle in ("asb_card", "asb_capsule", "asb_skill_bundle",
                   "asb_skill_collection", "asb_skill_collection_registry"):
        assert needle in text, f"__init__.py missing reference to {needle}"
    assert "scitask" not in text.lower()


def test_generate_sh_iterates_asb_schemas():
    text = (REPO_ROOT / "generate.sh").read_text()
    for needle in ("asb_card", "asb_capsule", "asb_skill_bundle",
                   "asb_skill_collection", "asb_skill_collection_registry",
                   "context.jsonld"):
        assert needle in text, f"generate.sh missing {needle}"

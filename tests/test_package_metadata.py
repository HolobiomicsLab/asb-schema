"""Package metadata agrees with CITATION.cff and with the CI test matrix."""

from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture(scope="module")
def project():
    tomllib = pytest.importorskip("tomllib")  # standard library from Python 3.11
    return tomllib.loads((REPO_ROOT / "pyproject.toml").read_text())["project"]


def test_authors_match_citation(project):
    citation = yaml.safe_load((REPO_ROOT / "CITATION.cff").read_text(encoding="utf-8"))
    cited = [f"{a['given-names']} {a['family-names']}" for a in citation["authors"]]
    assert [author["name"] for author in project["authors"]] == cited


def test_keywords_match_citation(project):
    citation = yaml.safe_load((REPO_ROOT / "CITATION.cff").read_text(encoding="utf-8"))
    assert project["keywords"] == citation["keywords"]


def test_python_classifiers_match_ci_matrix(project):
    ci = REPO_ROOT / ".github" / "workflows" / "ci.yml"
    if not ci.is_file():
        pytest.skip("CI workflow not present (source distribution)")
    workflow = yaml.safe_load(ci.read_text())
    matrix = workflow["jobs"]["test"]["strategy"]["matrix"]["python-version"]
    prefix = "Programming Language :: Python :: 3."
    declared = [
        c.removeprefix("Programming Language :: Python :: ") for c in project["classifiers"] if c.startswith(prefix)
    ]
    assert declared == matrix
    assert "Programming Language :: Python :: 3" in project["classifiers"]


def test_no_license_classifier_next_to_spdx_expression(project):
    # setuptools 77 and later reject a License classifier when `license` is an SPDX expression.
    assert isinstance(project["license"], str)
    assert not [c for c in project["classifiers"] if c.startswith("License ::")]

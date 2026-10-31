"""The version guard of the publish workflow accepts only a consistent release tag.

The guard is the Python block of the step "Tag equals the package version" in
.github/workflows/publish.yml. It runs here on copies of the four files it
reads, so a mismatch can be simulated without editing the repository.
"""

import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
WORKFLOW = REPO_ROOT / ".github" / "workflows" / "publish.yml"
GUARDED_FILES = ("pyproject.toml", "src/asb_schema/__init__.py", "CITATION.cff", "CHANGELOG.md")

pytestmark = [
    pytest.mark.skipif(not WORKFLOW.is_file(), reason="publish workflow not present (source distribution)"),
    pytest.mark.skipif(sys.version_info < (3, 11), reason="the guard uses tomllib (Python 3.11 or later)"),
]


def _guard_source():
    steps = yaml.safe_load(WORKFLOW.read_text())["jobs"]["build"]["steps"]
    run = next(step["run"] for step in steps if step.get("name") == "Tag equals the package version")
    return re.search(r"<<'PY'\n(.*?)\nPY", run, re.S).group(1)


def _version():
    return re.search(r'^__version__ = "([^"]+)"', (REPO_ROOT / "src/asb_schema/__init__.py").read_text(), re.M).group(1)


def _run_guard(tmp_path, tag, edit=None):
    for name in GUARDED_FILES:
        (tmp_path / name).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(REPO_ROOT / name, tmp_path / name)
    if edit:
        edit(tmp_path)
    env = {**os.environ, "GITHUB_REF_NAME": tag}
    return subprocess.run(
        [sys.executable, "-c", _guard_source()], cwd=tmp_path, env=env, capture_output=True, text=True
    )


def test_guard_accepts_the_declared_version(tmp_path):
    result = _run_guard(tmp_path, f"v{_version()}")
    assert result.returncode == 0, result.stdout + result.stderr


def test_guard_rejects_another_tag(tmp_path):
    assert _run_guard(tmp_path, "v99.0.0").returncode != 0


def test_guard_rejects_a_citation_version_mismatch(tmp_path):
    def edit(root):
        path = root / "CITATION.cff"
        path.write_text(re.sub(r"(?m)^version: .*$", "version: 99.0.0", path.read_text()))

    result = _run_guard(tmp_path, f"v{_version()}", edit)
    assert result.returncode != 0
    assert "CITATION.cff" in result.stdout


def test_guard_rejects_a_missing_changelog_heading(tmp_path):
    def edit(root):
        path = root / "CHANGELOG.md"
        path.write_text(path.read_text().replace(f"## {_version()}", "## unreleased"))

    result = _run_guard(tmp_path, f"v{_version()}", edit)
    assert result.returncode != 0
    assert "CHANGELOG.md" in result.stdout


def test_build_job_checks_that_the_tag_is_on_main():
    steps = yaml.safe_load(WORKFLOW.read_text())["jobs"]["build"]["steps"]
    checkout = next(step for step in steps if str(step.get("uses", "")).startswith("actions/checkout@"))
    assert checkout.get("with", {}).get("fetch-depth") == 0
    assert any("git merge-base --is-ancestor" in step.get("run", "") for step in steps)

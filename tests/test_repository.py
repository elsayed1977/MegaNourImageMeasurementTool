# ═══ (2026-10-04) اختبارات ثوابت المستودع — تنجح من اليوم الأول ═══
"""Repository-invariant tests.

These tests check properties of the repository itself — the files that JOSS and
SoftwareX require, the consistency of the declared version, and the absence of
committed research data. They pass before the measurement core is ported, so the
continuous-integration badge is meaningful from the first commit.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "LICENSE",
    "README.md",
    "requirements.txt",
    "CITATION.cff",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
    "pyproject.toml",
]

DATA_SUFFIXES = {".xlsx", ".xls", ".csv", ".tif", ".tiff", ".raw"}


@pytest.mark.parametrize("name", REQUIRED_FILES)
def test_required_file_exists(name: str) -> None:
    """Every file required by the publication checklist is present."""
    assert (ROOT / name).is_file(), f"missing required file: {name}"


def test_license_is_mit() -> None:
    """The declared licence matches the licence file."""
    text = (ROOT / "LICENSE").read_text(encoding="utf-8")
    assert "MIT License" in text
    assert "Permission is hereby granted" in text


def test_version_is_consistent() -> None:
    """The version declared in pyproject.toml and CITATION.cff agree."""
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    citation = (ROOT / "CITATION.cff").read_text(encoding="utf-8")

    py_version = re.search(r'^version\s*=\s*"([^"]+)"', pyproject, re.M)
    cff_version = re.search(r'^version:\s*"?([0-9]+\.[0-9]+\.[0-9]+)"?', citation, re.M)

    assert py_version, "no version found in pyproject.toml"
    assert cff_version, "no version found in CITATION.cff"
    assert py_version.group(1) == cff_version.group(1), (
        f"version mismatch: pyproject={py_version.group(1)} "
        f"citation={cff_version.group(1)}"
    )


def test_citation_has_orcid() -> None:
    """The primary author is identified by an ORCID."""
    citation = (ROOT / "CITATION.cff").read_text(encoding="utf-8")
    assert "orcid.org/0000-0003-1839-7571" in citation


def test_requirements_are_pinned_with_ranges() -> None:
    """Every runtime dependency declares a version constraint."""
    lines = [
        ln.strip()
        for ln in (ROOT / "requirements.txt").read_text(encoding="utf-8").splitlines()
        if ln.strip() and not ln.strip().startswith("#")
    ]
    assert lines, "requirements.txt is empty"
    for ln in lines:
        assert re.search(r"[<>=~]", ln), f"dependency without a version constraint: {ln}"


def test_gitignore_blocks_research_data() -> None:
    """The ignore file excludes measurement data and specimen images."""
    text = (ROOT / ".gitignore").read_text(encoding="utf-8")
    for pattern in ("*.xlsx", "*.csv", "IMG_*.jpg", "preferences.json"):
        assert pattern in text, f".gitignore does not exclude {pattern}"


def test_no_research_data_committed() -> None:
    """No data file sits outside the sanctioned fixtures directory."""
    offenders = [
        p.relative_to(ROOT)
        for p in ROOT.rglob("*")
        if p.is_file()
        and p.suffix.lower() in DATA_SUFFIXES
        and "fixtures" not in p.parts
        and "examples" not in p.parts
        and ".git" not in p.parts
        and ".venv" not in p.parts
    ]
    assert not offenders, f"research data must not be committed: {offenders}"


def test_ci_workflow_present() -> None:
    """A continuous-integration workflow exists."""
    wf = ROOT / ".github" / "workflows" / "ci.yml"
    assert wf.is_file(), "missing .github/workflows/ci.yml"
    assert "pytest" in wf.read_text(encoding="utf-8")

# Contributing to Mega Nour Image Measurement Tool

Thank you for considering a contribution. This document describes how to propose changes.

---

## Ways to contribute

| Type | Where |
|---|---|
| 🐞 Bug report | [GitHub Issues](https://github.com/elsayed1977/MegaNourImageMeasurementTool/issues) — use the bug template |
| 💡 Feature request | GitHub Issues — describe the research workflow it serves |
| 🌍 Translation | `mnimt/i18n/ar.json` and `en.json` — add or correct strings |
| 📖 Documentation | `docs/` |
| 🔧 Code | Fork → branch → pull request |

---

## Before you open an issue

1. Check the [existing issues](https://github.com/elsayed1977/MegaNourImageMeasurementTool/issues).
2. Include:
   - operating system and Python version;
   - the exact version of the tool (`Help ▸ About`, or the value of `mnimt.__version__`);
   - the steps that reproduce the problem;
   - the log file (`%LOCALAPPDATA%\ImageMeasurementTool\logs\`), if applicable.

> ⚠️ **Never attach research data** — no measurement spreadsheets, no images of specimens
> that are not yet published, no identifiable laboratory records. A synthetic example is
> always sufficient.

---

## Development setup

```bash
git clone https://github.com/elsayed1977/MegaNourImageMeasurementTool.git
cd ImageMeasurementTool
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r requirements.txt
pip install -r requirements-dev.txt
pytest -q
ruff check .
```

---

## Pull request checklist

| ✅ | Requirement |
|---|---|
| ☐ | The change is focused on one topic. |
| ☐ | `pytest -q` passes locally. |
| ☐ | A test was added or updated for any behavioural change. |
| ☐ | `ruff check .` reports no new issues. |
| ☐ | Docstrings follow the project convention (see below). |
| ☐ | No research data, personal data or credentials are included. |

---

## Coding conventions

- **Python 3.12**, PEP 8, line length 100 (`ruff` configuration in `pyproject.toml`).
- **Type hints** on all public functions.
- **No string literals in the interface** — every user-visible string must go through
  `tr("key")` and exist in **both** `ar.json` and `en.json`. A test enforces key parity.
- **Never write to the application directory** — runtime state belongs in
  `%LOCALAPPDATA%\ImageMeasurementTool\` (or the platform equivalent).
- **Never `except: pass`.** Every caught exception is either handled or logged with context.
- **Layering is enforced** — `core` must not import from `interface`; `interface` may import
  from `core` and `services`.

### Docstring convention

Every new or modified function carries a documentation comment above it. The project uses a
dated banner so that changes are traceable:

```python
# ═══ (YYYY-MM-DD) وصف موجز بالعربية ═══
def pixels_to_mm(pixels: float, scale_px_per_mm: float) -> float:
    """Convert a pixel distance to millimetres.

    Parameters
    ----------
    pixels
        Distance measured on the image, in pixels.
    scale_px_per_mm
        Calibration factor for the image. Must be positive.

    Raises
    ------
    ValueError
        If ``scale_px_per_mm`` is not strictly positive.
    """
```

---

## Reporting a measurement-integrity concern

Because this tool produces data used in published research, correctness reports of the
following kinds are treated as **high priority**: a calibration that silently produces
self-consistent but wrong units; a measurement that is exported without its provenance
record; a plausibility range that fails to flag an impossible dimension; any path in which a
row can leave the application without a traceable image fingerprint.

Please mark such issues with the **`integrity`** label.

---

## Licence of contributions

By submitting a pull request you agree that your contribution is licensed under the
**MIT License** (see [`LICENSE`](LICENSE)).

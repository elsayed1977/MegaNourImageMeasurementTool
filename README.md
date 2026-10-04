# Mega Nour Image Measurement Tool

[![CI](https://github.com/elsayed1977/MegaNourImageMeasurementTool/actions/workflows/ci.yml/badge.svg)](https://github.com/elsayed1977/MegaNourImageMeasurementTool/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
<!-- DOI badge: add after Zenodo archiving
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXXX)
-->

**An offline, bilingual desktop tool for calibrated two-point measurement of object
dimensions in images — built for agricultural and materials research.**

Load an image → calibrate the scale → click two points per dimension → get calibrated
measurements in a traceable table. No installation, no network, no programming.

---

## Why this tool

Three capabilities distinguish it from general-purpose image-analysis platforms and
commercial measurement packages:

| | Capability | Failure mode it removes |
|---|---|---|
| **D1** | **Arabic interface with a mirrored right-to-left layout** | Language barrier for the operators who actually perform the measurements |
| **D2** | **Provenance record attached to every measurement** — image fingerprint · applied calibration · timestamp · plausibility interval · software version | A published dataset that cannot be audited after the fact |
| **D3** | **Independent physical-plausibility validation** of each derived dimension | A calibration scale that is wrong but internally consistent — and therefore invisible |

> **D3 is not hypothetical.** In a real measurement campaign, a calibration error produced a
> mean clove length of **6.75 mm** — physically impossible — and remained undetected through
> export, a *"recalibration"* step built on an algebraically circular expression, and a
> complete re-analysis, because every self-consistency check agreed with itself. Only the
> comparison against the crop's botanical range caught it. See
> [`docs/measurement-integrity.md`](docs/measurement-integrity.md).

---

## Quick start

### Option A — run the released executable (no Python needed)

1. Download `MNIMT-v1.0.0-win64.exe` from the [latest release](https://github.com/elsayed1977/MegaNourImageMeasurementTool/releases/latest).
2. Run it. No installation, no administrator rights, no network access.

### Option B — run from source

```bash
git clone https://github.com/elsayed1977/MegaNourImageMeasurementTool.git
cd MegaNourImageMeasurementTool
python -m venv .venv
# Windows:
.venv\Scripts\activate
pip install -r requirements.txt
python -m mnimt
```

---

## Usage

```
1. File ▸ Open image               → load a PNG / JPEG / TIFF / BMP
2. Tools ▸ Calibrate               → click two points on a known reference,
                                     type its true length → scale is stored for the image
3. Tools ▸ Measure Length          → click-drag two endpoints on the object
4. Tools ▸ Measure Width           → repeat; the row is completed automatically
5. File ▸ Export                   → Excel (multi-sheet) or CSV, with the provenance columns
```

**Language:** choose **العربية** or **English** from the language selector; the layout mirrors
for Arabic. The setting persists between sessions.

**Reported columns:** `Image_ID` · `Image_MD5` · `Timestamp` · `Software_Version` ·
`Scale_px_per_mm` · `Length_px` · `Length_mm` · `Width_px` · `Width_mm` · `Plausible_Range` ·
`Flagged`

---

## Documentation

| Document | Content |
|---|---|
| [`docs/user-manual-en.md`](docs/user-manual-en.md) | Full user manual (English) |
| [`docs/user-manual-ar.md`](docs/user-manual-ar.md) | دليل المستخدم الكامل (عربي) |
| [`docs/measurement-integrity.md`](docs/measurement-integrity.md) | Why provenance and plausibility checks matter — with the documented case |
| [`docs/architecture.md`](docs/architecture.md) | Layered architecture and extension points |
| [`CHANGELOG.md`](CHANGELOG.md) | Release history |

---

## Citation

If you use this software in your research, please cite it as:

```bibtex
@software{MegaNourImageMeasurementTool,
  title  = {Mega Nour Image Measurement Tool},
  author = {Ali, Elsayed Ali Elsayed},
  year   = {2026},
  version= {1.0.0},
  url    = {https://github.com/elsayed1977/MegaNourImageMeasurementTool}
}
```

GitHub also renders a **"Cite this repository"** button from [`CITATION.cff`](CITATION.cff).

---

## Contributing

Bug reports and feature requests are welcome via
[GitHub Issues](https://github.com/elsayed1977/MegaNourImageMeasurementTool/issues).
See [`CONTRIBUTING.md`](CONTRIBUTING.md) before opening a pull request.

---

## License

Released under the **MIT License** — see [`LICENSE`](LICENSE).
You may use, modify and redistribute it, including commercially, provided the copyright
notice is retained.

## Author

**Elsayed Ali Elsayed Ali** · ORCID [0000-0003-1839-7571](https://orcid.org/0000-0003-1839-7571)

Biosystem Engineering Department, Agricultural Engineering Research Institute (AEnRI),
Agricultural Research Center (ARC), Dokki, Giza 12611, Egypt

✉️ elsayedalielsayed@gmail.com · elsayed.ali@arc.sci.eg

## Acknowledgements

The tool was validated on **5,311 measured garlic cloves** collected across nine machine
treatments. The author thanks those who assisted with image acquisition and measurement.

---

<sub>Built with Python · OpenCV · Tkinter · pandas · NumPy · SciPy · Pillow</sub>

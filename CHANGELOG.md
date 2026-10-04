# Changelog

All notable changes to **Mega Nour Image Measurement Tool** are documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this
project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Planned
- `v2.0` — migration of the interface layer to PySide6/Qt for full native RTL support.

---

## [1.0.0] — 2026-09-22

First public release. Consolidates the two development lines described below into a single
maintained version.

### Added
- **Bilingual interface** (Arabic with mirrored right-to-left layout, and English) with a
  runtime language switch that requires no restart.
- **Provenance record attached to every measurement**: source-image MD5 fingerprint,
  timestamp, applied calibration, declared plausibility interval, and software version.
- **Physical-plausibility validation** of each derived dimension against a user-declared
  botanical range, with flagging and an out-of-range report.
- **Persistent logging** to file, replacing console output.
- **Excel export** with `Measurements`, `Summary` and `Provenance` sheets, alongside CSV.
- **Build and packaging pipeline** producing a single self-contained Windows executable.
- Automated test suite and continuous integration.
- User manual in Arabic and English.

### Changed
- Calibration is now recorded **per image** rather than per file.
- Detection presets, preferences, recent-file list and light/dark themes.
- Modular four-layer architecture (core · detection · interface · services).

### Fixed
- Interface construction failure caused by methods that were called but never defined.
- Batch processing could be started but never completed or cancelled.
- Undefined attributes that raised `AttributeError` during detection and zoom operations.
- Removal of the non-functional automatic-detection call chain, and of the 250+ dead
  methods left behind by an incomplete refactor.

### Removed
- Superseded experimental code paths and duplicated helper implementations.

---

## [0.243] — 2025-10-20

Small, manually validated build. The version distributed as a compiled executable and used
for the measurement campaign referenced in the accompanying research.

### Added
- Manual two-point length and width measurement on a calibrated canvas.
- Calibration against a known reference distance.
- CSV export with measurement coordinates.

### Known issues
- Automatic detection non-functional: the entry point calls a method
  (`ParticleDetector.detect_particle`) that is never defined, and the trigger condition is
  unreachable.
- `MeasurementManager.clear_measurements` references attributes that do not exist.
- No Excel export, no logging, no provenance information, no physical-range validation.
- Single-language (English) interface.

---

## [0.26] — 2025-10-19

Full-featured development line. **Never released** — an incomplete refactor left it
non-functional in several paths (missing dialogue methods, undefined attributes, broken
test fixtures). Retained as the architectural basis for `v1.0`.

### Added
- Preferences, detection presets, help system, tooltips, recent files, light/dark themes.
- Batch processing, performance monitor, memory manager, error handler.
- Excel export with a summary sheet.
- Automated test classes (4) — fixture methods were incomplete.

---

## [0.25] — 2025-10-18

Complete detection pipeline (`ParticleDetector`, 40 methods) including ROI extraction,
contour validation, fallback strategies and shape analysis. Retained as the source for the
automatic-detection logic restored in `v1.0`.

---

## [0.0] — 2025-10-17

Initial prototype: image loading and manual two-point measurement.

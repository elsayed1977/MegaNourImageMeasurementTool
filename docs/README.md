# Documentation index

| Document | Audience | Language | Status |
|---|---|---|---|
| [`measurement-integrity.md`](measurement-integrity.md) | Researchers using the data; reviewers | English | ✅ written |
| [`architecture.md`](architecture.md) | Developers and maintainers | English | ⬜ to write with the `v1.0` port |
| `user-manual-en.md` | End users | English | ⬜ to write in Phase 3 |
| `user-manual-ar.md` | المستخدمون العرب | عربي | ⬜ to write in Phase 3 |
| `detection.md` | Users of the assisted-detection feature | English | ⬜ to write with the port |
| `export-format.md` | Anyone consuming the exported tables | English | ⬜ to write with the port |

---

## Export format (preliminary specification)

Every exported row contains the following columns. The provenance group is mandatory: a row
that cannot be traced to an image and a calibration must not leave the application.

### Measurement group
| Column | Type | Description |
|---|---|---|
| `ID` | int | Sequential identifier within the session |
| `Length_px` | float | Distance between the two clicked endpoints, in pixels |
| `Length_mm` | float | `Length_px` divided by `Scale_px_per_mm` |
| `Width_px` | float | Second dimension, in pixels |
| `Width_mm` | float | `Width_px` divided by `Scale_px_per_mm` |

### Provenance group (mandatory)
| Column | Type | Description |
|---|---|---|
| `Image_ID` | str | File name of the source image |
| `Image_MD5` | str | MD5 fingerprint of the source image file |
| `Timestamp` | str | ISO-8601 local time at which the measurement was recorded |
| `Software_Version` | str | Version identifier of the tool that produced the row |
| `Scale_px_per_mm` | float | Calibration in force for this image |

### Validation group
| Column | Type | Description |
|---|---|---|
| `Plausible_Range` | str | Declared interval, e.g. `25.0-45.0` |
| `Flagged` | bool | `True` if any dimension falls outside `Plausible_Range` |
| `Flag_Reason` | str | Which dimension and by how much, when `Flagged` is `True` |

### Cross-reference to the earlier export format

The earlier tool exported `ID · L_start_X · L_start_Y · L_End_X · L_End_Y · Length_px ·
Length_mm · W_start_X · W_start_Y · W_End_X · W_End_Y · Width_px · Width_mm · Auto_Area_px ·
Auto_Area_mm · Major_Axis_px · Minor_Axis_px · Detection_Confidence · Detection_Method`.
The provenance and validation groups are new; the coordinates are dropped, since they are
recoverable from the annotated image that is saved alongside the data.

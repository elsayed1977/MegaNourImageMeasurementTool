# Measurement integrity: why provenance and plausibility checks matter

This document records a **real calibration failure** from a measurement campaign carried out
with an earlier version of this tool. It is included in the repository because it is the
direct motivation for two of the tool's design decisions, and because the failure mode it
describes is easy to reproduce and hard to notice.

---

## 1. What happened

Garlic cloves were measured in the two-dimensional imaging stage of a grading machine. The
measurement software reported, for each clove, a pixel distance and a millimetre value
obtained by dividing that distance by a calibration scale.

A calibration error was made during the campaign. The consequence was not an obviously
broken dataset: it was a dataset in which **68 % of cloves were shorter than 20 mm**, while
every internal consistency check agreed with itself.

| | Corrected dataset (used for analysis) | Earlier export (superseded) |
|---|---|---|
| Cloves | 5,311 | 5,133 |
| Scale column | **per image** (`scale_px_per_mm`, ≈5.58) | **one constant per file** (`Scale px/mm`, 5.67) |
| Median length (mm) | **27.33** | **13.23** |
| Median width (mm) | **12.11** | **6.26** |
| Cloves shorter than 20 mm | 12.2 % | **68.0 %** |

In one treatment the mean measured length was **6.75 mm** in the affected export against
**22.34 mm** in the corrected dataset. The botanical length of a clove of this cultivar is
**25–45 mm**.

The defect was invisible in the row counts (5,133 against 5,311 — a difference of 3.3 %) and
invisible in any single statistic computed from the millimetre values, because those values
are internally consistent with the scale that produced them.

---

## 2. Why the recalibration step did not fix it

The correction was attempted with a preprocessing script that recomputed the scale from the
exported values:

```
scale = mean( Length_px / Length_mm ,  Width_px / Width_mm )
```

This expression is the natural way to "recover" a calibration, and it does not do what it
appears to do. The measurement software originally computed

```
Length_mm = Length_px / scale
```

so the expression above returns **exactly the scale the software had used**. It is
algebraically circular and is therefore **incapable of detecting a systematic calibration
error**. It reproduces the erroneous value and presents it as a correction: the recalibrated
column agrees perfectly with the column it replaced, whether or not the original calibration
was correct.

> **Lesson.** A self-consistency check is not a calibration check. If both quantities being
> compared were produced by the same instrument using the same scale, their ratio will always
> agree — including when the scale is wrong.

---

## 3. What actually detected the error

A **length histogram**, in which a mean clove length of 7 mm was immediately recognisable as
impossible. That is the entire detection procedure: no reference object, no instrument, no
statistical model — only a comparison of the derived dimension against the botanical range of
the crop.

The single operation in the whole workflow that carried **independent** information was that
comparison.

---

## 4. What the tool does about it

| Decision | Implementation |
|---|---|
| **Physical-plausibility validation** | Every derived dimension is checked against a user-declared range for the object being measured. Out-of-range measurements are flagged in the table, written to the log, and summarised in an "out-of-range" report. |
| **Calibration recorded per image** | The scale is stored with each image, not once per file. A file that mixes scales is visible rather than silent. |
| **Provenance per measurement** | Each exported row carries the image fingerprint (MD5), a timestamp, the applied scale, the declared plausibility interval, and the software version. |
| **Scale and measurement kept separate** | Pixel distances and calibrated distances are exported in separate columns, so a change of scale never destroys the original observation. |
| **No silent data loss** | Export counts are asserted against the number of records held in memory. |

---

## 5. Checklist for anyone measuring from images

1. **Declare a plausible range** for every dimension *before* measuring, from the literature
   or from a hand measurement with a calliper.
2. **Assert the range on every row** of the exported table. One line of code.
3. **Record the scale per image**, not per file or per session.
4. **Keep the pixel values** in the export alongside the calibrated ones.
5. **Archive the image fingerprint and the software version** with the data.
6. **Reproduce a sample by hand** with an independent instrument, and compare.
7. **Do not accept a self-consistency check as a calibration check.** The two can never
   disagree, which is exactly why the second one is useless.

---

## 6. Reference

The same case study is reported in the accompanying technical note on measurement integrity
in image-based clove grading, together with a second, independent pitfall: a one-line
construction of a confusion matrix that silently discards 23.2 % of the evaluated units and
inflates the reported grading accuracy by 30 %.

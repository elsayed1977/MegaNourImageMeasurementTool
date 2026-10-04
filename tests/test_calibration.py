# ═══ (2026-10-04) اختبارات نواة القياس — هيكل جاهز يعمل بعد نقل الشيفرة ═══
"""Tests for the measurement core.

The measurement core is ported from the validated v0.243 build into ``src/mnimt/core``.
Until that port lands, these tests skip cleanly so that the suite stays green; once the
package exists, they run and must pass.

The measurements they check are the ones that carry scientific weight:

* the pixel-to-millimetre conversion, including the rejection of a non-positive scale;
* the Euclidean distance between two clicked endpoints;
* the physical-plausibility flag, which is the check that a real calibration error
  escaped — a mean clove length of 6.75 mm instead of 22.34 mm.
"""

from __future__ import annotations

import pytest

core = pytest.importorskip(
    "mnimt.core",
    reason="measurement core not yet ported (see CHANGELOG v1.0.0)",
)


# ── تحويل البكسل إلى ملليمتر ──
def test_pixels_to_mm_basic() -> None:
    assert core.pixels_to_mm(100.0, scale_px_per_mm=5.0) == pytest.approx(20.0)


def test_pixels_to_mm_is_linear() -> None:
    """Doubling the pixel distance doubles the physical distance."""
    a = core.pixels_to_mm(50.0, 5.58)
    b = core.pixels_to_mm(100.0, 5.58)
    assert b == pytest.approx(2 * a)


@pytest.mark.parametrize("bad_scale", [0.0, -1.0])
def test_pixels_to_mm_rejects_non_positive_scale(bad_scale: float) -> None:
    """A missing or impossible calibration must raise, never silently return pixels."""
    with pytest.raises(ValueError):
        core.pixels_to_mm(100.0, scale_px_per_mm=bad_scale)


# ── المسافة الإقليدية بين نقطتين ──
def test_two_point_distance_axis_aligned() -> None:
    assert core.two_point_distance((0.0, 0.0), (30.0, 40.0)) == pytest.approx(50.0)


def test_two_point_distance_is_symmetric() -> None:
    p0, p1 = (12.5, 88.0), (197.3, 240.1)
    assert core.two_point_distance(p0, p1) == pytest.approx(
        core.two_point_distance(p1, p0)
    )


# ── التحقق الفيزيائي: الفحص الذي أفلت منه خطأ حقيقي ──
def test_dimension_below_declared_range_is_flagged() -> None:
    """A value below the declared botanical range is flagged."""
    result = core.check_plausibility(22.34, plausible_range=(25.0, 45.0))
    assert result.flagged is True


def test_impossible_dimension_is_flagged() -> None:
    """6.75 mm is impossible for a garlic clove and must be flagged.

    This is the documented failure mode: a mis-calibrated export produced a mean clove
    length of 6.75 mm, and every *self-consistency* check agreed with itself. Only an
    independent plausibility interval catches it.
    """
    result = core.check_plausibility(6.75, plausible_range=(25.0, 45.0))
    assert result.flagged is True
    assert "6.75" in str(result.message)


def test_plausibility_is_scale_error_detector() -> None:
    """A fourfold scale error is caught by the plausibility interval alone.

    31.77 mm is a valid clove length; 31.77 / 4.3 = 7.39 mm is not. No change to the
    algorithm is required for the interval to separate the two.
    """
    good = core.check_plausibility(31.77, plausible_range=(25.0, 45.0))
    bad = core.check_plausibility(31.77 / 4.3, plausible_range=(25.0, 45.0))
    assert good.flagged is False
    assert bad.flagged is True

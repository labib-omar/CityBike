"""
Unit tests for the numerical module.

Covers:
    - trip_duration_stats (partially implemented — mean, median, std)
"""

import pytest
import numpy as np

from numerical import trip_duration_stats


# ---------------------------------------------------------------------------
# trip_duration_stats
# ---------------------------------------------------------------------------

class TestTripDurationStats:

    def test_basic_stats(self) -> None:
        durations = np.array([10.0, 20.0, 30.0, 40.0, 50.0])
        stats = trip_duration_stats(durations)
        assert stats["mean"] == pytest.approx(30.0)
        assert stats["median"] == pytest.approx(30.0)

    def test_std(self) -> None:
        durations = np.array([10.0, 20.0, 30.0, 40.0, 50.0])
        stats = trip_duration_stats(durations)
        assert stats["std"] == pytest.approx(np.std(durations))

    def test_single_value(self) -> None:
        durations = np.array([42.0])
        stats = trip_duration_stats(durations)
        assert stats["mean"] == pytest.approx(42.0)
        assert stats["median"] == pytest.approx(42.0)
        assert stats["std"] == pytest.approx(0.0)

    def test_returns_expected_keys(self) -> None:
        durations = np.array([1.0, 2.0, 3.0])
        stats = trip_duration_stats(durations)
        assert "mean" in stats
        assert "median" in stats
        assert "std" in stats

    def test_values_are_floats(self) -> None:
        durations = np.array([5.0, 15.0, 25.0])
        stats = trip_duration_stats(durations)
        for val in stats.values():
            assert isinstance(val, float)

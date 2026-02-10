"""
Unit tests for utility functions (utils.py).

Covers all validation, parsing, and formatting helpers.
"""

import pytest
from datetime import datetime

from utils import (
    validate_positive,
    validate_non_negative,
    validate_email,
    validate_in,
    parse_datetime,
    parse_date,
    fmt_duration,
    fmt_currency,
)


# ---------------------------------------------------------------------------
# validate_positive
# ---------------------------------------------------------------------------

class TestValidatePositive:

    def test_positive_value(self) -> None:
        assert validate_positive(5.0) == 5.0

    def test_zero_raises(self) -> None:
        with pytest.raises(ValueError, match="must be positive"):
            validate_positive(0)

    def test_negative_raises(self) -> None:
        with pytest.raises(ValueError, match="must be positive"):
            validate_positive(-1)

    def test_custom_name_in_error(self) -> None:
        with pytest.raises(ValueError, match="price"):
            validate_positive(-10, name="price")


# ---------------------------------------------------------------------------
# validate_non_negative
# ---------------------------------------------------------------------------

class TestValidateNonNegative:

    def test_positive_value(self) -> None:
        assert validate_non_negative(3.5) == 3.5

    def test_zero_allowed(self) -> None:
        assert validate_non_negative(0) == 0

    def test_negative_raises(self) -> None:
        with pytest.raises(ValueError, match="must be non-negative"):
            validate_non_negative(-0.01)


# ---------------------------------------------------------------------------
# validate_email
# ---------------------------------------------------------------------------

class TestValidateEmail:

    def test_valid_email(self) -> None:
        assert validate_email("user@example.com") == "user@example.com"

    def test_missing_at_sign(self) -> None:
        with pytest.raises(ValueError, match="Invalid email"):
            validate_email("userexample.com")

    def test_empty_string(self) -> None:
        with pytest.raises(ValueError, match="Invalid email"):
            validate_email("")

    def test_non_string_raises(self) -> None:
        with pytest.raises(ValueError, match="Invalid email"):
            validate_email(123)  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# validate_in
# ---------------------------------------------------------------------------

class TestValidateIn:

    def test_value_in_set(self) -> None:
        assert validate_in("a", {"a", "b", "c"}) == "a"

    def test_value_not_in_set(self) -> None:
        with pytest.raises(ValueError, match="must be one of"):
            validate_in("x", {"a", "b", "c"}, name="letter")


# ---------------------------------------------------------------------------
# parse_datetime / parse_date
# ---------------------------------------------------------------------------

class TestParsing:

    def test_parse_datetime(self) -> None:
        dt = parse_datetime("2024-06-15 08:30:00")
        assert dt == datetime(2024, 6, 15, 8, 30, 0)

    def test_parse_datetime_invalid(self) -> None:
        with pytest.raises(ValueError):
            parse_datetime("15/06/2024 08:30")

    def test_parse_date(self) -> None:
        dt = parse_date("2024-06-15")
        assert dt == datetime(2024, 6, 15, 0, 0, 0)

    def test_parse_date_invalid(self) -> None:
        with pytest.raises(ValueError):
            parse_date("June 15, 2024")


# ---------------------------------------------------------------------------
# fmt_duration
# ---------------------------------------------------------------------------

class TestFmtDuration:

    def test_exact_hours(self) -> None:
        assert fmt_duration(120) == "2h 0m"

    def test_mixed(self) -> None:
        assert fmt_duration(95.5) == "1h 35m"

    def test_less_than_hour(self) -> None:
        assert fmt_duration(45) == "0h 45m"

    def test_zero(self) -> None:
        assert fmt_duration(0) == "0h 0m"


# ---------------------------------------------------------------------------
# fmt_currency
# ---------------------------------------------------------------------------

class TestFmtCurrency:

    def test_normal_amount(self) -> None:
        assert fmt_currency(9.5) == "€9.50"

    def test_zero(self) -> None:
        assert fmt_currency(0) == "€0.00"

    def test_large_amount(self) -> None:
        assert fmt_currency(1234.567) == "€1234.57"

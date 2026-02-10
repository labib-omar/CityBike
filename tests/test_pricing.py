"""
Unit tests for the pricing module.

Covers:
    - CasualPricing (fully implemented)
    - PricingStrategy cannot be instantiated directly
"""

import pytest

from pricing import PricingStrategy, CasualPricing


# ---------------------------------------------------------------------------
# PricingStrategy (abstract)
# ---------------------------------------------------------------------------

class TestPricingStrategy:

    def test_cannot_instantiate(self) -> None:
        with pytest.raises(TypeError):
            PricingStrategy()  # type: ignore[abstract]


# ---------------------------------------------------------------------------
# CasualPricing
# ---------------------------------------------------------------------------

class TestCasualPricing:

    def setup_method(self) -> None:
        self.pricing = CasualPricing()

    def test_zero_trip(self) -> None:
        cost = self.pricing.calculate_cost(0, 0)
        assert cost == pytest.approx(1.00)  # unlock fee only

    def test_known_trip(self) -> None:
        # 20 min, 5 km → 1.00 + 20*0.15 + 5*0.10 = 1.00 + 3.00 + 0.50 = 4.50
        cost = self.pricing.calculate_cost(20, 5)
        assert cost == pytest.approx(4.50)

    def test_long_trip(self) -> None:
        # 60 min, 12 km → 1.00 + 9.00 + 1.20 = 11.20
        cost = self.pricing.calculate_cost(60, 12)
        assert cost == pytest.approx(11.20)

    def test_cost_increases_with_duration(self) -> None:
        short = self.pricing.calculate_cost(10, 5)
        long = self.pricing.calculate_cost(30, 5)
        assert long > short

    def test_cost_increases_with_distance(self) -> None:
        near = self.pricing.calculate_cost(10, 1)
        far = self.pricing.calculate_cost(10, 10)
        assert far > near

    def test_is_pricing_strategy(self) -> None:
        assert isinstance(self.pricing, PricingStrategy)

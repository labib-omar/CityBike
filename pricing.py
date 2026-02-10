"""
Pricing strategies for trip cost calculation (Strategy Pattern).

Provides a common interface `PricingStrategy` and concrete implementations.

Students should:
    - Complete MemberPricing
    - Implement PeakHourPricing
    - Optionally add more strategies
"""

from abc import ABC, abstractmethod


# ---------------------------------------------------------------------------
# Strategy interface
# ---------------------------------------------------------------------------

class PricingStrategy(ABC):
    """Abstract pricing strategy — computes the cost of a trip."""

    @abstractmethod
    def calculate_cost(
        self, duration_minutes: float, distance_km: float
    ) -> float:
        """Return the trip cost in euros.

        Args:
            duration_minutes: Length of the trip in minutes.
            distance_km: Distance traveled in kilometers.

        Returns:
            Trip cost as a float.
        """
        ...


# ---------------------------------------------------------------------------
# Concrete strategies
# ---------------------------------------------------------------------------

class CasualPricing(PricingStrategy):
    """Pricing for casual (non-member) users.

    Rate:
        - €1.00 unlock fee
        - €0.15 per minute
        - €0.10 per km
    """

    UNLOCK_FEE = 1.00
    PER_MINUTE = 0.15
    PER_KM = 0.10

    def calculate_cost(
        self, duration_minutes: float, distance_km: float
    ) -> float:
        return (
            self.UNLOCK_FEE
            + self.PER_MINUTE * duration_minutes
            + self.PER_KM * distance_km
        )


class MemberPricing(PricingStrategy):
    """Pricing for member users — discounted rates.

    TODO:
        - No unlock fee
        - €0.08 per minute
        - €0.05 per km
        - Implement calculate_cost
    """

    PER_MINUTE = 0.08
    PER_KM = 0.05

    def calculate_cost(
        self, duration_minutes: float, distance_km: float
    ) -> float:
        # TODO: implement the member pricing formula
        raise NotImplementedError("MemberPricing.calculate_cost")


class PeakHourPricing(PricingStrategy):
    """Pricing during peak hours (surcharge on top of casual rates).

    TODO:
        - Apply a 1.5x multiplier to the CasualPricing cost
        - Implement calculate_cost
    """

    MULTIPLIER = 1.5

    def calculate_cost(
        self, duration_minutes: float, distance_km: float
    ) -> float:
        # TODO: implement peak-hour pricing
        raise NotImplementedError("PeakHourPricing.calculate_cost")

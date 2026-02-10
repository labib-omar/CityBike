"""
Unit tests for the factory module.

Covers:
    - create_bike (fully implemented)
"""

import pytest

from factories import create_bike
from models import ClassicBike, ElectricBike, Bike


# ---------------------------------------------------------------------------
# create_bike
# ---------------------------------------------------------------------------

class TestCreateBike:

    def test_creates_classic_bike(self) -> None:
        bike = create_bike({"bike_id": "BK001", "bike_type": "classic"})
        assert isinstance(bike, ClassicBike)
        assert bike.id == "BK001"
        assert bike.bike_type == "classic"

    def test_creates_electric_bike(self) -> None:
        bike = create_bike({"bike_id": "BK002", "bike_type": "electric"})
        assert isinstance(bike, ElectricBike)
        assert bike.id == "BK002"
        assert bike.bike_type == "electric"

    def test_classic_default_gears(self) -> None:
        bike = create_bike({"bike_id": "BK003", "bike_type": "classic"})
        assert isinstance(bike, ClassicBike)
        assert bike.gear_count == 7

    def test_classic_custom_gears(self) -> None:
        bike = create_bike({
            "bike_id": "BK004",
            "bike_type": "classic",
            "gear_count": "21",
        })
        assert isinstance(bike, ClassicBike)
        assert bike.gear_count == 21

    def test_case_insensitive_type(self) -> None:
        bike = create_bike({"bike_id": "BK005", "bike_type": "Classic"})
        assert isinstance(bike, ClassicBike)

    def test_unknown_type_raises(self) -> None:
        with pytest.raises(ValueError, match="Unknown bike_type"):
            create_bike({"bike_id": "BK006", "bike_type": "scooter"})

    def test_missing_type_raises(self) -> None:
        with pytest.raises(ValueError, match="Unknown bike_type"):
            create_bike({"bike_id": "BK007"})

    def test_result_is_bike_instance(self) -> None:
        bike = create_bike({"bike_id": "BK008", "bike_type": "electric"})
        assert isinstance(bike, Bike)

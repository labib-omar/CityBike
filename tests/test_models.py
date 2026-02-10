"""
Unit tests for OOP models.

Covers:
    - Entity (via ClassicBike since Entity is abstract)
    - Bike base class validation
    - ClassicBike creation, properties, validation, __str__, __repr__
"""

import pytest
from datetime import datetime

from models import (
    Bike,
    ClassicBike,
    ElectricBike,
    Entity,
)


# ---------------------------------------------------------------------------
# Entity (tested through concrete subclass ClassicBike)
# ---------------------------------------------------------------------------

class TestEntity:
    """Tests for the abstract Entity base class."""

    def test_entity_cannot_be_instantiated(self) -> None:
        with pytest.raises(TypeError):
            Entity(id="E001")  # type: ignore[abstract]

    def test_entity_rejects_empty_id(self) -> None:
        with pytest.raises(ValueError):
            ClassicBike(bike_id="", gear_count=5)

    def test_entity_rejects_non_string_id(self) -> None:
        with pytest.raises((ValueError, TypeError)):
            ClassicBike(bike_id=123, gear_count=5)  # type: ignore[arg-type]

    def test_entity_id_property(self) -> None:
        bike = ClassicBike(bike_id="BK001")
        assert bike.id == "BK001"

    def test_entity_created_at_default(self) -> None:
        bike = ClassicBike(bike_id="BK001")
        assert isinstance(bike.created_at, datetime)

    def test_entity_created_at_custom(self) -> None:
        ts = datetime(2024, 6, 15, 12, 0, 0)
        bike = ClassicBike.__new__(ClassicBike)
        Entity.__init__(bike, id="BK001", created_at=ts)
        assert bike.created_at == ts


# ---------------------------------------------------------------------------
# Bike
# ---------------------------------------------------------------------------

class TestBike:
    """Tests for the Bike base class."""

    def test_bike_rejects_invalid_type(self) -> None:
        with pytest.raises(ValueError, match="Invalid bike_type"):
            Bike(bike_id="BK001", bike_type="scooter")

    def test_bike_rejects_invalid_status(self) -> None:
        with pytest.raises(ValueError, match="Invalid status"):
            Bike(bike_id="BK001", bike_type="classic", status="broken")

    def test_bike_default_status(self) -> None:
        bike = Bike(bike_id="BK001", bike_type="classic")
        assert bike.status == "available"

    def test_bike_type_property(self) -> None:
        bike = Bike(bike_id="BK001", bike_type="electric")
        assert bike.bike_type == "electric"

    def test_bike_status_setter_valid(self) -> None:
        bike = Bike(bike_id="BK001", bike_type="classic")
        bike.status = "in_use"
        assert bike.status == "in_use"
        bike.status = "maintenance"
        assert bike.status == "maintenance"

    def test_bike_status_setter_invalid(self) -> None:
        bike = Bike(bike_id="BK001", bike_type="classic")
        with pytest.raises(ValueError, match="Invalid status"):
            bike.status = "destroyed"

    def test_bike_str(self) -> None:
        bike = Bike(bike_id="BK001", bike_type="classic", status="in_use")
        assert str(bike) == "Bike(BK001, classic, in_use)"

    def test_bike_repr(self) -> None:
        bike = Bike(bike_id="BK001", bike_type="classic", status="available")
        r = repr(bike)
        assert "BK001" in r
        assert "classic" in r
        assert "available" in r


# ---------------------------------------------------------------------------
# ClassicBike
# ---------------------------------------------------------------------------

class TestClassicBike:
    """Tests for the ClassicBike subclass."""

    def test_creation_defaults(self) -> None:
        bike = ClassicBike(bike_id="BK010")
        assert bike.id == "BK010"
        assert bike.bike_type == "classic"
        assert bike.gear_count == 7
        assert bike.status == "available"

    def test_creation_custom_gears(self) -> None:
        bike = ClassicBike(bike_id="BK011", gear_count=21)
        assert bike.gear_count == 21

    def test_rejects_zero_gears(self) -> None:
        with pytest.raises(ValueError):
            ClassicBike(bike_id="BK012", gear_count=0)

    def test_rejects_negative_gears(self) -> None:
        with pytest.raises(ValueError):
            ClassicBike(bike_id="BK013", gear_count=-3)

    def test_is_instance_of_bike(self) -> None:
        bike = ClassicBike(bike_id="BK014")
        assert isinstance(bike, Bike)
        assert isinstance(bike, Entity)

    def test_str(self) -> None:
        bike = ClassicBike(bike_id="BK015", gear_count=7)
        assert str(bike) == "ClassicBike(BK015, gears=7)"

    def test_repr(self) -> None:
        bike = ClassicBike(bike_id="BK015", gear_count=7, status="available")
        r = repr(bike)
        assert "BK015" in r
        assert "gear_count=7" in r
        assert "available" in r

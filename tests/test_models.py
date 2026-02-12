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
    Entity,
    Bike,
    ClassicBike,
    ElectricBike,
    User,
    Trip,
    Station,
    MaintenanceRecord,
)



def create_trip(data: dict, user_map: dict, bike_map: dict, station_map: dict) -> Trip:
    """Create a Trip object from a data dictionary.

    Args:
        data: Dict with trip info (trip_id, user_id, bike_id, start_station_id, end_station_id, start_time, end_time, distance_km)
        user_map: dict mapping user_id -> User object
        bike_map: dict mapping bike_id -> Bike object
        station_map: dict mapping station_id -> Station object

    Returns:
        Trip instance.

    Raises:
        ValueError if IDs are not found in the maps or invalid data.
    """
    # Lookup associated objects
    user = user_map.get(data["user_id"])
    bike = bike_map.get(data["bike_id"])
    start_station = station_map.get(data["start_station_id"])
    end_station = station_map.get(data["end_station_id"])

    if user is None:
        raise ValueError(f"User ID {data['user_id']} not found")
    if bike is None:
        raise ValueError(f"Bike ID {data['bike_id']} not found")
    if start_station is None:
        raise ValueError(f"Start station ID {data['start_station_id']} not found")
    if end_station is None:
        raise ValueError(f"End station ID {data['end_station_id']} not found")

    # Parse datetimes
    start_time = datetime.fromisoformat(data["start_time"])
    end_time = datetime.fromisoformat(data["end_time"])

    # Distance validation
    distance_km = float(data.get("distance_km", 0.0))
    if distance_km < 0:
        raise ValueError("distance_km cannot be negative")

    # Ensure end_time >= start_time
    if end_time < start_time:
        raise ValueError("end_time cannot be before start_time")

    return Trip(
        trip_id=data["trip_id"],
        user=user,
        bike=bike,
        start_station=start_station,
        end_station=end_station,
        start_time=start_time,
        end_time=end_time,
        distance_km=distance_km,
    )


def create_maintenance_record(data: dict, bike_map: dict) -> MaintenanceRecord:
    """Create a MaintenanceRecord object from a data dictionary.

    Args:
        data: Dict with maintenance info (record_id, bike_id, date, maintenance_type, cost, description)
        bike_map: dict mapping bike_id -> Bike object

    Returns:
        MaintenanceRecord instance.

    Raises:
        ValueError if bike_id is missing or maintenance_type/cost invalid.
    """
    bike = bike_map.get(data["bike_id"])
    if bike is None:
        raise ValueError(f"Bike ID {data['bike_id']} not found")

    # Parse date
    date = datetime.fromisoformat(data["date"])

    # Cost validation
    cost = float(data.get("cost", 0.0))
    if cost < 0:
        raise ValueError("Maintenance cost cannot be negative")

    maintenance_type = data["maintenance_type"]
    description = data.get("description", "")

    return MaintenanceRecord(
        record_id=data["record_id"],
        bike=bike,
        date=date,
        maintenance_type=maintenance_type,
        cost=cost,
        description=description,
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

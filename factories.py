"""
Factory Pattern — create domain objects from raw CSV-row dictionaries.

The factory functions hide which concrete subclass is instantiated,
so the rest of the code never needs to import ClassicBike / ElectricBike etc.

Students should:
    - Complete create_user()
    - Optionally add create_trip() and create_maintenance_record()
"""

from models import (
    Bike,
    ClassicBike,
    ElectricBike,
    User,
    CasualUser,
    MemberUser,
    Trip,
    Station,
    MaintenanceRecord,
)


def create_bike(data: dict) -> Bike:
    """Create a Bike (ClassicBike or ElectricBike) from a data dictionary.

    Args:
        data: A dict with at least 'bike_id' and 'bike_type'.

    Returns:
        A ClassicBike or ElectricBike instance.

    Raises:
        ValueError: If bike_type is unknown.

    Example:
        >>> bike = create_bike({"bike_id": "BK200", "bike_type": "electric"})
        >>> isinstance(bike, ElectricBike)
        True
    """
    bike_type = data.get("bike_type", "").lower()

    if bike_type == "classic":
        return ClassicBike(
            bike_id=data["bike_id"],
            gear_count=int(data.get("gear_count", 7)),
        )
    elif bike_type == "electric":
        return ElectricBike(
            bike_id=data["bike_id"],
            battery_level=float(data.get("battery_level", 100.0)),
            max_range_km=float(data.get("max_range_km", 50.0)),
        )
    else:
        raise ValueError(f"Unknown bike_type: {bike_type!r}")


from datetime import datetime

def create_user(data: dict) -> User:
    """Create a User (CasualUser or MemberUser) from a data dictionary.

    Args:
        data: A dict with at least 'user_id', 'name', 'email', 'user_type'.

    Returns:
        A CasualUser or MemberUser instance.

    Raises:
        ValueError: If user_type is unknown or required fields are missing.
    """
    user_type = data.get("user_type", "").lower()

    if user_type == "casual":
        return CasualUser(
            user_id=data["user_id"],
            name=data["name"],
            email=data["email"],
            day_pass_count=int(data.get("day_pass_count", 0)),
        )

    elif user_type == "member":
        # Parse membership dates; assume ISO format if provided
        start_str = data.get("membership_start")
        end_str = data.get("membership_end")

        membership_start = (
            datetime.fromisoformat(start_str) if start_str else datetime.now()
        )
        membership_end = (
            datetime.fromisoformat(end_str) if end_str else membership_start
        )

        return MemberUser(
            user_id=data["user_id"],
            name=data["name"],
            email=data["email"],
            membership_start=membership_start,
            membership_end=membership_end,
            tier=data.get("tier", "basic").lower(),
        )

    else:
        raise ValueError(f"Unknown user_type: {user_type!r}")

def create_trip(data: dict, users: dict, bikes: dict, stations: dict) -> Trip:
    """
    Create a Trip from a data dictionary.

    Args:
        data: dict with trip info, e.g. 'trip_id', 'user_id', 'bike_id', 'start_station_id', ...
        users: dict mapping user_id -> User instance
        bikes: dict mapping bike_id -> Bike instance
        stations: dict mapping station_id -> Station instance

    Returns:
        Trip instance
    """
    trip_id = data["trip_id"]

    # Lookup objects by ID
    user = users[data["user_id"]]
    bike = bikes[data["bike_id"]]
    start_station = stations[data["start_station_id"]]
    end_station = stations[data["end_station_id"]]

    # Parse datetime
    start_time = datetime.fromisoformat(data["start_time"])
    end_time = datetime.fromisoformat(data["end_time"])

    # Distance
    distance_km = float(data.get("distance_km", 0.0))

    return Trip(
        trip_id=trip_id,
        user=user,
        bike=bike,
        start_station=start_station,
        end_station=end_station,
        start_time=start_time,
        end_time=end_time,
        distance_km=distance_km,
    )

from models import MaintenanceRecord

def create_maintenance_record(data: dict, bikes: dict) -> MaintenanceRecord:
    """
    Create a MaintenanceRecord from a data dictionary.

    Args:
        data: dict with record info, e.g. 'record_id', 'bike_id', 'date', 'maintenance_type', 'cost'
        bikes: dict mapping bike_id -> Bike instance

    Returns:
        MaintenanceRecord instance
    """
    record_id = data["record_id"]
    bike = bikes[data["bike_id"]]

    date = datetime.fromisoformat(data["date"])
    maintenance_type = data["maintenance_type"]
    cost = float(data.get("cost", 0.0))
    description = data.get("description", "")

    return MaintenanceRecord(
        record_id=record_id,
        bike=bike,
        date=date,
        maintenance_type=maintenance_type,
        cost=cost,
        description=description,
    )

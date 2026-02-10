"""
Domain models for the CityBike Bike-Sharing Analytics platform.

This module defines the class hierarchy:
    Entity (ABC) -> Bike -> ClassicBike, ElectricBike
                 -> Station
                 -> User -> CasualUser, MemberUser
    Trip
    MaintenanceRecord
    BikeShareSystem

TODO for students:
    - Complete the Station, User, CasualUser, MemberUser classes
    - Complete the Trip and MaintenanceRecord classes
    - Implement the BikeShareSystem class
    - Add input validation to all constructors
    - Add @property decorators where appropriate
"""

from abc import ABC, abstractmethod
from datetime import datetime


# ---------------------------------------------------------------------------
# Abstract Base Class
# ---------------------------------------------------------------------------

class Entity(ABC):
    """Abstract base class for all domain entities.

    Attributes:
        id: Unique identifier for the entity.
        created_at: Timestamp when the entity was created.
    """

    def __init__(self, id: str, created_at: datetime | None = None) -> None:
        if not id or not isinstance(id, str):
            raise ValueError("id must be a non-empty string")
        self._id = id
        self._created_at = created_at or datetime.now()

    @property
    def id(self) -> str:
        """Return the entity's unique identifier."""
        return self._id

    @property
    def created_at(self) -> datetime:
        """Return the creation timestamp."""
        return self._created_at

    @abstractmethod
    def __str__(self) -> str:
        """Return a user-friendly string representation."""
        ...

    @abstractmethod
    def __repr__(self) -> str:
        """Return an unambiguous string representation for debugging."""
        ...


# ---------------------------------------------------------------------------
# Bike hierarchy
# ---------------------------------------------------------------------------

class Bike(Entity):
    """Represents a bike in the sharing system.

    Attributes:
        bike_type: Either 'classic' or 'electric'.
        status: One of 'available', 'in_use', 'maintenance'.
    """

    VALID_STATUSES = {"available", "in_use", "maintenance"}

    def __init__(
        self,
        bike_id: str,
        bike_type: str,
        status: str = "available",
    ) -> None:
        super().__init__(id=bike_id)
        if bike_type not in ("classic", "electric"):
            raise ValueError(f"Invalid bike_type: {bike_type}")
        if status not in self.VALID_STATUSES:
            raise ValueError(f"Invalid status: {status}")
        self._bike_type = bike_type
        self._status = status

    @property
    def bike_type(self) -> str:
        return self._bike_type

    @property
    def status(self) -> str:
        return self._status

    @status.setter
    def status(self, value: str) -> None:
        if value not in self.VALID_STATUSES:
            raise ValueError(f"Invalid status: {value}")
        self._status = value

    def __str__(self) -> str:
        return f"Bike({self.id}, {self.bike_type}, {self.status})"

    def __repr__(self) -> str:
        return (
            f"Bike(bike_id={self.id!r}, bike_type={self.bike_type!r}, "
            f"status={self.status!r})"
        )


class ClassicBike(Bike):
    """A classic (non-electric) bike with gears.

    Attributes:
        gear_count: Number of gears (must be positive).
    """

    def __init__(
        self,
        bike_id: str,
        gear_count: int = 7,
        status: str = "available",
    ) -> None:
        super().__init__(bike_id=bike_id, bike_type="classic", status=status)
        if gear_count <= 0:
            raise ValueError("gear_count must be positive")
        self._gear_count = gear_count

    @property
    def gear_count(self) -> int:
        return self._gear_count

    def __str__(self) -> str:
        return f"ClassicBike({self.id}, gears={self.gear_count})"

    def __repr__(self) -> str:
        return (
            f"ClassicBike(bike_id={self.id!r}, gear_count={self.gear_count}, "
            f"status={self.status!r})"
        )

# ---------------------------------------------------------------------------
# ElectricBike
# ---------------------------------------------------------------------------

class ElectricBike(Bike):
    """An electric bike with a battery."""

    def __init__(
        self,
        bike_id: str,
        battery_level: float = 100.0,
        max_range_km: float = 50.0,
        status: str = "available",
    ) -> None:
        super().__init__(bike_id=bike_id, bike_type="electric", status=status)
        if not (0.0 <= battery_level <= 100.0):
            raise ValueError("battery_level must be between 0 and 100")
        if max_range_km <= 0:
            raise ValueError("max_range_km must be positive")
        self._battery_level = battery_level
        self._max_range_km = max_range_km

    @property
    def battery_level(self) -> float:
        return self._battery_level

    @battery_level.setter
    def battery_level(self, value: float) -> None:
        if not (0.0 <= value <= 100.0):
            raise ValueError("battery_level must be between 0 and 100")
        self._battery_level = value

    @property
    def max_range_km(self) -> float:
        return self._max_range_km

    def __str__(self) -> str:
        return f"ElectricBike({self.id}, battery={self.battery_level}%, range={self.max_range_km}km)"

    def __repr__(self) -> str:
        return (
            f"ElectricBike(bike_id={self.id!r}, battery_level={self.battery_level}, "
            f"max_range_km={self.max_range_km}, status={self.status!r})"
        )


# ---------------------------------------------------------------------------
# Station
# ---------------------------------------------------------------------------

class Station(Entity):
    """Represents a bike-sharing station."""

    def __init__(
        self,
        station_id: str,
        name: str,
        capacity: int,
        latitude: float,
        longitude: float,
    ) -> None:
        super().__init__(id=station_id)
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        if not (-90 <= latitude <= 90):
            raise ValueError("latitude must be between -90 and 90")
        if not (-180 <= longitude <= 180):
            raise ValueError("longitude must be between -180 and 180")
        self._name = name
        self._capacity = capacity
        self._latitude = latitude
        self._longitude = longitude

    @property
    def name(self) -> str:
        return self._name

    @property
    def capacity(self) -> int:
        return self._capacity

    @property
    def latitude(self) -> float:
        return self._latitude

    @property
    def longitude(self) -> float:
        return self._longitude

    def __str__(self) -> str:
        return f"Station({self.id}, {self.name}, capacity={self.capacity})"

    def __repr__(self) -> str:
        return (
            f"Station(station_id={self.id!r}, name={self.name!r}, capacity={self.capacity}, "
            f"lat={self.latitude}, lon={self.longitude})"
        )


# ---------------------------------------------------------------------------
# User hierarchy
# ---------------------------------------------------------------------------

class User(Entity):
    """Base class for a system user."""

    def __init__(
        self,
        user_id: str,
        name: str,
        email: str,
        user_type: str,
    ) -> None:
        super().__init__(id=user_id)
        if "@" not in email:
            raise ValueError("Invalid email address")
        self._name = name
        self._email = email
        self._user_type = user_type

    @property
    def name(self) -> str:
        return self._name

    @property
    def email(self) -> str:
        return self._email

    @property
    def user_type(self) -> str:
        return self._user_type

    def __str__(self) -> str:
        return f"User({self.id}, {self.user_type})"

    def __repr__(self) -> str:
        return f"User(user_id={self.id!r}, name={self.name!r}, email={self.email!r}, type={self.user_type!r})"


class CasualUser(User):
    """A casual (non-member) user."""

    def __init__(
        self,
        user_id: str,
        name: str,
        email: str,
        day_pass_count: int = 0,
    ) -> None:
        super().__init__(user_id=user_id, name=name, email=email, user_type="casual")
        if day_pass_count < 0:
            raise ValueError("day_pass_count must be >= 0")
        self._day_pass_count = day_pass_count

    @property
    def day_pass_count(self) -> int:
        return self._day_pass_count

    def __str__(self) -> str:
        return f"CasualUser({self.id}, day_passes={self.day_pass_count})"

    def __repr__(self) -> str:
        return (
            f"CasualUser(user_id={self.id!r}, name={self.name!r}, email={self.email!r}, "
            f"day_pass_count={self.day_pass_count})"
        )


class MemberUser(User):
    """A registered member user."""

    VALID_TIERS = {"basic", "premium"}

    def __init__(
        self,
        user_id: str,
        name: str,
        email: str,
        membership_start: datetime,
        membership_end: datetime,
        tier: str = "basic",
    ) -> None:
        super().__init__(user_id=user_id, name=name, email=email, user_type="member")
        if membership_end <= membership_start:
            raise ValueError("membership_end must be after membership_start")
        if tier not in self.VALID_TIERS:
            raise ValueError(f"tier must be one of {self.VALID_TIERS}")
        self._membership_start = membership_start
        self._membership_end = membership_end
        self._tier = tier

    @property
    def membership_start(self) -> datetime:
        return self._membership_start

    @property
    def membership_end(self) -> datetime:
        return self._membership_end

    @property
    def tier(self) -> str:
        return self._tier

    def __str__(self) -> str:
        return f"MemberUser({self.id}, tier={self.tier})"

    def __repr__(self) -> str:
        return (
            f"MemberUser(user_id={self.id!r}, name={self.name!r}, email={self.email!r}, "
            f"start={self.membership_start}, end={self.membership_end}, tier={self.tier!r})"
        )


# ---------------------------------------------------------------------------
# Trip
# ---------------------------------------------------------------------------

class Trip:
    """Represents a single bike trip."""

    def __init__(
        self,
        trip_id: str,
        user: User,
        bike: Bike,
        start_station: Station,
        end_station: Station,
        start_time: datetime,
        end_time: datetime,
        distance_km: float,
    ) -> None:
        if distance_km < 0:
            raise ValueError("distance_km must be >= 0")
        if end_time < start_time:
            raise ValueError("end_time must be after start_time")
        self.trip_id = trip_id
        self.user = user
        self.bike = bike
        self.start_station = start_station
        self.end_station = end_station
        self.start_time = start_time
        self.end_time = end_time
        self.distance_km = distance_km

    @property
    def duration_minutes(self) -> float:
        delta = self.end_time - self.start_time
        return delta.total_seconds() / 60.0

    def __str__(self) -> str:
        return f"Trip({self.trip_id}, duration={self.duration_minutes:.1f} min)"

    def __repr__(self) -> str:
        return (
            f"Trip(trip_id={self.trip_id!r}, user={self.user.id!r}, bike={self.bike.id!r}, "
            f"start_station={self.start_station.id!r}, end_station={self.end_station.id!r}, "
            f"distance_km={self.distance_km})"
        )


# ---------------------------------------------------------------------------
# MaintenanceRecord
# ---------------------------------------------------------------------------

class MaintenanceRecord:
    """Represents a maintenance event for a bike."""

    VALID_TYPES = {
        "tire_repair",
        "brake_adjustment",
        "battery_replacement",
        "chain_lubrication",
        "general_inspection",
    }

    def __init__(
        self,
        record_id: str,
        bike: Bike,
        date: datetime,
        maintenance_type: str,
        cost: float,
        description: str = "",
    ) -> None:
        if maintenance_type not in self.VALID_TYPES:
            raise ValueError(f"Invalid maintenance_type: {maintenance_type}")
        if cost < 0:
            raise ValueError("cost must be >= 0")
        self.record_id = record_id
        self.bike = bike
        self.date = date
        self.maintenance_type = maintenance_type
        self.cost = cost
        self.description = description

    def __str__(self) -> str:
        return f"MaintenanceRecord({self.record_id}, bike={self.bike.id}, type={self.maintenance_type})"

    def __repr__(self) -> str:
        return (
            f"MaintenanceRecord(record_id={self.record_id!r}, bike={self.bike.id!r}, "
            f"type={self.maintenance_type!r}, cost={self.cost}, date={self.date})"
        )

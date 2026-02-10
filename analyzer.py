"""
Data analysis engine for the CityBike platform.

Contains the BikeShareSystem class that orchestrates:
    - CSV loading and cleaning
    - Answering business questions using Pandas
    - Generating summary reports

Students should implement the cleaning logic and at least 10 analytics methods.
"""

import pandas as pd
import numpy as np
from pathlib import Path


DATA_DIR = Path(__file__).resolve().parent / "data"
OUTPUT_DIR = Path(__file__).resolve().parent / "output"


class BikeShareSystem:
    """Central analysis class — loads, cleans, and analyzes bike-share data.

    Attributes:
        trips: DataFrame of trip records.
        stations: DataFrame of station metadata.
        maintenance: DataFrame of maintenance records.
    """

    def __init__(self) -> None:
        self.trips: pd.DataFrame | None = None
        self.stations: pd.DataFrame | None = None
        self.maintenance: pd.DataFrame | None = None

    # ------------------------------------------------------------------
    # Data loading
    # ------------------------------------------------------------------

    def load_data(self) -> None:
        """Load raw CSV files into DataFrames."""
        self.trips = pd.read_csv(DATA_DIR / "trips.csv")
        self.stations = pd.read_csv(DATA_DIR / "stations.csv")
        self.maintenance = pd.read_csv(DATA_DIR / "maintenance.csv")

        print(f"Loaded trips: {self.trips.shape}")
        print(f"Loaded stations: {self.stations.shape}")
        print(f"Loaded maintenance: {self.maintenance.shape}")

    # ------------------------------------------------------------------
    # Data inspection (provided)
    # ------------------------------------------------------------------

    def inspect_data(self) -> None:
        """Print basic info about each DataFrame."""
        for name, df in [
            ("Trips", self.trips),
            ("Stations", self.stations),
            ("Maintenance", self.maintenance),
        ]:
            print(f"\n{'='*40}")
            print(f"  {name}")
            print(f"{'='*40}")
            print(df.info())
            print(f"\nMissing values:\n{df.isnull().sum()}")
            print(f"\nFirst 3 rows:\n{df.head(3)}")

    # ------------------------------------------------------------------
    # Data cleaning
    # ------------------------------------------------------------------

    def clean_data(self) -> None:
        """Clean all DataFrames and export to CSV.

        Steps implemented:
            1. Remove duplicate rows
            2. Parse date/datetime columns
            3. Convert numeric columns stored as strings
            4. Handle missing values
            5. Remove invalid entries (e.g., end_time < start_time)
            6. Standardize categorical values
            7. Export cleaned data
        """
        if self.trips is None or self.stations is None or self.maintenance is None:
            raise RuntimeError("Call load_data() first")

        # -------------------------------
        # 1️⃣ Remove duplicates
        # -------------------------------
        self.trips = self.trips.drop_duplicates(subset=["trip_id"])
        self.stations = self.stations.drop_duplicates(subset=["station_id"])
        self.maintenance = self.maintenance.drop_duplicates(subset=["record_id"])
        print(f"After dedup: {self.trips.shape[0]} trips, "
            f"{self.stations.shape[0]} stations, "
            f"{self.maintenance.shape[0]} maintenance records")

        # -------------------------------
        # 2️⃣ Parse date/datetime columns
        # -------------------------------
        self.trips["start_time"] = pd.to_datetime(self.trips["start_time"], errors="coerce")
        self.trips["end_time"] = pd.to_datetime(self.trips["end_time"], errors="coerce")
        self.maintenance["date"] = pd.to_datetime(self.maintenance["date"], errors="coerce")

        # -------------------------------
        # 3️⃣ Convert numeric columns
        # -------------------------------
        numeric_cols = ["duration_minutes", "distance_km"]
        for col in numeric_cols:
            self.trips[col] = pd.to_numeric(self.trips[col], errors="coerce")

        self.maintenance["cost"] = pd.to_numeric(self.maintenance["cost"], errors="coerce")

        # -------------------------------
        # 4️⃣ Handle missing values
        # -------------------------------
        # Trips: drop rows missing critical info
        self.trips = self.trips.dropna(subset=["trip_id", "user_id", "bike_id",
                                            "start_station_id", "end_station_id",
                                            "start_time", "end_time", "duration_minutes", "distance_km", "status"])

        # Maintenance: drop rows missing key info
        self.maintenance = self.maintenance.dropna(subset=["record_id", "bike_id", "date", "maintenance_type", "cost"])

        # Stations: fill missing names with "Unknown"
        self.stations["station_name"] = self.stations["station_name"].fillna("Unknown")

        # -------------------------------
        # 5️⃣ Remove invalid entries
        # -------------------------------
        self.trips = self.trips[self.trips["end_time"] >= self.trips["start_time"]]
        self.trips = self.trips[self.trips["duration_minutes"] >= 0]
        self.trips = self.trips[self.trips["distance_km"] >= 0]

        # -------------------------------
        # 6️⃣ Standardize categorical values
        # -------------------------------
        cat_cols = ["status", "user_type", "bike_type"]
        for col in cat_cols:
            if col in self.trips.columns:
                self.trips[col] = self.trips[col].str.lower().str.strip()

        self.maintenance["maintenance_type"] = self.maintenance["maintenance_type"].str.lower().str.strip()

        # -------------------------------
        # 7️⃣ Export cleaned datasets
        # -------------------------------
        self.trips.to_csv(DATA_DIR / "trips_clean.csv", index=False)
        self.stations.to_csv(DATA_DIR / "stations_clean.csv", index=False)
        self.maintenance.to_csv(DATA_DIR / "maintenance_clean.csv", index=False)

        print("Cleaning complete.")
        print(f"Cleaned trips: {self.trips.shape[0]}, stations: {self.stations.shape[0]}, maintenance: {self.maintenance.shape[0]}")


    # ------------------------------------------------------------------
    # Analytics — Business Questions
    # ------------------------------------------------------------------

    def total_trips_summary(self) -> dict:
        """Q1: Total trips, total distance, average duration.

        Returns:
            Dict with 'total_trips', 'total_distance_km', 'avg_duration_min'.
        """
        df = self.trips
        return {
            "total_trips": len(df),
            "total_distance_km": round(df["distance_km"].sum(), 2),
            "avg_duration_min": round(df["duration_minutes"].mean(), 2),
        }

    def top_start_stations(self, n: int = 10) -> pd.DataFrame:
        """Q2: Top *n* most popular start stations.

        TODO: use value_counts() or groupby on start_station_id,
              merge with station names.
        """
        # Example start:
        # counts = self.trips["start_station_id"].value_counts().head(n)
        raise NotImplementedError("top_start_stations")

    def peak_usage_hours(self) -> pd.Series:
        """Q3: Trip count by hour of day.

        TODO: extract hour from start_time and count trips per hour.
        """
        raise NotImplementedError("peak_usage_hours")

    def busiest_day_of_week(self) -> pd.Series:
        """Q4: Trip count by day of week.

        TODO: extract day-of-week from start_time, count.
        """
        raise NotImplementedError("busiest_day_of_week")

    def avg_distance_by_user_type(self) -> pd.Series:
        """Q5: Average trip distance grouped by user type."""
        raise NotImplementedError("avg_distance_by_user_type")

    def monthly_trip_trend(self) -> pd.Series:
        """Q7: Monthly trip counts over time.

        TODO: extract year-month from start_time, group, count.
        """
        raise NotImplementedError("monthly_trip_trend")

    def top_active_users(self, n: int = 15) -> pd.DataFrame:
        """Q8: Top *n* most active users by trip count.

        TODO: group by user_id, count trips, sort descending.
        """
        raise NotImplementedError("top_active_users")

    def maintenance_cost_by_bike_type(self) -> pd.Series:
        """Q9: Total maintenance cost per bike type.

        TODO: group maintenance by bike_type, sum cost.
        """
        raise NotImplementedError("maintenance_cost_by_bike_type")

    def top_routes(self, n: int = 10) -> pd.DataFrame:
        """Q10: Most common start→end station pairs.

        TODO: group by (start_station_id, end_station_id), count, sort.
        """
        raise NotImplementedError("top_routes")

    # ------------------------------------------------------------------
    # Add more analytics methods here (Q6, Q11–Q14)
    # ------------------------------------------------------------------

    # ------------------------------------------------------------------
    # Reporting
    # ------------------------------------------------------------------

    def generate_summary_report(self) -> None:
        """Write a summary text report to output/summary_report.txt.

        TODO:
            - Uncomment and complete each section below
            - Add results from remaining analytics methods
        """
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        report_path = OUTPUT_DIR / "summary_report.txt"

        lines: list[str] = []
        lines.append("=" * 60)
        lines.append("  CityBike — Summary Report")
        lines.append("=" * 60)

        # --- Q1: Overall summary ---
        summary = self.total_trips_summary()
        lines.append("\n--- Overall Summary ---")
        lines.append(f"  Total trips       : {summary['total_trips']}")
        lines.append(f"  Total distance    : {summary['total_distance_km']} km")
        lines.append(f"  Avg duration      : {summary['avg_duration_min']} min")

        # --- Q2: Top start stations ---
        # TODO: uncomment once top_start_stations() is implemented
        # top_stations = self.top_start_stations()
        # lines.append("\n--- Top 10 Start Stations ---")
        # lines.append(top_stations.to_string(index=False))

        # --- Q3: Peak usage hours ---
        # TODO: uncomment once peak_usage_hours() is implemented
        # hours = self.peak_usage_hours()
        # lines.append("\n--- Peak Usage Hours ---")
        # lines.append(hours.to_string())

        # --- Q9: Maintenance cost by bike type ---
        # TODO: uncomment once maintenance_cost_by_bike_type() is implemented
        # maint_cost = self.maintenance_cost_by_bike_type()
        # lines.append("\n--- Maintenance Cost by Bike Type ---")
        # lines.append(maint_cost.to_string())

        # TODO: add more sections for Q4–Q8, Q10–Q14 …

        report_text = "\n".join(lines) + "\n"
        report_path.write_text(report_text)
        print(f"Report saved to {report_path}")

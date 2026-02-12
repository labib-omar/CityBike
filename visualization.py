"""
Matplotlib visualizations for the CityBike platform.

Creates:
    1. Bar chart — trips per station
    2. Line chart — monthly trip trend
    3. Histogram — trip duration distribution
    4. Box plot — duration by user type

Exports PNG files to output/figures/.
"""

import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path


FIGURES_DIR = Path(__file__).resolve().parent / "output" / "figures"


def _save_figure(fig: plt.Figure, filename: str) -> None:
    """Save a Matplotlib figure to the figures directory."""
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    filepath = FIGURES_DIR / filename
    fig.savefig(filepath, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {filepath}")


# ---------------------------------------------------------------------------
# 1. Bar chart — trips per station
# ---------------------------------------------------------------------------

def plot_trips_per_station(trips: pd.DataFrame, stations: pd.DataFrame) -> None:
    counts = (
        trips["start_station_id"]
        .value_counts()
        .head(10)
        .rename_axis("station_id")
        .reset_index(name="trip_count")
    )

    merged = counts.merge(
        stations[["station_id", "station_name"]],
        on="station_id",
        how="left",
    )

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.barh(merged["station_name"], merged["trip_count"], color="steelblue")
    ax.set_xlabel("Number of Trips")
    ax.set_ylabel("Station")
    ax.set_title("Top 10 Start Stations by Trip Count")
    ax.invert_yaxis()

    _save_figure(fig, "trips_per_station.png")


# ---------------------------------------------------------------------------
# 2. Line chart — monthly trend
# ---------------------------------------------------------------------------

def plot_monthly_trend(trips: pd.DataFrame) -> None:
    monthly = (
        trips
        .set_index("start_time")
        .resample("ME")
        .size()
    )

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(monthly.index, monthly.values, marker="o", label="Monthly Trips")

    ax.set_title("Monthly Trip Trend")
    ax.set_xlabel("Month")
    ax.set_ylabel("Number of Trips")
    ax.legend()
    ax.grid(True)

    _save_figure(fig, "monthly_trend.png")


# ---------------------------------------------------------------------------
# 3. Histogram — trip duration distribution
# ---------------------------------------------------------------------------

def plot_duration_histogram(trips: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(8, 5))

    ax.hist(trips["duration_minutes"], bins=30, alpha=0.7, edgecolor="black", label="Duration")

    ax.set_title("Trip Duration Distribution")
    ax.set_xlabel("Duration (minutes)")
    ax.set_ylabel("Frequency")
    ax.legend()

    _save_figure(fig, "duration_histogram.png")


# ---------------------------------------------------------------------------
# 4. Box plot — duration by user type
# ---------------------------------------------------------------------------

def plot_duration_by_user_type(trips: pd.DataFrame) -> None:
    grouped = trips.groupby("user_type")["duration_minutes"]

    data = [group for _, group in grouped]
    labels = [name for name, _ in grouped]

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.boxplot(data, labels=labels)

    ax.set_title("Trip Duration by User Type")
    ax.set_xlabel("User Type")
    ax.set_ylabel("Duration (minutes)")

    _save_figure(fig, "duration_by_user_type.png")

"""
Matplotlib visualizations for the CityBike platform.

Students should create at least 4 charts:
    1. Bar chart — trips per station or revenue by user type
    2. Line chart — monthly trip trend over time
    3. Histogram — trip duration or distance distribution
    4. Box plot — duration by user type or bike type

All charts must have: title, axis labels, legend (where applicable).
Export each chart as PNG to output/figures/.
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
# 1. Bar chart (provided as example)
# ---------------------------------------------------------------------------

def plot_trips_per_station(trips: pd.DataFrame, stations: pd.DataFrame) -> None:
    """Bar chart showing the number of trips starting at each station.

    Args:
        trips: Cleaned trips DataFrame.
        stations: Stations DataFrame (for station names).
    """
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
    """Line chart of monthly trip counts.

    TODO:
        - Extract year-month from start_time
        - Group and count
        - Plot a line chart
        - Save as 'monthly_trend.png'
    """
    raise NotImplementedError("plot_monthly_trend")


# ---------------------------------------------------------------------------
# 3. Histogram — trip duration distribution
# ---------------------------------------------------------------------------

def plot_duration_histogram(trips: pd.DataFrame) -> None:
    """Histogram of trip durations.

    TODO:
        - Use trips["duration_minutes"]
        - Choose an appropriate number of bins
        - Add title, axis labels
        - Save as 'duration_histogram.png'
    """
    raise NotImplementedError("plot_duration_histogram")


# ---------------------------------------------------------------------------
# 4. Box plot — duration by user type
# ---------------------------------------------------------------------------

def plot_duration_by_user_type(trips: pd.DataFrame) -> None:
    """Box plot comparing trip durations across user types.

    TODO:
        - Group data by user_type
        - Create side-by-side box plots
        - Add title, axis labels
        - Save as 'duration_by_user_type.png'
    """
    raise NotImplementedError("plot_duration_by_user_type")

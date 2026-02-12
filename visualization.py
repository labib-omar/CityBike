"""
Matplotlib and Seaborn visualizations for the CityBike platform.

Creates:
    1. Bar chart — trips per station
    2. Line chart — monthly trip trend
    3. Histogram — trip duration distribution
    4. Box plot — duration by user type
    5. Histogram — trip distance distribution
    6. Line chart — average duration by hour
    7. Pie chart — user type proportion
    8. Bar chart — maintenance cost by bike type
    9. Heatmap — top routes (start vs end station)

Exports PNG files to output/figures/.
"""

import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
import seaborn as sns

FIGURES_DIR = Path(__file__).resolve().parent / "output" / "figures"

def _save_figure(fig: plt.Figure, filename: str) -> None:
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    filepath = FIGURES_DIR / filename
    fig.savefig(filepath, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {filepath}")


# ---------------------------------------------------------------------------
# 1. Bar chart — trips per station
# ---------------------------------------------------------------------------
def plot_trips_per_station(trips: pd.DataFrame, stations: pd.DataFrame) -> None:
    if trips.empty or stations.empty or "start_station_id" not in trips.columns:
        return
    
    counts = trips["start_station_id"].value_counts().head(10).rename_axis("station_id").reset_index(name="trip_count")
    merged = counts.merge(stations[["station_id", "station_name"]], on="station_id", how="left")
    merged["station_name"] = merged["station_name"].fillna("Unknown")

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.barh(merged["station_name"], merged["trip_count"], color="steelblue", edgecolor="navy", linewidth=1.2)
    ax.set_xlabel("Number of Trips", fontweight="bold")
    ax.set_ylabel("Station", fontweight="bold")
    ax.set_title("Top 10 Start Stations by Trip Count", fontweight="bold", pad=15)
    ax.invert_yaxis()
    ax.grid(axis="x", alpha=0.3, linestyle="--")

    for i, (bar, value) in enumerate(zip(bars, merged["trip_count"])):
        ax.text(value + 1, i, str(int(value)), va="center", fontsize=9)

    _save_figure(fig, "trips_per_station.png")


# ---------------------------------------------------------------------------
# 2. Line chart — monthly trip trend
# ---------------------------------------------------------------------------
def plot_monthly_trend(trips: pd.DataFrame) -> None:
    if trips.empty or "start_time" not in trips.columns:
        return
    
    if not pd.api.types.is_datetime64_any_dtype(trips["start_time"]):
        trips["start_time"] = pd.to_datetime(trips["start_time"], errors="coerce")
    
    monthly = trips.set_index("start_time").resample("ME").size()
    if monthly.empty:
        return

    fig, ax = plt.subplots(figsize=(11, 6))
    ax.plot(monthly.index, monthly.values, marker="o", linewidth=2.5, markersize=8, color="#2E86AB", label="Monthly Trips")
    ax.fill_between(monthly.index, monthly.values, alpha=0.2, color="#2E86AB")
    ax.set_title("Monthly Trip Trend", fontweight="bold", pad=15)
    ax.set_xlabel("Month", fontweight="bold")
    ax.set_ylabel("Number of Trips", fontweight="bold")
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3, linestyle="--")
    fig.autofmt_xdate(rotation=45)

    _save_figure(fig, "monthly_trend.png")


# ---------------------------------------------------------------------------
# 3. Histogram — trip duration distribution
# ---------------------------------------------------------------------------
def plot_duration_histogram(trips: pd.DataFrame) -> None:
    if trips.empty or "duration_minutes" not in trips.columns:
        return

    durations = trips["duration_minutes"].dropna()
    if durations.empty:
        return

    fig, ax = plt.subplots(figsize=(9, 6))
    n, bins, patches = ax.hist(durations, bins=30, alpha=0.75, edgecolor="black", color="#A23B72")
    
    # Gradient colors
    cm = plt.cm.RdYlGn
    bin_centers = 0.5 * (bins[:-1] + bins[1:])
    col = (bin_centers - min(bin_centers)) / (max(bin_centers) - min(bin_centers))
    for c, p in zip(col, patches):
        plt.setp(p, 'facecolor', cm(c))

    ax.set_title("Trip Duration Distribution", fontweight="bold", pad=15)
    ax.set_xlabel("Duration (minutes)", fontweight="bold")
    ax.set_ylabel("Frequency", fontweight="bold")
    ax.grid(axis="y", alpha=0.3, linestyle="--")

    stats_text = f"Mean: {durations.mean():.1f} min\nMedian: {durations.median():.1f} min\nStd: {durations.std():.1f} min"
    ax.text(0.98, 0.97, stats_text, transform=ax.transAxes, fontsize=9,
            verticalalignment='top', horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

    _save_figure(fig, "duration_histogram.png")


# ---------------------------------------------------------------------------
# 4. Box plot — duration by user type
# ---------------------------------------------------------------------------
def plot_duration_by_user_type(trips: pd.DataFrame) -> None:
    if trips.empty or "user_type" not in trips.columns or "duration_minutes" not in trips.columns:
        return

    trips_clean = trips[trips["duration_minutes"].notna()].copy()
    grouped = trips_clean.groupby("user_type")["duration_minutes"]
    data = [group.values for _, group in grouped]
    labels = [name.capitalize() for name, _ in grouped]

    fig, ax = plt.subplots(figsize=(9, 6))
    bp = ax.boxplot(data, labels=labels, patch_artist=True, widths=0.6,
                    boxprops=dict(facecolor='#FFB6C1', alpha=0.7),
                    medianprops=dict(color='red', linewidth=2))

    ax.set_title("Trip Duration by User Type", fontweight="bold", pad=15)
    ax.set_xlabel("User Type", fontweight="bold")
    ax.set_ylabel("Duration (minutes)", fontweight="bold")
    ax.grid(axis="y", alpha=0.3, linestyle="--")

    for i, group in enumerate(data, 1):
        ax.plot(i, group.mean(), 'D', color='darkblue', markersize=6, label='Mean' if i==1 else '')

    ax.legend(fontsize=10)
    _save_figure(fig, "duration_by_user_type.png")


# ---------------------------------------------------------------------------
# 5. Histogram — trip distance distribution
# ---------------------------------------------------------------------------
def plot_distance_histogram(trips: pd.DataFrame) -> None:
    if trips.empty or "distance_km" not in trips.columns:
        return

    distances = trips["distance_km"].dropna()
    if distances.empty:
        return

    fig, ax = plt.subplots(figsize=(9, 6))
    ax.hist(distances, bins=30, color="#1f77b4", edgecolor="black", alpha=0.7)
    ax.set_title("Trip Distance Distribution", fontweight="bold", pad=15)
    ax.set_xlabel("Distance (km)", fontweight="bold")
    ax.set_ylabel("Frequency", fontweight="bold")
    ax.grid(axis="y", alpha=0.3, linestyle="--")
    _save_figure(fig, "distance_histogram.png")


# ---------------------------------------------------------------------------
# 6. Line chart — average duration by hour
# ---------------------------------------------------------------------------
def plot_avg_duration_by_hour(trips: pd.DataFrame) -> None:
    if trips.empty or "start_time" not in trips.columns or "duration_minutes" not in trips.columns:
        return

    trips["hour"] = trips["start_time"].dt.hour
    avg_duration = trips.groupby("hour")["duration_minutes"].mean()

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(avg_duration.index, avg_duration.values, marker="o", color="#2ca02c")
    ax.set_title("Average Trip Duration by Hour", fontweight="bold", pad=15)
    ax.set_xlabel("Hour of Day", fontweight="bold")
    ax.set_ylabel("Average Duration (min)", fontweight="bold")
    ax.grid(True, alpha=0.3, linestyle="--")
    _save_figure(fig, "avg_duration_by_hour.png")


# ---------------------------------------------------------------------------
# 7. Pie chart — user type proportion
# ---------------------------------------------------------------------------
def plot_user_type_share(trips: pd.DataFrame) -> None:
    if trips.empty or "user_type" not in trips.columns:
        return

    counts = trips["user_type"].value_counts()
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(counts, labels=counts.index.str.capitalize(), autopct="%1.1f%%",
           colors=["#1f77b4","#ff7f0e"], startangle=90)
    ax.set_title("User Type Share", fontweight="bold")
    _save_figure(fig, "user_type_share.png")


# ---------------------------------------------------------------------------
# 8. Bar chart — maintenance cost by bike type
# ---------------------------------------------------------------------------
def plot_maintenance_cost_by_bike_type(maintenance: pd.DataFrame) -> None:
    if maintenance.empty or "bike_type" not in maintenance.columns:
        return

    maintenance["bike_type"] = maintenance["bike_type"].str.lower().str.strip()
    costs = maintenance.groupby("bike_type")["cost"].sum().sort_values(ascending=False)

    fig, ax = plt.subplots(figsize=(7, 5))
    bars = ax.bar(costs.index, costs.values, color="#FF7F0E")
    ax.set_title("Maintenance Cost by Bike Type", fontweight="bold")
    ax.set_ylabel("Cost ($)", fontweight="bold")
    ax.set_xlabel("Bike Type", fontweight="bold")
    ax.grid(axis="y", alpha=0.3, linestyle="--")

    for bar, val in zip(bars, costs.values):
        ax.text(bar.get_x() + bar.get_width()/2, val + 5, f"{val:.2f}", ha='center', fontsize=9)

    _save_figure(fig, "maintenance_cost_by_bike_type.png")


# ---------------------------------------------------------------------------
# 9. Heatmap — all routes (start vs end station)
# ---------------------------------------------------------------------------
def plot_top_routes_heatmap(trips: pd.DataFrame, n: int = None) -> None:
    """Heatmap of all or top-n routes by start and end station."""
    if trips.empty or "start_station_id" not in trips.columns or "end_station_id" not in trips.columns:
        return
    
    routes = (
        trips.groupby(["start_station_id", "end_station_id"])
        .size()
        .reset_index(name="count")
        .sort_values("count", ascending=False)
    )
    
    # If n is None, show all routes; otherwise limit to top n
    if n is not None:
        routes = routes.head(n)
    
    if routes.empty:
        return

    # Get all unique stations from routes
    all_stations = sorted(set(routes["start_station_id"].unique()) | set(routes["end_station_id"].unique()))
    
    # Create full pivot with all stations to ensure complete matrix
    pivot = routes.pivot_table(index="start_station_id", columns="end_station_id", values="count", fill_value=0)
    
    # Reindex to include all stations
    pivot = pivot.reindex(index=all_stations, columns=all_stations, fill_value=0)

    # Adjust figure size based on number of stations
    num_stations = len(all_stations)
    fig_size = max(10, num_stations * 0.8)
    font_size = max(6, 12 - num_stations // 3)
    
    fig, ax = plt.subplots(figsize=(fig_size, fig_size))
    im = ax.imshow(pivot, cmap="YlOrRd", aspect="auto")
    
    # Add colorbar
    cbar = fig.colorbar(im, ax=ax, label="Trip Count")
    
    # Set ticks and labels
    ax.set_xticks(range(len(pivot.columns)))
    ax.set_yticks(range(len(pivot.index)))
    ax.set_xticklabels(pivot.columns, rotation=45, ha="right", fontsize=font_size)
    ax.set_yticklabels(pivot.index, fontsize=font_size)
    
    # Add text annotations for non-zero values
    for i in range(len(pivot.index)):
        for j in range(len(pivot.columns)):
            val = pivot.iloc[i, j]
            if val > 0:
                text_color = "white" if val > pivot.values.max() * 0.5 else "black"
                ax.text(j, i, f"{int(val)}", ha="center", va="center", color=text_color, fontsize=font_size-1, fontweight="bold")

    ax.set_xlabel("End Station", fontweight="bold", fontsize=11)
    ax.set_ylabel("Start Station", fontweight="bold", fontsize=11)
    
    if n is not None:
        title = f"Top {n} Routes Heatmap (Trip Count)"
        filename = f"top_{n}_routes_heatmap.png"
    else:
        title = f"All Routes Heatmap (Trip Count) - {len(routes)} unique routes"
        filename = "all_routes_heatmap.png"
    
    ax.set_title(title, fontweight="bold", fontsize=12, pad=15)
    
    _save_figure(fig, filename)


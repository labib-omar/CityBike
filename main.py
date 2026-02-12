"""
CityBike — Bike-Sharing Analytics Platform
===========================================

Entry point that orchestrates the full pipeline:
    1. Load raw data
    2. Inspect & clean data
    3. Run analytics (business questions)
    4. Run numerical computations
    5. Generate visualizations
    6. Export summary report

Usage:
    python main.py
"""

import numpy as np

from analyzer import BikeShareSystem
from visualization import (
    plot_trips_per_station,
    plot_monthly_trend,
    plot_duration_histogram,
    plot_duration_by_user_type,
)
from pricing import CasualPricing, MemberPricing
from numerical import calculate_fares


def main() -> None:
    """Run the complete CityBike analytics pipeline."""

    system = BikeShareSystem()

    # Step 1 — Load data
    print("\n>>> Loading data …")
    system.load_data()

    # Step 2 — Inspect
    print("\n>>> Inspecting data …")
    system.inspect_data()

    # Step 3 — Clean
    print("\n>>> Cleaning data …")
    system.clean_data()

    # Step 4 — Analytics
    print("\n>>> Running analytics …")

    summary = system.total_trips_summary()
    print(f"  Total trips      : {summary['total_trips']}")
    print(f"  Total distance   : {summary['total_distance_km']} km")
    print(f"  Avg duration     : {summary['avg_duration_min']} min")

    # Additional analytics
    print("\n  Top Start Stations:")
    print(system.top_start_stations())

    print("\n  Peak Usage Hours:")
    print(system.peak_usage_hours())

    # Step 4b — Pricing (Strategy Pattern + NumPy vectorization)
    print("\n>>> Calculating revenue …")

    casual_strategy = CasualPricing()
    member_strategy = MemberPricing()

    # Casual users
    casual_mask = system.trips["user_type"] == "casual"
    casual_trips = system.trips[casual_mask]

    casual_fares = calculate_fares(
        durations=casual_trips["duration_minutes"].to_numpy(),
        distances=casual_trips["distance_km"].to_numpy(),
        per_minute=casual_strategy.PER_MINUTE,
        per_km=casual_strategy.PER_KM,
        unlock_fee=casual_strategy.UNLOCK_FEE,
    )

    # Member users
    member_mask = system.trips["user_type"] == "member"
    member_trips = system.trips[member_mask]

    member_fares = calculate_fares(
        durations=member_trips["duration_minutes"].to_numpy(),
        distances=member_trips["distance_km"].to_numpy(),
        per_minute=member_strategy.PER_MINUTE,
        per_km=member_strategy.PER_KM,
        unlock_fee=0.0,
    )

    total_revenue = np.sum(casual_fares) + np.sum(member_fares)

    print(f"  Casual revenue   : €{np.sum(casual_fares):.2f}")
    print(f"  Member revenue   : €{np.sum(member_fares):.2f}")
    print(f"  Total revenue    : €{total_revenue:.2f}")

    # Step 5 — Visualizations
    print("\n>>> Generating visualizations …")

    plot_trips_per_station(system.trips, system.stations)
    plot_monthly_trend(system.trips)
    plot_duration_histogram(system.trips)
    plot_duration_by_user_type(system.trips)

    # Step 6 — Report
    print("\n>>> Generating summary report …")
    system.generate_summary_report()

    print("\n>>> Done! Check output/ for results.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n[ERROR] {e}")

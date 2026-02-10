"""
NumPy-based numerical computations for the CityBike platform.

Includes:
    - Station distance matrix using Euclidean distance
    - Vectorized trip statistics (mean, median, std, percentiles)
    - Outlier detection using z-scores
    - Vectorized fare calculation across all trips
"""

import numpy as np

# ---------------------------------------------------------------------------
# Distance calculations
# ---------------------------------------------------------------------------

def station_distance_matrix(
    latitudes: np.ndarray, longitudes: np.ndarray
) -> np.ndarray:
    """Compute pairwise Euclidean distances between stations.

    Uses a simplified flat-earth distance model:
        d = sqrt((lat2 - lat1)^2 + (lon2 - lon1)^2)
    """
    lat_diff = latitudes[:, np.newaxis] - latitudes[np.newaxis, :]
    lon_diff = longitudes[:, np.newaxis] - longitudes[np.newaxis, :]
    distances = np.sqrt(lat_diff**2 + lon_diff**2)
    return distances

# ---------------------------------------------------------------------------
# Trip statistics
# ---------------------------------------------------------------------------

def trip_duration_stats(durations: np.ndarray) -> dict[str, float]:
    """Compute summary statistics for trip durations."""
    return {
        "mean": float(np.mean(durations)),
        "median": float(np.median(durations)),
        "std": float(np.std(durations)),
        "p25": float(np.percentile(durations, 25)),
        "p75": float(np.percentile(durations, 75)),
        "p90": float(np.percentile(durations, 90)),
    }

# ---------------------------------------------------------------------------
# Outlier detection
# ---------------------------------------------------------------------------

def detect_outliers_zscore(
    values: np.ndarray, threshold: float = 3.0
) -> np.ndarray:
    """Identify outlier indices using the z-score method."""
    std = np.std(values)
    if std == 0:
        return np.zeros_like(values, dtype=bool)
    z = (values - np.mean(values)) / std
    return np.abs(z) > threshold

# ---------------------------------------------------------------------------
# Vectorized fare calculation
# ---------------------------------------------------------------------------

def calculate_fares(
    durations: np.ndarray,
    distances: np.ndarray,
    per_minute: float,
    per_km: float,
    unlock_fee: float = 0.0,
) -> np.ndarray:
    """Calculate fares for many trips at once using NumPy."""
    return unlock_fee + per_minute * durations + per_km * distances

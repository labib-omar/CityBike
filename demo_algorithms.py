"""
Demo script for testing custom sorting and searching algorithms
on the CityBike trips dataset.
"""

import pandas as pd
from algorithms import (
    merge_sort,
    insertion_sort,
    binary_search,
    linear_search,
    benchmark_sort,
    benchmark_search,
)

# -----------------------------
# Load trips data
# -----------------------------
trips = pd.read_csv("data/trips_clean.csv")

# We'll sort/search based on 'duration_minutes'
data = trips["duration_minutes"].tolist()
target_value = data[len(data) // 2]  # Pick a value roughly in the middle

# -----------------------------
# Sorting demo
# -----------------------------
print("\n=== Sorting Demo ===")
sorted_merge = merge_sort(data)
sorted_insertion = insertion_sort(data)

print(f"First 5 sorted by merge_sort: {sorted_merge[:5]}")
print(f"First 5 sorted by insertion_sort: {sorted_insertion[:5]}")

sort_bench = benchmark_sort(data)
print("\nSorting Benchmark (ms):")
print(sort_bench)

# -----------------------------
# Searching demo
# -----------------------------
print("\n=== Searching Demo ===")
# Make sure data is sorted for binary_search
sorted_data = sorted(data)
index_bin = binary_search(sorted_data, target_value)
index_lin = linear_search(data, target_value)
index_builtin = data.index(target_value)

print(f"Target {target_value} found at index (binary_search): {index_bin}")
print(f"Target {target_value} found at index (linear_search): {index_lin}")
print(f"Target {target_value} found at index (builtin index): {index_builtin}")

search_bench = benchmark_search(data, target_value)
print("\nSearching Benchmark (ms):")
print(search_bench)

"""
Unit tests for sorting and searching algorithms.

Covers:
    - merge_sort (fully implemented)
    - benchmark_sort (fully implemented)
"""

import pytest

from algorithms import merge_sort, benchmark_sort


# ---------------------------------------------------------------------------
# merge_sort
# ---------------------------------------------------------------------------

class TestMergeSort:

    def test_empty_list(self) -> None:
        assert merge_sort([]) == []

    def test_single_element(self) -> None:
        assert merge_sort([42]) == [42]

    def test_already_sorted(self) -> None:
        assert merge_sort([1, 2, 3, 4, 5]) == [1, 2, 3, 4, 5]

    def test_reverse_sorted(self) -> None:
        assert merge_sort([5, 4, 3, 2, 1]) == [1, 2, 3, 4, 5]

    def test_duplicates(self) -> None:
        assert merge_sort([3, 1, 2, 3, 1]) == [1, 1, 2, 3, 3]

    def test_negative_numbers(self) -> None:
        assert merge_sort([-3, 0, -1, 4, 2]) == [-3, -1, 0, 2, 4]

    def test_strings(self) -> None:
        assert merge_sort(["banana", "apple", "cherry"]) == [
            "apple", "banana", "cherry"
        ]

    def test_custom_key(self) -> None:
        data = ["bb", "a", "ccc"]
        result = merge_sort(data, key=len)
        assert result == ["a", "bb", "ccc"]

    def test_key_with_dicts(self) -> None:
        data = [
            {"name": "Charlie", "age": 30},
            {"name": "Alice", "age": 25},
            {"name": "Bob", "age": 28},
        ]
        result = merge_sort(data, key=lambda x: x["age"])
        assert [d["name"] for d in result] == ["Alice", "Bob", "Charlie"]

    def test_does_not_modify_original(self) -> None:
        original = [3, 1, 2]
        merge_sort(original)
        assert original == [3, 1, 2]

    def test_large_random_list(self) -> None:
        import random
        random.seed(0)
        data = random.sample(range(1000), 200)
        assert merge_sort(data) == sorted(data)

    def test_stability(self) -> None:
        """Equal elements should preserve their original relative order."""
        data = [(1, "a"), (2, "b"), (1, "c"), (2, "d")]
        result = merge_sort(data, key=lambda x: x[0])
        # Items with key=1 should stay in order: (1,"a") before (1,"c")
        ones = [item for item in result if item[0] == 1]
        assert ones == [(1, "a"), (1, "c")]


# ---------------------------------------------------------------------------
# benchmark_sort
# ---------------------------------------------------------------------------

class TestBenchmarkSort:

    def test_returns_dict_with_expected_keys(self) -> None:
        result = benchmark_sort([5, 3, 1, 4, 2], repeats=1)
        assert "merge_sort_ms" in result
        assert "builtin_sorted_ms" in result

    def test_timings_are_positive(self) -> None:
        result = benchmark_sort(list(range(100, 0, -1)), repeats=2)
        assert result["merge_sort_ms"] > 0
        assert result["builtin_sorted_ms"] > 0

    def test_works_with_key(self) -> None:
        data = ["bb", "a", "ccc"]
        result = benchmark_sort(data, key=len, repeats=1)
        assert isinstance(result["merge_sort_ms"], float)

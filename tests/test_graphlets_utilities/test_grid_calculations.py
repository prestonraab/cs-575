"""Tests for grid calculation functions in graphlet_utilities."""

import pytest
from src.graphlet_utilities import calculate_subplot_grid, get_axis_for_subplot


class TestCalculateSubplotGrid:
    """Test suite for calculate_subplot_grid function."""

    def test_single_graph_single_column(self) -> None:
        """Test grid calculation for a single graph."""
        num_rows, num_cols = calculate_subplot_grid(1, 4)
        assert num_rows == 1
        assert num_cols == 1

    def test_fewer_graphs_than_columns(self) -> None:
        """Test that actual columns matches number of graphs when fewer graphs than desired columns."""
        num_rows, num_cols = calculate_subplot_grid(3, 5)
        assert num_rows == 1
        assert num_cols == 3

    def test_exact_grid_fit(self) -> None:
        """Test when graphs fit exactly in the grid."""
        num_rows, num_cols = calculate_subplot_grid(8, 4)
        assert num_rows == 2
        assert num_cols == 4

    def test_graphs_require_extra_row(self) -> None:
        """Test when graphs require an extra partial row."""
        num_rows, num_cols = calculate_subplot_grid(5, 4)
        assert num_rows == 2
        assert num_cols == 4

    def test_9_graphs_3_columns(self) -> None:
        """Test 9 graphs in 3 columns (3x3 grid)."""
        num_rows, num_cols = calculate_subplot_grid(9, 3)
        assert num_rows == 3
        assert num_cols == 3

    def test_9_graphs_4_columns(self) -> None:
        """Test 9 graphs in 4 columns (need 3 rows)."""
        num_rows, num_cols = calculate_subplot_grid(9, 4)
        assert num_rows == 3
        assert num_cols == 4

    def test_10_graphs_4_columns(self) -> None:
        """Test 10 graphs in 4 columns (need 3 rows)."""
        num_rows, num_cols = calculate_subplot_grid(10, 4)
        assert num_rows == 3
        assert num_cols == 4

    def test_single_column_layout(self) -> None:
        """Test layout with only 1 column."""
        num_rows, num_cols = calculate_subplot_grid(5, 1)
        assert num_rows == 5
        assert num_cols == 1

    def test_single_row_layout(self) -> None:
        """Test layout with graphs fitting in single row."""
        num_rows, num_cols = calculate_subplot_grid(3, 10)
        assert num_rows == 1
        assert num_cols == 3

    def test_invalid_num_cols_zero(self) -> None:
        """Test that zero columns raises ValueError."""
        with pytest.raises(ValueError, match="num_cols must be at least 1"):
            calculate_subplot_grid(5, 0)

    def test_invalid_num_cols_negative(self) -> None -> None:
        """Test that negative columns raises ValueError."""
        with pytest.raises(ValueError, match="num_cols must be at least 1"):
            calculate_subplot_grid(5, -1)

    def test_large_number_of_graphs(self) -> None:
        """Test with a large number of graphs."""
        num_rows, num_cols = calculate_subplot_grid(100, 8)
        assert num_rows == 13
        assert num_cols == 8
        assert num_rows * num_cols >= 100

    def test_grid_has_enough_cells(self) -> None:
        """Test that grid always has enough cells for all graphs."""
        test_cases = [
            (1, 1),
            (5, 4),
            (9, 3),
            (17, 5),
            (100, 7),
        ]
        for num_graphs, num_cols in test_cases:
            num_rows, actual_cols = calculate_subplot_grid(num_graphs, num_cols)
            total_cells = num_rows * actual_cols
            assert total_cells >= num_graphs, (
                f"Grid with {num_rows}x{actual_cols} has {total_cells} cells, "
                f"but need {num_graphs}"
            )


class TestGetAxisForSubplot:
    """Test suite for get_axis_for_subplot function."""

    def test_single_subplot_access(self):
        """Test single subplot (1x1 grid) uses gca."""
        access_type, axis_index = get_axis_for_subplot(0, 1, 1)
        assert access_type == "gca"
        assert axis_index is None

    def test_single_row_multiple_columns(self):
        """Test single row with multiple columns uses col access."""
        access_type, axis_index = get_axis_for_subplot(2, 1, 4)
        assert access_type == "col"
        assert axis_index == 2

    def test_single_row_all_positions(self):
        """Test all positions in a single row."""
        for col in range(4):
            access_type, axis_index = get_axis_for_subplot(col, 1, 4)
            assert access_type == "col"
            assert axis_index == col

    def test_multi_row_grid_top_left(self):
        """Test top-left corner of multi-row grid."""
        access_type, axis_index = get_axis_for_subplot(0, 2, 3)
        assert access_type == "cell"
        assert axis_index == (0, 0)

    def test_multi_row_grid_middle(self):
        """Test middle position of multi-row grid."""
        access_type, axis_index = get_axis_for_subplot(4, 2, 3)
        assert access_type == "cell"
        assert axis_index == (1, 1)

    def test_multi_row_grid_bottom_right(self):
        """Test bottom-right of multi-row grid."""
        access_type, axis_index = get_axis_for_subplot(5, 2, 3)
        assert access_type == "cell"
        assert axis_index == (1, 2)

    def test_3x3_grid_all_positions(self):
        """Test all positions in a 3x3 grid."""
        expected_positions = [
            (0, 0),
            (0, 1),
            (0, 2),
            (1, 0),
            (1, 1),
            (1, 2),
            (2, 0),
            (2, 1),
            (2, 2),
        ]
        for count, expected in enumerate(expected_positions):
            access_type, axis_index = get_axis_for_subplot(count, 3, 3)
            assert access_type == "cell"
            assert axis_index == expected

    def test_2x4_grid_wraps_correctly(self):
        """Test that 2x4 grid correctly wraps to second row."""
        # First row
        for col in range(4):
            access_type, axis_index = get_axis_for_subplot(col, 2, 4)
            assert access_type == "cell"
            assert axis_index == (0, col)

        # Second row
        for col in range(4):
            access_type, axis_index = get_axis_for_subplot(4 + col, 2, 4)
            assert access_type == "cell"
            assert axis_index == (1, col)

    def test_single_row_single_column_different_count(self):
        """Test that count doesn't matter for 1x1 grid."""
        for count in [0, 5, 100]:
            access_type, axis_index = get_axis_for_subplot(count, 1, 1)
            assert access_type == "gca"
            assert axis_index is None

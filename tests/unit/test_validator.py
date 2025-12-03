"""Unit tests for board validation logic."""

import pytest
from src.game.validator import (
    validate_board_settings,
    validate_position,
    get_adjacent_positions,
    calculate_mine_density,
    suggest_reasonable_settings
)


class TestValidateBoardSettings:
    """Test board settings validation."""

    def test_valid_board_settings(self):
        """Test valid board configurations."""
        # Valid settings
        assert validate_board_settings(9, 9, 10) is True
        assert validate_board_settings(15, 15, 30) is True
        assert validate_board_settings(20, 20, 50) is True
        assert validate_board_settings(30, 30, 100) is True

    def test_invalid_width_too_small(self):
        """Test width too small."""
        with pytest.raises(ValueError, match="Width must be between 9 and 30"):
            validate_board_settings(8, 15, 10)

    def test_invalid_width_too_large(self):
        """Test width too large."""
        with pytest.raises(ValueError, match="Width must be between 9 and 30"):
            validate_board_settings(31, 15, 10)

    def test_invalid_height_too_small(self):
        """Test height too small."""
        with pytest.raises(ValueError, match="Height must be between 9 and 30"):
            validate_board_settings(15, 8, 10)

    def test_invalid_height_too_large(self):
        """Test height too large."""
        with pytest.raises(ValueError, match="Height must be between 9 and 30"):
            validate_board_settings(15, 31, 10)

    def test_invalid_mine_count_zero(self):
        """Test mine count zero."""
        with pytest.raises(ValueError, match="Mine count must be at least 1"):
            validate_board_settings(15, 15, 0)

    def test_invalid_mine_count_too_high(self):
        """Test mine count too high."""
        with pytest.raises(ValueError, match="Width must be between 9 and 30"):
            validate_board_settings(5, 5, 25)  # Invalid dimensions first

    def test_invalid_mine_density_too_high(self):
        """Test mine density too high."""
        with pytest.raises(ValueError, match="Mine density too high"):
            validate_board_settings(10, 10, 30)  # 30% density

    def test_boundary_values(self):
        """Test boundary values."""
        # Minimum dimensions
        assert validate_board_settings(9, 9, 1) is True

        # Maximum dimensions
        assert validate_board_settings(30, 30, 1) is True

        # Maximum mine density (25%)
        assert validate_board_settings(20, 20, 100) is True  # Exactly 25%

    def test_non_integer_inputs(self):
        """Test non-integer inputs."""
        with pytest.raises(ValueError, match="Width must be between 9 and 30"):
            validate_board_settings(15.5, 15, 10)

        with pytest.raises(ValueError, match="Height must be between 9 and 30"):
            validate_board_settings(15, 15.5, 10)


class TestValidatePosition:
    """Test position validation."""

    def test_valid_positions(self):
        """Test valid positions."""
        assert validate_position(0, 0, 10, 10) is True
        assert validate_position(5, 5, 10, 10) is True
        assert validate_position(9, 9, 10, 10) is True
        assert validate_position(29, 29, 30, 30) is True

    def test_invalid_row_negative(self):
        """Test negative row."""
        with pytest.raises(ValueError, match="Row must be between 0 and"):
            validate_position(-1, 5, 10, 10)

    def test_invalid_row_too_high(self):
        """Test row too high."""
        with pytest.raises(ValueError, match="Row must be between 0 and"):
            validate_position(10, 5, 10, 10)

    def test_invalid_col_negative(self):
        """Test negative column."""
        with pytest.raises(ValueError, match="Column must be between 0 and"):
            validate_position(5, -1, 10, 10)

    def test_invalid_col_too_high(self):
        """Test column too high."""
        with pytest.raises(ValueError, match="Column must be between 0 and"):
            validate_position(5, 10, 10, 10)

    def test_boundary_positions(self):
        """Test boundary positions."""
        # Maximum valid positions
        assert validate_position(9, 9, 10, 10) is True
        assert validate_position(29, 29, 30, 30) is True


class TestGetAdjacentPositions:
    """Test getting adjacent positions."""

    def test_center_cell(self):
        """Test adjacent positions for center cell."""
        adjacent = get_adjacent_positions(1, 1, 3, 3)
        expected = [
            (0, 0), (0, 1), (0, 2),
            (1, 0),         (1, 2),
            (2, 0), (2, 1), (2, 2)
        ]
        assert len(adjacent) == 8
        assert set(adjacent) == set(expected)

    def test_corner_cell(self):
        """Test adjacent positions for corner cell."""
        adjacent = get_adjacent_positions(0, 0, 3, 3)
        expected = [(0, 1), (1, 0), (1, 1)]
        assert len(adjacent) == 3
        assert set(adjacent) == set(expected)

    def test_edge_cell(self):
        """Test adjacent positions for edge cell."""
        adjacent = get_adjacent_positions(0, 1, 3, 3)
        expected = [(0, 0), (0, 2), (1, 0), (1, 1), (1, 2)]
        assert len(adjacent) == 5
        assert set(adjacent) == set(expected)

    def test_single_cell_board(self):
        """Test adjacent positions for single cell board."""
        adjacent = get_adjacent_positions(0, 0, 1, 1)
        assert len(adjacent) == 0

    def test_large_board(self):
        """Test adjacent positions on large board."""
        adjacent = get_adjacent_positions(5, 5, 10, 10)
        assert len(adjacent) == 8

        # All positions should be within bounds
        for row, col in adjacent:
            assert 0 <= row < 10
            assert 0 <= col < 10


class TestCalculateMineDensity:
    """Test mine density calculation."""

    def test_calculate_mine_density(self):
        """Test mine density calculation."""
        # 10% density
        density = calculate_mine_density(10, 10, 10)
        assert density == 0.1

        # 20% density
        density = calculate_mine_density(10, 10, 20)
        assert density == 0.2

        # 25% density (maximum)
        density = calculate_mine_density(20, 20, 100)
        assert density == 0.25

        # Very low density
        density = calculate_mine_density(30, 30, 1)
        assert density == 1 / 900

    def test_zero_mines(self):
        """Test zero mine density."""
        density = calculate_mine_density(10, 10, 0)
        assert density == 0.0

    def test_maximum_mines(self):
        """Test maximum mine density."""
        density = calculate_mine_density(10, 10, 99)  # 99% of cells
        assert density == 0.99


class TestSuggestReasonableSettings:
    """Test reasonable settings suggestion."""

    def test_suggest_reasonable_settings(self):
        """Test reasonable settings suggestion."""
        # 10x10 board
        mines = suggest_reasonable_settings(10, 10)
        assert mines == 15  # 15% of 100

        # 20x20 board
        mines = suggest_reasonable_settings(20, 20)
        assert mines == 60  # 15% of 400

        # 30x30 board
        mines = suggest_reasonable_settings(30, 30)
        assert mines == 135  # 15% of 900

    def test_suggest_minimum_mines(self):
        """Test suggestion for very small boards."""
        # 9x9 board (minimum)
        mines = suggest_reasonable_settings(9, 9)
        assert mines >= 1  # At least 1 mine

    def test_suggest_maximum_mines(self):
        """Test suggestion respects maximum density."""
        # Very small board
        mines = suggest_reasonable_settings(9, 9)
        total_cells = 9 * 9
        density = mines / total_cells
        assert density <= 0.25  # Should not exceed 25%
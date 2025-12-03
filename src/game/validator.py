"""Validation logic for minesweeper game settings."""

from typing import Tuple


def validate_board_settings(width: int, height: int, mine_count: int) -> bool:
    """Validate board configuration parameters.

    Args:
        width: Board width in cells
        height: Board height in cells
        mine_count: Number of mines

    Returns:
        True if settings are valid

    Raises:
        ValueError: If any parameter is invalid
    """
    # Validate dimensions
    if not isinstance(width, int) or width < 9 or width > 30:
        raise ValueError(f"Width must be between 9 and 30, got {width}")

    if not isinstance(height, int) or height < 9 or height > 30:
        raise ValueError(f"Height must be between 9 and 30, got {height}")

    if not isinstance(mine_count, int):
        raise ValueError(f"Mine count must be an integer, got {type(mine_count)}")

    # Validate mine count
    total_cells = width * height
    if mine_count < 1:
        raise ValueError(f"Mine count must be at least 1, got {mine_count}")

    if mine_count >= total_cells:
        raise ValueError(f"Mine count must be less than total cells ({total_cells}), got {mine_count}")

    # Check mine density (max 25% for playability)
    mine_density = mine_count / total_cells
    if mine_density > 0.25:
        raise ValueError(f"Mine density too high: {mine_density:.1%}, max 25%")

    return True


def validate_position(row: int, col: int, width: int, height: int) -> bool:
    """Validate cell position coordinates.

    Args:
        row: Row position (0-indexed)
        col: Column position (0-indexed)
        width: Board width
        height: Board height

    Returns:
        True if position is valid

    Raises:
        ValueError: If position is out of bounds
    """
    if not isinstance(row, int) or row < 0 or row >= height:
        raise ValueError(f"Row must be between 0 and {height-1}, got {row}")

    if not isinstance(col, int) or col < 0 or col >= width:
        raise ValueError(f"Column must be between 0 and {width-1}, got {col}")

    return True


def get_adjacent_positions(row: int, col: int, width: int, height: int) -> list[Tuple[int, int]]:
    """Get all valid adjacent positions for a cell.

    Args:
        row: Row position
        col: Column position
        width: Board width
        height: Board height

    Returns:
        List of (row, col) tuples for adjacent cells
    """
    adjacent = []

    # Check all 8 directions
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:  # Skip the cell itself
                continue

            new_row, new_col = row + dr, col + dc

            # Check bounds
            if 0 <= new_row < height and 0 <= new_col < width:
                adjacent.append((new_row, new_col))

    return adjacent


def calculate_mine_density(width: int, height: int, mine_count: int) -> float:
    """Calculate mine density as a percentage.

    Args:
        width: Board width
        height: Board height
        mine_count: Number of mines

    Returns:
        Mine density as a percentage (0.0 to 1.0)
    """
    total_cells = width * height
    return mine_count / total_cells


def suggest_reasonable_settings(width: int, height: int) -> int:
    """Suggest a reasonable mine count for given dimensions.

    Args:
        width: Board width
        height: Board height

    Returns:
        Suggested mine count
    """
    total_cells = width * height

    # Use 15% density as a reasonable default
    suggested_mines = int(total_cells * 0.15)

    # Ensure at least 1 mine and reasonable limits
    suggested_mines = max(1, suggested_mines)
    suggested_mines = min(suggested_mines, total_cells - 1)

    return suggested_mines
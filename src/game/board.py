"""Board entity for minesweeper game with grid management and mine generation."""

import random
from typing import List, Set, Tuple, Optional
from .cell import Cell
from .validator import validate_position, get_adjacent_positions


class Board:
    """Represents the minesweeper game board."""

    def __init__(self, width: int, height: int, mine_count: int):
        """Initialize a new board with given dimensions and mine count.

        Args:
            width: Number of columns (9-30)
            height: Number of rows (9-30)
            mine_count: Number of mines to place
        """
        self.width = width
        self.height = height
        self.mine_count = mine_count
        self.cells: List[List[Cell]] = []
        self.revealed_count = 0
        self.flagged_count = 0
        self.first_click = True
        self.mine_positions: Set[Tuple[int, int]] = set()

        # Initialize empty grid
        self._initialize_grid()

    def _initialize_grid(self) -> None:
        """Initialize the grid with empty cells."""
        self.cells = []
        for row in range(self.height):
            row_cells = []
            for col in range(self.width):
                row_cells.append(Cell(row, col))
            self.cells.append(row_cells)

    def generate_mines(self, safe_row: int, safe_col: int) -> None:
        """Generate mines, ensuring the safe position is not a mine.

        Args:
            safe_row: Row position that must not be a mine (first click)
            safe_col: Column position that must not be a mine (first click)
        """
        # Only generate mines if not already generated
        if self.mine_positions:
            return

        # Get all possible positions except the safe one
        all_positions = []
        for row in range(self.height):
            for col in range(self.width):
                if (row, col) != (safe_row, safe_col):
                    all_positions.append((row, col))

        # Randomly select mine positions
        self.mine_positions = set(random.sample(all_positions, self.mine_count))

        # Place mines
        for row, col in self.mine_positions:
            self.cells[row][col].set_mine()

        # Calculate adjacent mine counts
        self._calculate_adjacent_mines()

    def _calculate_adjacent_mines(self) -> None:
        """Calculate the number of adjacent mines for each cell."""
        for row in range(self.height):
            for col in range(self.width):
                if not self.cells[row][col].is_mine:
                    adjacent_mines = self._count_adjacent_mines(row, col)
                    self.cells[row][col].set_adjacent_mines(adjacent_mines)

    def _count_adjacent_mines(self, row: int, col: int) -> int:
        """Count mines in adjacent cells.

        Args:
            row: Row position
            col: Column position

        Returns:
            Number of adjacent mines (0-8)
        """
        count = 0
        adjacent_positions = get_adjacent_positions(row, col, self.width, self.height)

        for adj_row, adj_col in adjacent_positions:
            if self.cells[adj_row][adj_col].is_mine:
                count += 1

        return count

    def reveal_cell(self, row: int, col: int) -> bool:
        """Reveal a cell at the given position.

        Args:
            row: Row position (0-indexed)
            col: Column position (0-indexed)

        Returns:
            True if cell was revealed, False if it was already revealed or flagged

        Raises:
            ValueError: If position is out of bounds
        """
        validate_position(row, col, self.width, self.height)

        cell = self.cells[row][col]

        # Cannot reveal flagged or already revealed cells
        if not cell.can_reveal():
            return False

        # First click - generate mines
        if self.first_click:
            self.generate_mines(row, col)
            self.first_click = False

        # Reveal the cell
        cell.reveal()
        self.revealed_count += 1

        # If this is an empty cell (no adjacent mines), reveal adjacent cells
        if cell.adjacent_mines == 0 and not cell.is_mine:
            self._reveal_adjacent_empty_cells(row, col)

        return True

    def _reveal_adjacent_empty_cells(self, row: int, col: int) -> None:
        """Recursively reveal adjacent empty cells.

        Args:
            row: Starting row position
            col: Starting column position
        """
        to_reveal = [(row, col)]
        revealed = set()

        while to_reveal:
            current_row, current_col = to_reveal.pop()

            if (current_row, current_col) in revealed:
                continue

            revealed.add((current_row, current_col))

            # Get adjacent positions
            adjacent_positions = get_adjacent_positions(
                current_row, current_col, self.width, self.height
            )

            for adj_row, adj_col in adjacent_positions:
                adj_cell = self.cells[adj_row][adj_col]

                # Only reveal hidden cells
                if adj_cell.is_hidden and not adj_cell.is_flagged:
                    adj_cell.reveal()
                    self.revealed_count += 1

                    # If this adjacent cell is also empty, add it to the queue
                    if adj_cell.adjacent_mines == 0 and not adj_cell.is_mine:
                        to_reveal.append((adj_row, adj_col))

    def flag_cell(self, row: int, col: int) -> bool:
        """Toggle flag on a cell at the given position.

        Args:
            row: Row position (0-indexed)
            col: Column position (0-indexed)

        Returns:
            True if flag was toggled, False if cell cannot be flagged

        Raises:
            ValueError: If position is out of bounds
        """
        validate_position(row, col, self.width, self.height)

        cell = self.cells[row][col]

        # Cannot flag revealed cells
        if not cell.can_flag():
            return False

        # Toggle flag
        was_flagged = cell.is_flagged
        cell.flag()

        # Update flag count
        if was_flagged and not cell.is_flagged:
            self.flagged_count -= 1
        elif not was_flagged and cell.is_flagged:
            self.flagged_count += 1

        return True

    def expand_adjacent_cells(self, row: int, col: int) -> Set[Tuple[int, int]]:
        """Auto-expand adjacent cells when correct number of flags are placed.

        Args:
            row: Row position of revealed cell
            col: Column position of revealed cell

        Returns:
            Set of (row, col) tuples for cells that were revealed

        Raises:
            ValueError: If position is out of bounds or cell is not revealed
        """
        validate_position(row, col, self.width, self.height)

        cell = self.cells[row][col]

        # Only expand revealed cells with numbers
        if not cell.is_revealed or cell.adjacent_mines == 0:
            return set()

        # Count adjacent flags
        adjacent_positions = get_adjacent_positions(row, col, self.width, self.height)
        flag_count = 0
        hidden_adjacent = []

        for adj_row, adj_col in adjacent_positions:
            adj_cell = self.cells[adj_row][adj_col]
            if adj_cell.is_flagged:
                flag_count += 1
            elif adj_cell.is_hidden:
                hidden_adjacent.append((adj_row, adj_col))

        # Only expand if correct number of flags are placed
        if flag_count != cell.adjacent_mines:
            return set()

        # Reveal all hidden adjacent cells
        revealed = set()
        for adj_row, adj_col in hidden_adjacent:
            if self.reveal_cell(adj_row, adj_col):
                revealed.add((adj_row, adj_col))

        return revealed

    def check_win_condition(self) -> bool:
        """Check if the game has been won.

        Returns:
            True if all non-mine cells are revealed
        """
        total_non_mine_cells = (self.width * self.height) - self.mine_count
        return self.revealed_count == total_non_mine_cells

    def check_lose_condition(self) -> bool:
        """Check if the game has been lost.

        Returns:
            True if any mine has been revealed
        """
        for row, col in self.mine_positions:
            if self.cells[row][col].is_revealed:
                return True
        return False

    def get_cell(self, row: int, col: int) -> Cell:
        """Get cell at the given position.

        Args:
            row: Row position (0-indexed)
            col: Column position (0-indexed)

        Returns:
            Cell object at the position

        Raises:
            ValueError: If position is out of bounds
        """
        validate_position(row, col, self.width, self.height)
        return self.cells[row][col]

    def get_board_state(self) -> List[List[dict]]:
        """Get the current state of the board for serialization.

        Returns:
            2D list of cell state dictionaries
        """
        state = []
        for row in range(self.height):
            row_state = []
            for col in range(self.width):
                cell = self.cells[row][col]
                row_state.append({
                    'row': row,
                    'col': col,
                    'is_mine': cell.is_mine,
                    'is_revealed': cell.is_revealed,
                    'is_flagged': cell.is_flagged,
                    'adjacent_mines': cell.adjacent_mines,
                    'can_reveal': cell.can_reveal(),
                    'can_flag': cell.can_flag()
                })
            state.append(row_state)
        return state

    def __str__(self) -> str:
        """String representation of the board."""
        lines = []
        lines.append(f"Board({self.width}x{self.height}, {self.mine_count} mines)")
        lines.append(f"Revealed: {self.revealed_count}, Flagged: {self.flagged_count}")

        # Show board state (for debugging)
        for row in range(self.height):
            row_str = ""
            for col in range(self.width):
                cell = self.cells[row][col]
                if cell.is_flagged:
                    row_str += "F"
                elif not cell.is_revealed:
                    row_str += "?"
                elif cell.is_mine:
                    row_str += "*"
                else:
                    row_str += str(cell.adjacent_mines)
                row_str += " "
            lines.append(row_str)

        return "\n".join(lines)
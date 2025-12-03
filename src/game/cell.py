"""Cell entity with state pattern for minesweeper game."""

from abc import ABC, abstractmethod
from enum import Enum


class CellState(ABC):
    """Abstract base class for cell states."""

    @abstractmethod
    def reveal(self) -> 'CellState':
        """Reveal the cell and return new state."""
        pass

    @abstractmethod
    def flag(self) -> 'CellState':
        """Toggle flag on cell and return new state."""
        pass

    @abstractmethod
    def can_reveal(self) -> bool:
        """Check if cell can be revealed."""
        pass

    @abstractmethod
    def can_flag(self) -> bool:
        """Check if cell can be flagged."""
        pass


class HiddenState(CellState):
    """Hidden cell state - default state for unrevealed cells."""

    def reveal(self) -> CellState:
        """Reveal the cell."""
        return RevealedState()

    def flag(self) -> CellState:
        """Flag the cell."""
        return FlaggedState()

    def can_reveal(self) -> bool:
        """Hidden cells can be revealed."""
        return True

    def can_flag(self) -> bool:
        """Hidden cells can be flagged."""
        return True

    def __str__(self) -> str:
        return "Hidden"


class RevealedState(CellState):
    """Revealed cell state - cell has been clicked and revealed."""

    def reveal(self) -> CellState:
        """Already revealed - no change."""
        return self

    def flag(self) -> CellState:
        """Cannot flag revealed cell."""
        return self

    def can_reveal(self) -> bool:
        """Revealed cells cannot be revealed again."""
        return False

    def can_flag(self) -> bool:
        """Revealed cells cannot be flagged."""
        return False

    def __str__(self) -> str:
        return "Revealed"


class FlaggedState(CellState):
    """Flagged cell state - cell has been marked as potential mine."""

    def reveal(self) -> CellState:
        """Cannot reveal flagged cell."""
        return self

    def flag(self) -> CellState:
        """Unflag the cell."""
        return HiddenState()

    def can_reveal(self) -> bool:
        """Flagged cells cannot be revealed."""
        return False

    def can_flag(self) -> bool:
        """Flagged cells can be unflagged."""
        return True

    def __str__(self) -> str:
        return "Flagged"


class Cell:
    """Represents a single cell on the minesweeper board."""

    def __init__(self, row: int, col: int):
        """Initialize a cell at the given position."""
        self.row = row
        self.col = col
        self._state = HiddenState()
        self.is_mine = False
        self.adjacent_mines = 0

    def reveal(self) -> None:
        """Reveal the cell if possible."""
        if self.can_reveal():
            self._state = self._state.reveal()

    def flag(self) -> None:
        """Toggle flag on the cell if possible."""
        if self.can_flag():
            self._state = self._state.flag()

    def can_reveal(self) -> bool:
        """Check if cell can be revealed."""
        return self._state.can_reveal()

    def can_flag(self) -> bool:
        """Check if cell can be flagged."""
        return self._state.can_flag()

    @property
    def is_revealed(self) -> bool:
        """Check if cell is revealed."""
        return isinstance(self._state, RevealedState)

    @property
    def is_flagged(self) -> bool:
        """Check if cell is flagged."""
        return isinstance(self._state, FlaggedState)

    @property
    def is_hidden(self) -> bool:
        """Check if cell is hidden."""
        return isinstance(self._state, HiddenState)

    def set_mine(self) -> None:
        """Mark this cell as containing a mine."""
        self.is_mine = True

    def set_adjacent_mines(self, count: int) -> None:
        """Set the number of adjacent mines."""
        if not 0 <= count <= 8:
            raise ValueError(f"Adjacent mines must be between 0 and 8, got {count}")
        self.adjacent_mines = count

    def __str__(self) -> str:
        """String representation of the cell."""
        return f"Cell({self.row}, {self.col}, {self._state}, mine={self.is_mine}, adjacent={self.adjacent_mines})"

    def __repr__(self) -> str:
        """Detailed representation of the cell."""
        return self.__str__()
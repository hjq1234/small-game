"""Unit tests for Cell entity and state pattern."""

import pytest
from src.game.cell import Cell, HiddenState, RevealedState, FlaggedState


class TestCellStates:
    """Test cell state classes."""

    def test_hidden_state(self):
        """Test HiddenState behavior."""
        state = HiddenState()

        # Can reveal
        new_state = state.reveal()
        assert isinstance(new_state, RevealedState)

        # Can flag
        new_state = state.flag()
        assert isinstance(new_state, FlaggedState)

        # Can reveal and flag
        assert state.can_reveal() is True
        assert state.can_flag() is True

    def test_revealed_state(self):
        """Test RevealedState behavior."""
        state = RevealedState()

        # Cannot reveal again
        new_state = state.reveal()
        assert new_state is state

        # Cannot flag
        new_state = state.flag()
        assert new_state is state

        # Cannot reveal or flag
        assert state.can_reveal() is False
        assert state.can_flag() is False

    def test_flagged_state(self):
        """Test FlaggedState behavior."""
        state = FlaggedState()

        # Cannot reveal
        new_state = state.reveal()
        assert new_state is state

        # Can unflag
        new_state = state.flag()
        assert isinstance(new_state, HiddenState)

        # Cannot reveal, can flag (unflag)
        assert state.can_reveal() is False
        assert state.can_flag() is True


class TestCell:
    """Test Cell entity."""

    def test_cell_initialization(self):
        """Test cell creation."""
        cell = Cell(2, 3)
        assert cell.row == 2
        assert cell.col == 3
        assert cell.is_hidden is True
        assert cell.is_revealed is False
        assert cell.is_flagged is False
        assert cell.is_mine is False
        assert cell.adjacent_mines == 0

    def test_cell_reveal(self):
        """Test cell revealing."""
        cell = Cell(0, 0)

        # Can reveal hidden cell
        assert cell.can_reveal() is True
        cell.reveal()
        assert cell.is_revealed is True
        assert cell.is_hidden is False

        # Cannot reveal again
        assert cell.can_reveal() is False
        cell.reveal()  # Should not change state
        assert cell.is_revealed is True

    def test_cell_flag(self):
        """Test cell flagging."""
        cell = Cell(0, 0)

        # Can flag hidden cell
        assert cell.can_flag() is True
        cell.flag()
        assert cell.is_flagged is True
        assert cell.is_hidden is False

        # Can unflag
        cell.flag()
        assert cell.is_flagged is False
        assert cell.is_hidden is True

    def test_cell_flag_prevents_reveal(self):
        """Test that flagged cells cannot be revealed."""
        cell = Cell(0, 0)
        cell.flag()
        assert cell.is_flagged is True
        assert cell.can_reveal() is False

        # Try to reveal flagged cell
        cell.reveal()
        assert cell.is_flagged is True  # Should not change
        assert cell.is_revealed is False

    def test_cell_reveal_prevents_flag(self):
        """Test that revealed cells cannot be flagged."""
        cell = Cell(0, 0)
        cell.reveal()
        assert cell.is_revealed is True
        assert cell.can_flag() is False

        # Try to flag revealed cell
        cell.flag()
        assert cell.is_revealed is True  # Should not change
        assert cell.is_flagged is False

    def test_mine_setting(self):
        """Test setting cell as mine."""
        cell = Cell(0, 0)
        assert cell.is_mine is False

        cell.set_mine()
        assert cell.is_mine is True

    def test_adjacent_mines_setting(self):
        """Test setting adjacent mine count."""
        cell = Cell(0, 0)
        assert cell.adjacent_mines == 0

        cell.set_adjacent_mines(3)
        assert cell.adjacent_mines == 3

    def test_adjacent_mines_validation(self):
        """Test adjacent mine count validation."""
        cell = Cell(0, 0)

        # Valid values
        for count in range(9):
            cell.set_adjacent_mines(count)
            assert cell.adjacent_mines == count

        # Invalid values
        with pytest.raises(ValueError):
            cell.set_adjacent_mines(-1)

        with pytest.raises(ValueError):
            cell.set_adjacent_mines(9)

    def test_cell_string_representation(self):
        """Test cell string representation."""
        cell = Cell(1, 2)
        cell.set_adjacent_mines(3)
        cell.set_mine()

        str_repr = str(cell)
        assert "Cell(1, 2" in str_repr
        assert "mine=True" in str_repr
        assert "adjacent=3" in str_repr
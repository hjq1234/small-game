"""Unit tests for Board entity."""

import pytest
from src.game.board import Board
from src.game.cell import Cell


class TestBoardInitialization:
    """Test board creation and initialization."""

    def test_board_creation(self):
        """Test basic board creation."""
        board = Board(9, 9, 10)
        assert board.width == 9
        assert board.height == 9
        assert board.mine_count == 10
        assert board.revealed_count == 0
        assert board.flagged_count == 0
        assert board.first_click is True

    def test_board_grid_initialization(self):
        """Test that board creates correct grid structure."""
        board = Board(5, 4, 3)
        assert len(board.cells) == 4  # height
        assert len(board.cells[0]) == 5  # width
        assert isinstance(board.cells[0][0], Cell)

    def test_board_cell_positions(self):
        """Test that cells have correct positions."""
        board = Board(3, 2, 1)
        for row in range(2):
            for col in range(3):
                cell = board.cells[row][col]
                assert cell.row == row
                assert cell.col == col


class TestMineGeneration:
    """Test mine generation functionality."""

    def test_mine_generation_count(self):
        """Test that correct number of mines are generated."""
        board = Board(9, 9, 10)
        board.generate_mines(0, 0)
        assert len(board.mine_positions) == 10

    def test_safe_position_not_mined(self):
        """Test that safe position is not mined."""
        board = Board(9, 9, 10)
        safe_row, safe_col = 4, 4
        board.generate_mines(safe_row, safe_col)
        assert (safe_row, safe_col) not in board.mine_positions

    def test_mines_placed_on_cells(self):
        """Test that mines are properly placed on cells."""
        board = Board(5, 5, 5)
        board.generate_mines(0, 0)

        mine_count = 0
        for row in range(5):
            for col in range(5):
                if board.cells[row][col].is_mine:
                    mine_count += 1
                    assert (row, col) in board.mine_positions

        assert mine_count == 5


class TestAdjacentMineCalculation:
    """Test adjacent mine counting."""

    def test_adjacent_mines_corner_cell(self):
        """Test adjacent mine count for corner cell."""
        board = Board(3, 3, 1)
        # Place mine at (0, 1)
        board.cells[0][1].set_mine()
        board.mine_positions = {(0, 1)}
        board._calculate_adjacent_mines()

        # Cell (0, 0) should have 1 adjacent mine
        assert board.cells[0][0].adjacent_mines == 1

    def test_adjacent_mines_edge_cell(self):
        """Test adjacent mine count for edge cell."""
        board = Board(3, 3, 2)
        # Place mines at (0, 0) and (0, 2)
        board.cells[0][0].set_mine()
        board.cells[0][2].set_mine()
        board.mine_positions = {(0, 0), (0, 2)}
        board._calculate_adjacent_mines()

        # Cell (0, 1) should have 2 adjacent mines
        assert board.cells[0][1].adjacent_mines == 2

    def test_adjacent_mines_center_cell(self):
        """Test adjacent mine count for center cell."""
        board = Board(3, 3, 4)
        # Place mines in all adjacent positions to center
        board.cells[0][1].set_mine()  # top
        board.cells[1][0].set_mine()  # left
        board.cells[1][2].set_mine()  # right
        board.cells[2][1].set_mine()  # bottom
        board.mine_positions = {(0, 1), (1, 0), (1, 2), (2, 1)}
        board._calculate_adjacent_mines()

        # Cell (1, 1) should have 4 adjacent mines
        assert board.cells[1][1].adjacent_mines == 4

    def test_adjacent_mines_zero(self):
        """Test cell with no adjacent mines."""
        board = Board(3, 3, 0)
        board._calculate_adjacent_mines()

        for row in range(3):
            for col in range(3):
                assert board.cells[row][col].adjacent_mines == 0


class TestCellRevealing:
    """Test cell revealing functionality."""

    def test_reveal_hidden_cell(self):
        """Test revealing a hidden cell."""
        board = Board(3, 3, 0)
        board.generate_mines(0, 0)

        # Place a mine to prevent full expansion
        board.cells[1][1].set_mine()
        board.cells[1][1].set_adjacent_mines(0)
        board._calculate_adjacent_mines()

        success = board.reveal_cell(0, 0)
        assert success is True
        assert board.cells[0][0].is_revealed is True
        assert board.revealed_count >= 1  # May expand if adjacent_mines == 0

    def test_reveal_flagged_cell_fails(self):
        """Test that revealing a flagged cell fails."""
        board = Board(3, 3, 0)
        board.cells[1][1].flag()

        success = board.reveal_cell(1, 1)
        assert success is False
        assert board.cells[1][1].is_revealed is False

    def test_reveal_revealed_cell_fails(self):
        """Test that revealing an already revealed cell fails."""
        board = Board(3, 3, 0)
        board.generate_mines(0, 0)

        # Place a mine to prevent expansion
        board.cells[1][1].set_mine()
        board.cells[1][1].set_adjacent_mines(0)
        board._calculate_adjacent_mines()

        board.reveal_cell(0, 0)
        initial_count = board.revealed_count

        success = board.reveal_cell(0, 0)
        assert success is False
        assert board.revealed_count == initial_count  # Count shouldn't increase

    def test_first_click_generates_mines(self):
        """Test that first click triggers mine generation."""
        board = Board(3, 3, 2)
        assert board.first_click is True
        assert len(board.mine_positions) == 0

        board.reveal_cell(1, 1)
        assert board.first_click is False
        assert len(board.mine_positions) == 2

    def test_reveal_empty_cell_expands_adjacent(self):
        """Test that revealing empty cell expands adjacent cells."""
        board = Board(5, 5, 1)
        # Place mine far away
        board.generate_mines(0, 0)

        # Find an empty cell
        empty_cell = None
        for row in range(5):
            for col in range(5):
                if not board.cells[row][col].is_mine and board.cells[row][col].adjacent_mines == 0:
                    empty_cell = (row, col)
                    break
            if empty_cell:
                break

        if empty_cell:
            row, col = empty_cell
            initial_revealed = board.revealed_count
            board.reveal_cell(row, col)
            # Should reveal more than just this cell
            assert board.revealed_count > initial_revealed


class TestFlagging:
    """Test cell flagging functionality."""

    def test_flag_hidden_cell(self):
        """Test flagging a hidden cell."""
        board = Board(3, 3, 0)

        success = board.flag_cell(1, 1)
        assert success is True
        assert board.cells[1][1].is_flagged is True
        assert board.flagged_count == 1

    def test_unflag_flagged_cell(self):
        """Test unflagging a flagged cell."""
        board = Board(3, 3, 0)
        board.flag_cell(1, 1)

        success = board.flag_cell(1, 1)  # Toggle flag off
        assert success is True
        assert board.cells[1][1].is_flagged is False
        assert board.flagged_count == 0

    def test_flag_revealed_cell_fails(self):
        """Test that flagging a revealed cell fails."""
        board = Board(3, 3, 0)
        board.reveal_cell(1, 1)

        success = board.flag_cell(1, 1)
        assert success is False
        assert board.cells[1][1].is_flagged is False


class TestWinLoseConditions:
    """Test win and lose condition checking."""

    def test_win_condition_all_revealed(self):
        """Test win condition when all non-mine cells are revealed."""
        board = Board(3, 3, 1)
        board.generate_mines(0, 0)

        # Reveal all non-mine cells
        for row in range(3):
            for col in range(3):
                if not board.cells[row][col].is_mine:
                    board.reveal_cell(row, col)

        # The win condition should be met
        assert board.check_win_condition() is True

    def test_win_condition_not_met(self):
        """Test win condition when not all cells are revealed."""
        board = Board(3, 3, 1)
        board.generate_mines(0, 0)

        # Reveal only one cell (not enough to win)
        # But first we need to prevent auto-expansion by placing mines strategically
        # Find a cell that won't trigger auto-expansion
        target_row, target_col = 2, 2  # Corner cell
        if board.cells[target_row][target_col].adjacent_mines == 0:
            # If it's empty, it will auto-expand, so skip this test
            pytest.skip("Cannot test partial win - cell would auto-expand")

        board.reveal_cell(target_row, target_col)

        # Should not be won yet since we need to reveal 8 out of 9 total cells
        # (9 total - 1 mine = 8 non-mine cells needed to win)
        assert board.check_win_condition() is False

    def test_lose_condition_mine_revealed(self):
        """Test lose condition when mine is revealed."""
        board = Board(3, 3, 1)
        board.generate_mines(0, 0)

        # Find a mine and reveal it
        mine_row, mine_col = next(iter(board.mine_positions))

        # Make sure the mine cell is not flagged
        if board.cells[mine_row][mine_col].is_flagged:
            board.flag_cell(mine_row, mine_col)  # Unflag it first

        board.reveal_cell(mine_row, mine_col)

        assert board.check_lose_condition() is True

    def test_lose_condition_not_met(self):
        """Test lose condition when no mines are revealed."""
        board = Board(3, 3, 1)
        board.generate_mines(0, 0)

        # Reveal a non-mine cell
        for row in range(3):
            for col in range(3):
                if not board.cells[row][col].is_mine:
                    board.reveal_cell(row, col)
                    break
            else:
                continue
            break

        assert board.check_lose_condition() is False


class TestAutoExpansion:
    """Test auto-expansion functionality."""

    def test_expand_with_correct_flags(self):
        """Test expansion when correct number of flags are placed."""
        board = Board(5, 5, 4)
        board.generate_mines(0, 0)

        # Find a cell with 2 adjacent mines
        target_cell = None
        for row in range(5):
            for col in range(5):
                if board.cells[row][col].adjacent_mines == 2 and not board.cells[row][col].is_mine:
                    target_cell = (row, col)
                    break
            if target_cell:
                break

        if target_cell:
            row, col = target_cell
            # Reveal the cell first
            board.reveal_cell(row, col)

            # Find and flag the 2 adjacent mines
            adjacent_positions = [(r, c) for r in range(5) for c in range(5)
                                if abs(r - row) <= 1 and abs(c - col) <= 1 and (r, c) != (row, col)]

            flagged_count = 0
            for adj_row, adj_col in adjacent_positions:
                if board.cells[adj_row][adj_col].is_mine:
                    board.flag_cell(adj_row, adj_col)
                    flagged_count += 1

            assert flagged_count == 2

            # Now expand
            initial_revealed = board.revealed_count
            expanded = board.expand_adjacent_cells(row, col)
            assert len(expanded) > 0  # Should reveal some cells

    def test_expand_with_incorrect_flags(self):
        """Test expansion fails when incorrect number of flags are placed."""
        board = Board(3, 3, 2)
        board.generate_mines(0, 0)

        # Find a cell with 2 adjacent mines
        target_cell = None
        for row in range(3):
            for col in range(3):
                if board.cells[row][col].adjacent_mines == 2 and not board.cells[row][col].is_mine:
                    target_cell = (row, col)
                    break
            if target_cell:
                break

        if target_cell:
            row, col = target_cell
            # Reveal the cell first
            board.reveal_cell(row, col)

            # Flag only 1 mine (incorrect number)
            adjacent_positions = [(r, c) for r in range(3) for c in range(3)
                                if abs(r - row) <= 1 and abs(c - col) <= 1 and (r, c) != (row, col)]

            for adj_row, adj_col in adjacent_positions:
                if board.cells[adj_row][adj_col].is_mine:
                    board.flag_cell(adj_row, adj_col)
                    break  # Only flag one

            # Try to expand
            initial_revealed = board.revealed_count
            expanded = board.expand_adjacent_cells(row, col)
            assert len(expanded) == 0  # Should not expand
            assert board.revealed_count == initial_revealed


class TestPositionValidation:
    """Test position validation."""

    def test_valid_position(self):
        """Test valid position access."""
        board = Board(5, 5, 1)
        cell = board.get_cell(2, 2)
        assert cell.row == 2
        assert cell.col == 2

    def test_invalid_row_too_low(self):
        """Test invalid row (too low)."""
        board = Board(5, 5, 1)
        with pytest.raises(ValueError):
            board.get_cell(-1, 2)

    def test_invalid_row_too_high(self):
        """Test invalid row (too high)."""
        board = Board(5, 5, 1)
        with pytest.raises(ValueError):
            board.get_cell(5, 2)

    def test_invalid_col_too_low(self):
        """Test invalid column (too low)."""
        board = Board(5, 5, 1)
        with pytest.raises(ValueError):
            board.get_cell(2, -1)

    def test_invalid_col_too_high(self):
        """Test invalid column (too high)."""
        board = Board(5, 5, 1)
        with pytest.raises(ValueError):
            board.get_cell(2, 5)
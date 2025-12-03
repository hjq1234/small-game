"""Integration tests for game flow scenarios."""

import pytest
from src.game.game_state import create_game_session, GameState
from src.game.difficulty import DifficultyPreset


class TestGameFlow:
    """Test complete game flow scenarios."""

    def test_complete_beginner_game_win(self):
        """Test completing a beginner game by winning."""
        # Create beginner game
        session = create_game_session("beginner")
        board = session.board

        # Start game
        session.start_game()
        assert session.state == GameState.PLAYING

        # Make first click to generate mines (click top-left corner)
        session.make_move(0, 0, 'reveal')

        # Find all safe cells (non-mines)
        safe_cells = []
        for row in range(board.height):
            for col in range(board.width):
                if not board.cells[row][col].is_mine:
                    safe_cells.append((row, col))

        # Reveal all safe cells to win, but skip already revealed ones
        for row, col in safe_cells:
            if not board.cells[row][col].is_revealed:
                success = session.make_move(row, col, 'reveal')
                if session.state in [GameState.WON, GameState.LOST]:
                    break

        # Game should be won
        assert session.state == GameState.WON
        assert session.is_game_over() is True

    def test_complete_beginner_game_loss(self):
        """Test losing a beginner game by hitting a mine."""
        # Create beginner game
        session = create_game_session("beginner")
        board = session.board

        # Start game
        session.start_game()

        # Make first click to generate mines (click top-left corner)
        session.make_move(0, 0, 'reveal')

        # Find a mine and reveal it
        mine_cells = []
        for row in range(board.height):
            for col in range(board.width):
                if board.cells[row][col].is_mine:
                    mine_cells.append((row, col))

        assert len(mine_cells) > 0

        # Reveal a mine to lose
        row, col = mine_cells[0]
        success = session.make_move(row, col, 'reveal')
        assert success is True

        # Game should be lost
        assert session.state == GameState.LOST
        assert session.is_game_over() is True

    def test_flag_and_reveal_flow(self):
        """Test flagging mines and revealing safe cells."""
        # Create beginner game
        session = create_game_session("beginner")
        board = session.board

        # Start game
        session.start_game()

        # Make first click to generate mines (click top-left corner)
        session.make_move(0, 0, 'reveal')

        # Find a mine and flag it
        mine_cells = []
        for row in range(board.height):
            for col in range(board.width):
                if board.cells[row][col].is_mine:
                    mine_cells.append((row, col))

        # Flag first mine
        mine_row, mine_col = mine_cells[0]
        success = session.make_move(mine_row, mine_col, 'flag')
        assert success is True
        assert board.cells[mine_row][mine_col].is_flagged is True

        # Find a hidden safe cell to reveal
        safe_cell = None
        for row in range(board.height):
            for col in range(board.width):
                if (not board.cells[row][col].is_mine and
                    board.cells[row][col].is_hidden):
                    safe_cell = (row, col)
                    break
            if safe_cell:
                break

        # Reveal safe cell
        safe_row, safe_col = safe_cell
        success = session.make_move(safe_row, safe_col, 'reveal')
        assert success is True
        assert board.cells[safe_row][safe_col].is_revealed is True

        # Game should still be playing
        assert session.state == GameState.PLAYING

    def test_auto_expansion_flow(self):
        """Test auto-expansion functionality."""
        # Create beginner game
        session = create_game_session("beginner")
        board = session.board

        # Start game
        session.start_game()

        # Find a cell with adjacent mines
        target_cell = None
        for row in range(board.height):
            for col in range(board.width):
                if (not board.cells[row][col].is_mine and
                    board.cells[row][col].adjacent_mines > 0):
                    target_cell = (row, col)
                    break
            if target_cell:
                break

        if target_cell:
            row, col = target_cell
            adjacent_mines = board.cells[row][col].adjacent_mines

            # Reveal the cell first
            session.make_move(row, col, 'reveal')

            # Flag all adjacent mines
            flagged_count = 0
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue
                    adj_row, adj_col = row + dr, col + dc
                    if (0 <= adj_row < board.height and
                        0 <= adj_col < board.width and
                        board.cells[adj_row][adj_col].is_mine):
                        session.make_move(adj_row, adj_col, 'flag')
                        flagged_count += 1

            # If we flagged the correct number of mines, try expansion
            if flagged_count == adjacent_mines:
                # Expansion should work
                expanded = session.expand_adjacent(row, col)
                assert expanded is True  # Should return True if any cells expanded

    def test_pause_resume_flow(self):
        """Test pause and resume functionality."""
        # Create beginner game
        session = create_game_session("beginner")

        # Start game
        session.start_game()
        assert session.state == GameState.PLAYING

        # Pause game
        session.pause_game()
        assert session.state == GameState.PAUSED

        # Resume game
        session.resume_game()
        assert session.state == GameState.PLAYING

    def test_reset_game_flow(self):
        """Test game reset functionality."""
        # Create beginner game
        session = create_game_session("beginner")

        # Start game and make some moves
        session.start_game()
        session.make_move(0, 0, 'reveal')  # First click - generates mines

        # Find a mine to flag
        mine_cell = None
        for row in range(session.board.height):
            for col in range(session.board.width):
                if session.board.cells[row][col].is_mine:
                    mine_cell = (row, col)
                    break
            if mine_cell:
                break

        session.make_move(mine_cell[0], mine_cell[1], 'flag')  # Flag a mine

        # Check that moves were made
        assert session.moves_count > 0
        assert session.flags_used > 0

        # Reset game
        session.reset_game()

        # Check reset state
        assert session.state == GameState.NEW
        assert session.moves_count == 0
        assert session.flags_used == 0
        assert session.board.revealed_count == 0

    def test_custom_difficulty_flow(self):
        """Test custom difficulty game flow."""
        # Create custom game
        session = create_game_session("custom", width=15, height=10, mines=20)

        # Verify custom settings
        assert session.difficulty.name == "Custom"
        assert session.board.width == 15
        assert session.board.height == 10
        assert session.board.mine_count == 20

        # Start game
        session.start_game()
        assert session.state == GameState.PLAYING

    def test_invalid_move_handling(self):
        """Test handling of invalid moves."""
        # Create beginner game
        session = create_game_session("beginner")
        session.start_game()

        # Try to reveal a flagged cell
        board = session.board
        board.cells[0][0].flag()

        # This should fail
        success = session.make_move(0, 0, 'reveal')
        assert success is False

        # Try to flag a revealed cell
        board.cells[1][1].reveal()
        success = session.make_move(1, 1, 'flag')
        assert success is False

        # Game should still be playing
        assert session.state == GameState.PLAYING

    def test_game_statistics(self):
        """Test game statistics tracking."""
        # Create beginner game
        session = create_game_session("beginner")
        session.start_game()

        # Make first click to generate mines
        session.make_move(0, 0, 'reveal')

        # Find a mine to flag
        mine_cell = None
        for row in range(session.board.height):
            for col in range(session.board.width):
                if session.board.cells[row][col].is_mine:
                    mine_cell = (row, col)
                    break
            if mine_cell:
                break

        # Flag a mine
        session.make_move(mine_cell[0], mine_cell[1], 'flag')

        # Get statistics
        stats = session.get_statistics()

        # Verify statistics
        assert stats['difficulty'] == 'Beginner'
        assert stats['board_width'] == 9
        assert stats['board_height'] == 9
        assert stats['mine_count'] == 10
        assert stats['state'] == 'playing'
        assert stats['moves_count'] == 1  # Only flag counts as move
        assert stats['flags_used'] == 1
        assert stats['duration'] is not None
        assert 'start_time' in stats
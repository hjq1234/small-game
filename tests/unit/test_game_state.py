"""Unit tests for GameSession and game state management."""

import pytest
from datetime import datetime
from src.game.game_state import GameSession, GameState, create_game_session
from src.game.difficulty import DifficultyPreset


class TestGameSession:
    """Test GameSession functionality."""

    def test_game_session_creation(self):
        """Test game session creation."""
        difficulty = DifficultyPreset.BEGINNER.level
        session = GameSession(difficulty)

        assert session.id is not None
        assert session.difficulty == difficulty
        assert session.state == GameState.NEW
        assert session.start_time is None
        assert session.end_time is None
        assert session.moves_count == 0
        assert session.flags_used == 0

    def test_game_session_with_custom_id(self):
        """Test game session creation with custom ID."""
        difficulty = DifficultyPreset.BEGINNER.level
        custom_id = "test-session-123"
        session = GameSession(difficulty, custom_id)

        assert session.id == custom_id

    def test_start_game(self):
        """Test starting a game."""
        difficulty = DifficultyPreset.BEGINNER.level
        session = GameSession(difficulty)

        assert session.state == GameState.NEW
        session.start_game()
        assert session.state == GameState.PLAYING
        assert session.start_time is not None

    def test_start_game_already_playing(self):
        """Test starting a game that's already playing."""
        difficulty = DifficultyPreset.BEGINNER.level
        session = GameSession(difficulty)
        session.start_game()

        # Starting again should not change state
        original_start = session.start_time
        session.start_game()
        assert session.state == GameState.PLAYING
        assert session.start_time == original_start

    def test_make_reveal_move(self):
        """Test making a reveal move."""
        difficulty = DifficultyPreset.BEGINNER.level
        session = GameSession(difficulty)
        session.start_game()

        # Make a reveal move
        success = session.make_move(0, 0, 'reveal')
        assert success is True
        assert session.moves_count == 1
        assert session.board.cells[0][0].is_revealed is True

    def test_make_flag_move(self):
        """Test making a flag move."""
        difficulty = DifficultyPreset.BEGINNER.level
        session = GameSession(difficulty)
        session.start_game()

        # Make a flag move
        success = session.make_move(0, 0, 'flag')
        assert success is True
        assert session.flags_used == 1
        assert session.board.cells[0][0].is_flagged is True

    def test_make_move_not_playing(self):
        """Test making a move when not playing."""
        difficulty = DifficultyPreset.BEGINNER.level
        session = GameSession(difficulty)
        # Game not started

        # Should start the game automatically when making first move
        success = session.make_move(0, 0, 'reveal')
        assert success is True
        assert session.state == GameState.PLAYING
        assert session.moves_count == 1

    def test_make_move_invalid_action(self):
        """Test making a move with invalid action."""
        difficulty = DifficultyPreset.BEGINNER.level
        session = GameSession(difficulty)
        session.start_game()

        # Invalid action should be handled gracefully
        success = session.make_move(0, 0, 'invalid')
        # Should return False for invalid action
        assert success is False

    def test_expand_adjacent(self):
        """Test expanding adjacent cells."""
        difficulty = DifficultyPreset.BEGINNER.level
        session = GameSession(difficulty)
        session.start_game()

        # Find a cell to expand
        for row in range(difficulty.height):
            for col in range(difficulty.width):
                if session.board.cells[row][col].adjacent_mines > 0:
                    # Flag adjacent mines first
                    adjacent_positions = []
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue
                            adj_row, adj_col = row + dr, col + dc
                            if (0 <= adj_row < difficulty.height and
                                0 <= adj_col < difficulty.width):
                                if session.board.cells[adj_row][adj_col].is_mine:
                                    session.board.flag_cell(adj_row, adj_col)

                    # Now expand
                    success = session.expand_adjacent(row, col)
                    assert isinstance(success, bool)
                    return

        # If no suitable cell found, skip test
        pytest.skip("No suitable cell found for expansion test")

    def test_expand_adjacent_not_playing(self):
        """Test expanding when not playing."""
        difficulty = DifficultyPreset.BEGINNER.level
        session = GameSession(difficulty)
        # Game not started

        with pytest.raises(ValueError, match="Cannot expand in state"):
            session.expand_adjacent(0, 0)

    def test_pause_and_resume(self):
        """Test pausing and resuming game."""
        difficulty = DifficultyPreset.BEGINNER.level
        session = GameSession(difficulty)
        session.start_game()

        assert session.state == GameState.PLAYING

        session.pause_game()
        assert session.state == GameState.PAUSED

        session.resume_game()
        assert session.state == GameState.PLAYING

    def test_pause_not_playing(self):
        """Test pausing when not playing."""
        difficulty = DifficultyPreset.BEGINNER.level
        session = GameSession(difficulty)

        # Should not change state
        session.pause_game()
        assert session.state == GameState.NEW

    def test_resume_not_paused(self):
        """Test resuming when not paused."""
        difficulty = DifficultyPreset.BEGINNER.level
        session = GameSession(difficulty)
        session.start_game()

        # Should not change state
        session.resume_game()
        assert session.state == GameState.PLAYING

    def test_get_game_duration(self):
        """Test getting game duration."""
        difficulty = DifficultyPreset.BEGINNER.level
        session = GameSession(difficulty)

        # Before start
        assert session.get_game_duration() is None

        # After start
        session.start_game()
        duration = session.get_game_duration()
        assert duration is not None
        assert duration >= 0

    def test_get_statistics(self):
        """Test getting game statistics."""
        difficulty = DifficultyPreset.BEGINNER.level
        session = GameSession(difficulty)
        session.start_game()
        session.make_move(0, 0, 'reveal')

        stats = session.get_statistics()

        assert stats['session_id'] == session.id
        assert stats['difficulty'] == difficulty.name
        assert stats['board_width'] == difficulty.width
        assert stats['board_height'] == difficulty.height
        assert stats['mine_count'] == difficulty.mines
        assert stats['state'] == GameState.PLAYING.value
        assert stats['moves_count'] == 1
        assert stats['flags_used'] == 0
        assert stats['revealed_count'] >= 1  # May expand if adjacent_mines == 0
        assert stats['flagged_count'] == 0
        assert stats['duration'] is not None
        assert 'start_time' in stats
        assert 'end_time' not in stats  # Game not over

    def test_is_game_over(self):
        """Test game over check."""
        difficulty = DifficultyPreset.BEGINNER.level
        session = GameSession(difficulty)

        # New game
        assert session.is_game_over() is False

        # Playing game
        session.start_game()
        assert session.is_game_over() is False

        # Won game
        session.state = GameState.WON
        assert session.is_game_over() is True

        # Lost game
        session.state = GameState.LOST
        assert session.is_game_over() is True

    def test_is_game_active(self):
        """Test game active check."""
        difficulty = DifficultyPreset.BEGINNER.level
        session = GameSession(difficulty)

        # New game
        assert session.is_game_active() is False

        # Playing game
        session.start_game()
        assert session.is_game_active() is True

        # Paused game
        session.pause_game()
        assert session.is_game_active() is True

        # Won game
        session.state = GameState.WON
        assert session.is_game_active() is False

    def test_reset_game(self):
        """Test resetting game."""
        difficulty = DifficultyPreset.BEGINNER.level
        session = GameSession(difficulty)
        session.start_game()
        session.make_move(0, 0, 'reveal')

        # Reset
        session.reset_game()

        assert session.state == GameState.NEW
        assert session.start_time is None
        assert session.end_time is None
        assert session.moves_count == 0
        assert session.flags_used == 0
        assert session.board.revealed_count == 0


class TestGameSessionCreation:
    """Test game session creation helper function."""

    def test_create_game_session_beginner(self):
        """Test creating beginner game session."""
        session = create_game_session("beginner")
        assert session.difficulty == DifficultyPreset.BEGINNER.level

    def test_create_game_session_intermediate(self):
        """Test creating intermediate game session."""
        session = create_game_session("intermediate")
        assert session.difficulty == DifficultyPreset.INTERMEDIATE.level

    def test_create_game_session_advanced(self):
        """Test creating advanced game session."""
        session = create_game_session("advanced")
        assert session.difficulty == DifficultyPreset.ADVANCED.level

    def test_create_game_session_custom(self):
        """Test creating custom game session."""
        session = create_game_session("custom", width=20, height=15, mines=30)
        assert session.difficulty.name == "Custom"
        assert session.difficulty.width == 20
        assert session.difficulty.height == 15
        assert session.difficulty.mines == 30

    def test_create_game_session_invalid_difficulty(self):
        """Test creating game session with invalid difficulty."""
        with pytest.raises(ValueError):
            create_game_session("invalid")

    def test_create_game_session_invalid_custom(self):
        """Test creating game session with invalid custom settings."""
        with pytest.raises(ValueError):
            create_game_session("custom", width=5, height=5, mines=30)  # Too many mines
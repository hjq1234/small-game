"""Game session and state management for minesweeper game."""

import uuid
from datetime import datetime
from enum import Enum
from typing import Optional
from .board import Board
from .difficulty import DifficultyLevel, DifficultyPreset


class GameState(Enum):
    """Possible game states."""
    NEW = "new"              # Game created, no moves made
    PLAYING = "playing"      # Game in progress
    PAUSED = "paused"        # Game paused
    WON = "won"              # All non-mine cells revealed
    LOST = "lost"            # Mine clicked


class GameSession:
    """Represents a game session with state tracking."""

    def __init__(self, difficulty: DifficultyLevel, session_id: Optional[str] = None):
        """Initialize a new game session.

        Args:
            difficulty: Difficulty level configuration
            session_id: Optional session ID (auto-generated if not provided)
        """
        self.id = session_id or str(uuid.uuid4())
        self.difficulty = difficulty
        self.board = Board(difficulty.width, difficulty.height, difficulty.mines)
        self.state = GameState.NEW
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None
        self.moves_count = 0
        self.flags_used = 0

    def start_game(self) -> None:
        """Start the game session."""
        if self.state == GameState.NEW:
            self.state = GameState.PLAYING
            self.start_time = datetime.now()

    def make_move(self, row: int, col: int, action: str) -> bool:
        """Make a move in the game.

        Args:
            row: Row position
            col: Column position
            action: Action type ('reveal' or 'flag')

        Returns:
            True if move was successful

        Raises:
            ValueError: If game is not in playing state
        """
        if self.state not in (GameState.PLAYING, GameState.NEW):
            raise ValueError(f"Cannot make move in state {self.state.value}")

        # Start game if it's new
        if self.state == GameState.NEW:
            self.start_game()

        success = False

        if action == 'reveal':
            success = self.board.reveal_cell(row, col)
            if success:
                self.moves_count += 1

                # Check lose condition
                if self.board.check_lose_condition():
                    self.state = GameState.LOST
                    self.end_time = datetime.now()

                # Check win condition
                elif self.board.check_win_condition():
                    self.state = GameState.WON
                    self.end_time = datetime.now()

        elif action == 'flag':
            success = self.board.flag_cell(row, col)
            if success:
                self.flags_used += 1

        return success

    def expand_adjacent(self, row: int, col: int) -> bool:
        """Auto-expand adjacent cells.

        Args:
            row: Row position of revealed cell
            col: Column position of revealed cell

        Returns:
            True if any cells were expanded

        Raises:
            ValueError: If game is not in playing state
        """
        if self.state != GameState.PLAYING:
            raise ValueError(f"Cannot expand in state {self.state.value}")

        expanded = self.board.expand_adjacent_cells(row, col)

        if expanded:
            self.moves_count += 1

            # Check win condition after expansion
            if self.board.check_win_condition():
                self.state = GameState.WON
                self.end_time = datetime.now()

        return len(expanded) > 0

    def pause_game(self) -> None:
        """Pause the game."""
        if self.state == GameState.PLAYING:
            self.state = GameState.PAUSED

    def resume_game(self) -> None:
        """Resume the game."""
        if self.state == GameState.PAUSED:
            self.state = GameState.PLAYING

    def get_game_duration(self) -> Optional[float]:
        """Get game duration in seconds.

        Returns:
            Game duration in seconds, or None if game hasn't started
        """
        if self.start_time is None:
            return None

        end_time = self.end_time or datetime.now()
        return (end_time - self.start_time).total_seconds()

    def get_statistics(self) -> dict:
        """Get game statistics.

        Returns:
            Dictionary with game statistics
        """
        stats = {
            'session_id': self.id,
            'difficulty': self.difficulty.name,
            'board_width': self.board.width,
            'board_height': self.board.height,
            'mine_count': self.board.mine_count,
            'state': self.state.value,
            'moves_count': self.moves_count,
            'flags_used': self.flags_used,
            'revealed_count': self.board.revealed_count,
            'flagged_count': self.board.flagged_count,
            'duration': self.get_game_duration(),
        }

        if self.start_time:
            stats['start_time'] = self.start_time.isoformat()
        if self.end_time:
            stats['end_time'] = self.end_time.isoformat()

        return stats

    def is_game_over(self) -> bool:
        """Check if the game is over."""
        return self.state in (GameState.WON, GameState.LOST)

    def is_game_active(self) -> bool:
        """Check if the game is active (playing or paused)."""
        return self.state in (GameState.PLAYING, GameState.PAUSED)

    def reset_game(self) -> None:
        """Reset the game to initial state."""
        self.board = Board(self.difficulty.width, self.difficulty.height, self.difficulty.mines)
        self.state = GameState.NEW
        self.start_time = None
        self.end_time = None
        self.moves_count = 0
        self.flags_used = 0

    def __str__(self) -> str:
        """String representation of the game session."""
        return (f"GameSession(id={self.id[:8]}..., difficulty={self.difficulty.name}, "
                f"state={self.state.value}, moves={self.moves_count})")


def create_game_session(difficulty_name: str = "beginner", **custom_settings) -> GameSession:
    """Create a new game session.

    Args:
        difficulty_name: Difficulty level name ('beginner', 'intermediate', 'advanced', or 'custom')
        **custom_settings: Custom settings if difficulty_name is 'custom'

    Returns:
        New game session

    Raises:
        ValueError: If difficulty name is invalid or custom settings are invalid
    """
    if difficulty_name.lower() == "custom":
        from .validator import validate_board_settings

        width = custom_settings.get("width", 9)
        height = custom_settings.get("height", 9)
        mines = custom_settings.get("mines", 10)

        validate_board_settings(width, height, mines)
        difficulty = DifficultyLevel("Custom", width, height, mines)
    else:
        difficulty = DifficultyPreset.get_by_name(difficulty_name)

    return GameSession(difficulty)
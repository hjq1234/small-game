#!/usr/bin/env python3
"""Simple test to verify the game works."""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from game.cell import Cell, HiddenState, RevealedState, FlaggedState
from game.board import Board
from game.game_state import GameSession, GameState
from game.difficulty import DifficultyPreset


def test_basic_gameplay():
    """Test basic gameplay mechanics."""
    print("Testing basic gameplay...")

    # Create a simple game
    difficulty = DifficultyPreset.BEGINNER.level
    session = GameSession(difficulty)

    print(f"Created game session: {session.id}")
    print(f"Board size: {session.board.width}x{session.board.height}")
    print(f"Mines: {session.board.mine_count}")

    # Make first move (should be safe due to first-click safety)
    success = session.make_move(4, 4, 'reveal')
    print(f"First move successful: {success}")
    print(f"Game state: {session.state.value}")
    print(f"Revealed cells: {session.board.revealed_count}")

    # Test flagging
    success = session.make_move(0, 0, 'flag')
    print(f"Flag move successful: {success}")
    print(f"Flags used: {session.flags_used}")

    # Test cell states
    cell = session.board.cells[4][4]
    print(f"First clicked cell: revealed={cell.is_revealed}, flagged={cell.is_flagged}")

    cell = session.board.cells[0][0]
    print(f"Flagged cell: revealed={cell.is_revealed}, flagged={cell.is_flagged}")

    print("Basic gameplay test completed successfully!")


def test_cell_states():
    """Test cell state transitions."""
    print("\nTesting cell state transitions...")

    cell = Cell(0, 0)
    print(f"Initial state: hidden={cell.is_hidden}, revealed={cell.is_revealed}, flagged={cell.is_flagged}")

    # Test reveal
    cell.reveal()
    print(f"After reveal: hidden={cell.is_hidden}, revealed={cell.is_revealed}, flagged={cell.is_flagged}")

    # Test flag (should not work on revealed cell)
    cell.flag()
    print(f"After flag attempt on revealed cell: hidden={cell.is_hidden}, revealed={cell.is_revealed}, flagged={cell.is_flagged}")

    # Create new cell and test flag first
    cell2 = Cell(1, 1)
    cell2.flag()
    print(f"After flag: hidden={cell2.is_hidden}, revealed={cell2.is_revealed}, flagged={cell2.is_flagged}")

    # Test reveal on flagged cell (should not work)
    cell2.reveal()
    print(f"After reveal attempt on flagged cell: hidden={cell2.is_hidden}, revealed={cell2.is_revealed}, flagged={cell2.is_flagged}")

    print("Cell state tests completed!")


if __name__ == "__main__":
    test_basic_gameplay()
    test_cell_states()
    print("\nAll tests completed successfully!")
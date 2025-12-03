#!/usr/bin/env python3
"""Direct runner for the game window to test the UI."""

import pygame
import sys
import os

# Add src to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.game_window import GameWindow


def main():
    """Run the game directly."""
    try:
        game = GameWindow()
        game.start_new_game("beginner")
        print("Game window created successfully!")
        print("Press any key to start the game loop...")
        input()
        # game.run()  # Uncomment to actually run the game
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
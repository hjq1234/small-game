"""Main entry point for the Minesweeper game."""

import sys
import argparse
from ui.game_window import GameWindow
from game.difficulty import DifficultyPreset

# Add the src directory to Python path for proper imports
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Minesweeper Game')

    parser.add_argument(
        '--difficulty',
        choices=['beginner', 'intermediate', 'advanced', 'custom'],
        default='beginner',
        help='Game difficulty level (default: beginner)'
    )

    parser.add_argument(
        '--width',
        type=int,
        default=9,
        help='Custom board width (default: 9)'
    )

    parser.add_argument(
        '--height',
        type=int,
        default=9,
        help='Custom board height (default: 9)'
    )

    parser.add_argument(
        '--mines',
        type=int,
        default=10,
        help='Custom number of mines (default: 10)'
    )

    parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable debug mode'
    )

    parser.add_argument(
        '--profile',
        action='store_true',
        help='Enable performance profiling'
    )

    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose output'
    )

    return parser.parse_args()


def main():
    """Main entry point."""
    args = parse_arguments()

    try:
        if args.verbose:
            print(f"Starting Minesweeper with difficulty: {args.difficulty}")
            if args.difficulty == 'custom':
                print(f"Custom settings: {args.width}x{args.height} with {args.mines} mines")

        # Create and run the game
        game = GameWindow()

        if args.difficulty == 'custom':
            # Validate custom settings
            from game.validator import validate_board_settings
            try:
                validate_board_settings(args.width, args.height, args.mines)
                game.start_new_game('custom', width=args.width, height=args.height, mines=args.mines)
            except ValueError as e:
                print(f"Invalid custom settings: {e}")
                print("Starting with beginner difficulty instead.")
                game.start_new_game('beginner')
        else:
            game.start_new_game(args.difficulty)

        # Run the game
        if args.profile:
            import cProfile
            import pstats

            profiler = cProfile.Profile()
            profiler.enable()

            try:
                game.run()
            finally:
                profiler.disable()

                # Save profiling results
                stats = pstats.Stats(profiler)
                stats.sort_stats('cumulative')
                stats.print_stats(20)  # Top 20 functions
        else:
            game.run()

    except KeyboardInterrupt:
        print("\nGame interrupted by user")
        sys.exit(0)
    except Exception as e:
        if args.debug:
            import traceback
            traceback.print_exc()
        else:
            print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
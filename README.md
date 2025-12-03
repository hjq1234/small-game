# Minesweeper Game

A classic Minesweeper game implementation in Python using Pygame.

## Features

- **Classic Gameplay**: Left-click to reveal cells, right-click to flag mines
- **First-Click Safety**: First click is always safe from mines
- **Auto-Expansion**: Automatically reveals adjacent empty cells
- **Flag System**: Right-click to flag suspected mines
- **Difficulty Levels**: Beginner, Intermediate, and Advanced presets
- **Custom Boards**: Create custom board sizes and mine counts
- **Double-Click Expansion**: Double-click revealed cells to auto-expand when correct flags are placed
- **Game Statistics**: Track moves, time, and game state
- **Pause/Resume**: Pause and resume games
- **Comprehensive Testing**: Full unit and integration test coverage

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Basic Usage

```bash
# Run with default beginner difficulty
python run_game.py

# Run with specific difficulty
python run_game.py --difficulty intermediate

# Run with custom settings
python run_game.py --difficulty custom --width 20 --height 15 --mines 30
```

**Difficulty Levels:**
- `beginner`: 9×9 board, 10 mines
- `intermediate`: 16×16 board, 40 mines
- `advanced`: 30×16 board, 99 mines
- `custom`: Define your own size and mine count

**In-Game Controls:**
- Press **1** to switch to Beginner difficulty
- Press **2** to switch to Intermediate difficulty
- Press **3** to switch to Advanced difficulty
- Current difficulty is displayed in the top-left corner

### Command Line Options

- `--difficulty`: Choose difficulty level (`beginner`, `intermediate`, `advanced`, `custom`)
- `--width`: Custom board width (9-30)
- `--height`: Custom board height (9-30)
- `--mines`: Custom number of mines
- `--debug`: Enable debug mode
- `--profile`: Enable performance profiling
- `--verbose`: Enable verbose output

### Controls

- **Left Click**: Reveal cell
- **Right Click**: Flag/unflag cell
- **Double Click**: Auto-expand adjacent cells (when correct flags are placed)
- **Space**: Pause/resume game
- **R**: Restart current game
- **N**: New game with difficulty selection
- **1/2/3**: Quick select beginner/intermediate/advanced difficulty
- **ESC**: Quit game

## Project Structure

```
src/
├── game/                 # Core game logic
│   ├── __init__.py
│   ├── board.py         # Game board management
│   ├── cell.py          # Cell state and behavior
│   ├── game_state.py    # Game session management
│   ├── difficulty.py    # Difficulty configurations
│   └── validator.py     # Input validation
├── ui/                  # User interface
│   ├── __init__.py
│   ├── game_window.py   # Main game window
│   ├── cell_renderer.py # Cell visual rendering
│   ├── input_handler.py # Input processing
│   └── assets/          # Game assets (sprites, sounds)
├── main.py              # Application entry point
└── config.py            # Game configuration

tests/
├── unit/                # Unit tests
│   ├── test_cell.py     # Cell entity tests
│   ├── test_board.py    # Board entity tests
│   ├── test_game_state.py # Game state tests
│   ├── test_difficulty.py # Difficulty tests
│   └── test_validator.py # Validation tests
└── integration/         # Integration tests
    └── test_game_flow.py # Complete game flow tests
```

## Architecture

### Core Entities

- **Cell**: Individual game cell with state management (Hidden, Revealed, Flagged)
- **Board**: Game board with mine generation and cell relationships
- **GameSession**: Game state management and move tracking
- **DifficultyLevel**: Preset and custom difficulty configurations

### Key Features

- **State Pattern**: Cell states manage their own behavior and transitions
- **First-Click Safety**: Mines are generated after first click to ensure safety
- **Auto-Expansion**: Empty cells automatically reveal adjacent cells
- **Validation**: Comprehensive input validation for all game parameters
- **Testing**: 100+ unit and integration tests with high coverage

## Testing

Run the test suite:

```bash
# Run all tests
python -m pytest tests/ -v

# Run unit tests only
python -m pytest tests/unit/ -v

# Run integration tests only
python -m pytest tests/integration/ -v

# Run with coverage
python -m pytest tests/ --cov=src --cov-report=html
```

## Development

### Code Style

- Follows Python 3.13 best practices
- Type hints throughout the codebase
- Comprehensive docstrings
- Single-purpose functions and classes
- Clear separation of concerns

### Performance

- Optimized for 60 FPS gameplay
- Efficient mine generation algorithms
- Memory-efficient cell state management
- Fast board rendering and input processing

## Requirements

- Python 3.13+
- Pygame 2.5.0+
- pytest 7.4.0+ (for testing)

## License

This project is part of the small-game collection and follows the project's development guidelines.
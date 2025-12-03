# Data Model: Minesweeper Game

**Date**: 2025-12-02
**Feature**: Minesweeper Game

## Entity Definitions

### Cell Entity

**Purpose**: Represents an individual cell on the game board

**Attributes**:
- `row: int` - Row position (0-indexed)
- `col: int` - Column position (0-indexed)
- `is_mine: bool` - Whether this cell contains a mine
- `is_revealed: bool` - Whether this cell has been revealed
- `is_flagged: bool` - Whether this cell has been flagged
- `adjacent_mines: int` - Number of adjacent mines (0-8)
- `state: CellState` - Current cell state (HiddenState, RevealedState, FlaggedState)

**State Transitions**:
- Hidden → Revealed: When player clicks to reveal
- Hidden → Flagged: When player right-clicks to flag
- Flagged → Hidden: When player right-clicks to unflag
- Flagged → Revealed: Not allowed (must unflag first)

**Validation Rules**:
- Cannot reveal a flagged cell
- Cannot flag a revealed cell
- Adjacent mines must be 0-8

### Board Entity

**Purpose**: Manages the game board state and cell relationships

**Attributes**:
- `width: int` - Number of columns (9-30)
- `height: int` - Number of rows (9-30)
- `mine_count: int` - Total number of mines
- `cells: List[List[Cell]]` - 2D grid of cells
- `revealed_count: int` - Number of revealed cells
- `flagged_count: int` - Number of flagged cells
- `first_click: bool` - Whether first click has occurred

**Validation Rules**:
- Width: 9-30 cells
- Height: 9-30 cells
- Mine count: 1 to (width × height - 1)
- First click cannot be on a mine

**Business Rules**:
- Generate mines after first click to ensure safety
- Calculate adjacent mine counts for all cells
- Track revealed cells for win condition

### GameSession Entity

**Purpose**: Tracks the current game session state and progress

**Attributes**:
- `id: str` - Unique session identifier
- `difficulty: DifficultyLevel` - Selected difficulty level
- `board: Board` - Current game board
- `state: GameState` - Current game state
- `start_time: datetime` - Game start time
- `end_time: datetime` - Game end time (optional)
- `moves_count: int` - Total number of moves made
- `flags_used: int` - Number of flags placed

**State Machine**:
- NEW → PLAYING: After first cell click
- PLAYING → WON: All non-mine cells revealed
- PLAYING → LOST: Mine clicked
- Any → PAUSED: Player pauses game

### DifficultyLevel Entity

**Purpose**: Defines preset difficulty configurations

**Attributes**:
- `name: str` - Difficulty name ("Beginner", "Intermediate", "Advanced")
- `width: int` - Board width
- `height: int` - Board height
- `mine_count: int` - Number of mines
- `best_time: int` - Best completion time (optional)

**Predefined Levels**:
- Beginner: 9×9 board, 10 mines
- Intermediate: 16×16 board, 40 mines
- Advanced: 30×16 board, 99 mines

### CustomSettings Entity

**Purpose**: User-defined board configuration

**Attributes**:
- `width: int` - Custom board width (9-30)
- `height: int` - Custom board height (9-30)
- `mine_count: int` - Custom mine count

**Validation Rules**:
- Minimum board size: 9×9
- Maximum board size: 30×30
- Mine count: 1 to (width × height - 1)
- Reasonable mine density (typically 10-25%)

## Entity Relationships

```
GameSession (1) ──> (1) Board
     │                │
     │                └──> (width × height) Cell
     │
     └──> (1) DifficultyLevel or CustomSettings
```

**Relationship Details**:
- One GameSession has exactly one Board
- One Board contains many Cells (width × height)
- GameSession uses either a DifficultyLevel or CustomSettings
- Board manages all Cell state transitions

## State Management

### Cell States

```python
class CellState(ABC):
    @abstractmethod
    def reveal(self) -> CellState:
        pass

    @abstractmethod
    def flag(self) -> CellState:
        pass

    @abstractmethod
    def can_reveal(self) -> bool:
        pass

    @abstractmethod
    def can_flag(self) -> bool:
        pass

class HiddenState(CellState):
    def reveal(self) -> CellState:
        return RevealedState()

    def flag(self) -> CellState:
        return FlaggedState()

    def can_reveal(self) -> bool:
        return True

    def can_flag(self) -> bool:
        return True

class RevealedState(CellState):
    def reveal(self) -> CellState:
        return self  # Already revealed

    def flag(self) -> CellState:
        return self  # Cannot flag revealed cell

    def can_reveal(self) -> bool:
        return False

    def can_flag(self) -> bool:
        return False

class FlaggedState(CellState):
    def reveal(self) -> CellState:
        return self  # Cannot reveal flagged cell

    def flag(self) -> CellState:
        return HiddenState()  # Unflag

    def can_reveal(self) -> bool:
        return False

    def can_flag(self) -> bool:
        return True
```

### Game States

```python
class GameState(Enum):
    NEW = "new"              # Game created, no moves made
    PLAYING = "playing"      # Game in progress
    PAUSED = "paused"        # Game paused
    WON = "won"              # All non-mine cells revealed
    LOST = "lost"            # Mine clicked
```

## Data Validation

### Board Validation

```python
def validate_board_settings(width: int, height: int, mine_count: int) -> bool:
    """Validate board configuration parameters."""
    if not (9 <= width <= 30):
        raise ValueError(f"Width must be between 9 and 30, got {width}")

    if not (9 <= height <= 30):
        raise ValueError(f"Height must be between 9 and 30, got {height}")

    total_cells = width * height
    if not (1 <= mine_count < total_cells):
        raise ValueError(f"Mine count must be between 1 and {total_cells - 1}, got {mine_count}")

    # Check mine density (max 25% for playability)
    mine_density = mine_count / total_cells
    if mine_density > 0.25:
        raise ValueError(f"Mine density too high: {mine_density:.1%}, max 25%")

    return True
```

### Move Validation

```python
def validate_move(board: Board, row: int, col: int, action: str) -> bool:
    """Validate player move."""
    if not (0 <= row < board.height and 0 <= col < board.width):
        raise ValueError(f"Position ({row}, {col}) out of bounds")

    cell = board.cells[row][col]

    if action == "reveal":
        if not cell.can_reveal():
            raise InvalidMoveError(f"Cannot reveal cell at ({row}, {col})")

    elif action == "flag":
        if not cell.can_flag():
            raise InvalidMoveError(f"Cannot flag cell at ({row}, {col})")

    return True
```

## Data Persistence

### Session Data (Optional)

For future enhancements, session data could include:
- Game history and statistics
- Best completion times per difficulty
- Custom settings preferences
- Player achievements

### Serialization Format

```json
{
  "session_id": "uuid",
  "difficulty": "beginner|intermediate|advanced|custom",
  "board_width": 9,
  "board_height": 9,
  "mine_count": 10,
  "game_state": "new|playing|paused|won|lost",
  "start_time": "2025-12-02T10:00:00Z",
  "end_time": "2025-12-02T10:03:45Z",
  "moves_count": 25,
  "flags_used": 8,
  "board_data": {
    "mines": [[0, 1], [2, 3], ...],
    "revealed": [[0, 0], [1, 1], ...],
    "flagged": [[0, 2], [3, 4], ...]
  }
}
```

This data model provides a solid foundation for implementing the minesweeper game with clear entity relationships, comprehensive validation rules, and extensible state management.
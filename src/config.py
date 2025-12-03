"""Game configuration constants for Minesweeper."""

# Window settings
WINDOW_TITLE = "Minesweeper"
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
MIN_WINDOW_SIZE = (400, 300)

# Cell settings
CELL_SIZE = 20  # pixels
CELL_PADDING = 1
MIN_CELL_SIZE = 15
MAX_CELL_SIZE = 30

# Colors (RGB)
COLOR_HIDDEN = (192, 192, 192)      # Light gray
COLOR_REVEALED = (255, 255, 255)    # White
COLOR_MINE = (255, 0, 0)            # Red
COLOR_FLAG = (255, 255, 0)          # Yellow
COLOR_TEXT = (0, 0, 0)              # Black
COLOR_BORDER = (128, 128, 128)      # Dark gray
COLOR_BG_HOVER = (220, 220, 220)    # Light blue-gray for hover
COLOR_DROPDOWN_BG = (240, 240, 240) # Dropdown background

# Game colors for numbers
COLOR_NUMBER_1 = (0, 0, 255)          # Blue
COLOR_NUMBER_2 = (0, 128, 0)          # Green
COLOR_NUMBER_3 = (255, 0, 0)          # Red
COLOR_NUMBER_4 = (0, 0, 128)          # Dark blue
COLOR_NUMBER_5 = (128, 0, 0)          # Dark red
COLOR_NUMBER_6 = (0, 128, 128)        # Cyan
COLOR_NUMBER_7 = (0, 0, 0)            # Black
COLOR_NUMBER_8 = (128, 128, 128)      # Gray

# Timing
DOUBLE_CLICK_TIME = 300  # milliseconds
FPS_TARGET = 60
FPS_MIN = 30

# Board constraints
MIN_BOARD_WIDTH = 9
MAX_BOARD_WIDTH = 30
MIN_BOARD_HEIGHT = 9
MAX_BOARD_HEIGHT = 30
MAX_MINE_DENSITY = 0.25  # 25%

# Difficulty presets
DIFFICULTY_BEGINNER = {
    'name': 'Beginner',
    'width': 9,
    'height': 9,
    'mines': 10
}

DIFFICULTY_INTERMEDIATE = {
    'name': 'Intermediate',
    'width': 16,
    'height': 16,
    'mines': 40
}

DIFFICULTY_ADVANCED = {
    'name': 'Advanced',
    'width': 30,
    'height': 16,
    'mines': 99
}

# Font settings
FONT_SIZE_SMALL = 12
FONT_SIZE_MEDIUM = 16
FONT_SIZE_LARGE = 24

# Game states
GAME_STATE_NEW = "new"
GAME_STATE_PLAYING = "playing"
GAME_STATE_PAUSED = "paused"
GAME_STATE_WON = "won"
GAME_STATE_LOST = "lost"
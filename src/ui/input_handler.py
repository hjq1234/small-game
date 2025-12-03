"""Input handling for minesweeper game."""

import pygame
import time
from typing import Optional, Tuple, Callable


class InputHandler:
    """Handles mouse and keyboard input for the game."""

    def __init__(self):
        """Initialize the input handler."""
        self.last_click_time = 0
        self.double_click_threshold = 300  # milliseconds
        self.last_click_button = None
        self.last_click_pos = None

    def handle_events(self, event: pygame.event.Event) -> Optional[dict]:
        """Handle pygame events and return action information.

        Args:
            event: Pygame event to handle

        Returns:
            Dictionary with action information, or None if no relevant action
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            return self._handle_mouse_click(event)
        elif event.type == pygame.KEYDOWN:
            return self._handle_key_press(event)

        return None

    def _handle_mouse_click(self, event: pygame.event.Event) -> Optional[dict]:
        """Handle mouse click events.

        Args:
            event: Mouse button down event

        Returns:
            Action dictionary with type and position
        """
        current_time = time.time() * 1000  # Convert to milliseconds
        pos = event.pos
        button = event.button

        # Check for double click
        is_double_click = self._is_double_click(current_time, button, pos)

        # Update click tracking
        self.last_click_time = current_time
        self.last_click_button = button
        self.last_click_pos = pos

        # Determine action based on button and double-click
        if button == 1:  # Left click
            if is_double_click:
                return {
                    'type': 'double_click',
                    'position': pos,
                    'button': button
                }
            else:
                return {
                    'type': 'left_click',
                    'position': pos,
                    'button': button
                }
        elif button == 3:  # Right click
            return {
                'type': 'right_click',
                'position': pos,
                'button': button
            }

        return None

    def _handle_key_press(self, event: pygame.event.Event) -> Optional[dict]:
        """Handle keyboard events.

        Args:
            event: Key down event

        Returns:
            Action dictionary with key information
        """
        key = event.key

        # Game controls
        if key == pygame.K_SPACE:
            return {
                'type': 'pause_resume',
                'key': 'space'
            }
        elif key == pygame.K_r:
            return {
                'type': 'restart',
                'key': 'r'
            }
        elif key == pygame.K_n:
            return {
                'type': 'new_game',
                'key': 'n'
            }
        elif key == pygame.K_ESCAPE:
            return {
                'type': 'quit',
                'key': 'escape'
            }
        elif key == pygame.K_h or key == pygame.K_F1:
            return {
                'type': 'help',
                'key': 'help'
            }

        # Difficulty shortcuts
        elif key == pygame.K_1:
            return {
                'type': 'set_difficulty',
                'difficulty': 'beginner',
                'key': '1'
            }
        elif key == pygame.K_2:
            return {
                'type': 'set_difficulty',
                'difficulty': 'intermediate',
                'key': '2'
            }
        elif key == pygame.K_3:
            return {
                'type': 'set_difficulty',
                'difficulty': 'advanced',
                'key': '3'
            }

        return None

    def _is_double_click(self, current_time: float, button: int, pos: Tuple[int, int]) -> bool:
        """Check if this is a double click.

        Args:
            current_time: Current time in milliseconds
            button: Mouse button that was clicked
            pos: Mouse position

        Returns:
            True if this is a double click
        """
        if self.last_click_button is None:
            return False

        time_diff = current_time - self.last_click_time
        same_button = button == self.last_click_button
        same_position = self._is_same_position(pos, self.last_click_pos)

        return (time_diff <= self.double_click_threshold and
                same_button and
                same_position)

    def _is_same_position(self, pos1: Tuple[int, int], pos2: Tuple[int, int]) -> bool:
        """Check if two positions are the same (within tolerance).

        Args:
            pos1: First position
            pos2: Second position

        Returns:
            True if positions are the same
        """
        if pos1 is None or pos2 is None:
            return False

        tolerance = 5  # pixels
        return (abs(pos1[0] - pos2[0]) <= tolerance and
                abs(pos1[1] - pos2[1]) <= tolerance)

    def screen_to_grid(self, pos: Tuple[int, int], cell_size: int, offset_x: int = 0, offset_y: int = 0) -> Optional[Tuple[int, int]]:
        """Convert screen position to grid coordinates.

        Args:
            pos: Screen position (x, y)
            cell_size: Size of each cell in pixels
            offset_x: X offset of the grid
            offset_y: Y offset of the grid

        Returns:
            Grid coordinates (row, col) or None if outside grid
        """
        x, y = pos
        x -= offset_x
        y -= offset_y

        if x < 0 or y < 0:
            return None

        col = x // (cell_size + 1)  # +1 for border
        row = y // (cell_size + 1)

        return (row, col)

    def reset_click_tracking(self) -> None:
        """Reset click tracking for double-click detection."""
        self.last_click_time = 0
        self.last_click_button = None
        self.last_click_pos = None


class InputEvent:
    """Represents an input event with additional context."""

    def __init__(self, event_type: str, **kwargs):
        """Initialize input event.

        Args:
            event_type: Type of event
            **kwargs: Additional event data
        """
        self.type = event_type
        self.data = kwargs
        self.timestamp = time.time()

    def __str__(self) -> str:
        """String representation of the event."""
        return f"InputEvent(type={self.type}, data={self.data})"
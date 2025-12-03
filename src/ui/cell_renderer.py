"""Cell visual representation and rendering for minesweeper game."""

import pygame
from typing import Tuple, Optional
from game.cell import Cell
from config import (
    CELL_SIZE, CELL_PADDING, COLOR_HIDDEN, COLOR_REVEALED, COLOR_MINE,
    COLOR_FLAG, COLOR_TEXT, COLOR_BORDER, COLOR_NUMBER_1, COLOR_NUMBER_2,
    COLOR_NUMBER_3, COLOR_NUMBER_4, COLOR_NUMBER_5, COLOR_NUMBER_6,
    COLOR_NUMBER_7, COLOR_NUMBER_8, FONT_SIZE_MEDIUM
)


class CellRenderer:
    """Handles visual representation of individual cells."""

    def __init__(self, cell: Cell, x: int, y: int):
        """Initialize cell renderer.

        Args:
            cell: The cell to render
            x: X position on screen
            y: Y position on screen
        """
        self.cell = cell
        self.x = x
        self.y = y
        self.width = CELL_SIZE
        self.height = CELL_SIZE
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.font = None

    def set_font(self, font: pygame.font.Font) -> None:
        """Set the font for text rendering."""
        self.font = font

    def render(self, screen: pygame.Surface, game_over: bool = False) -> None:
        """Render the cell on the screen.

        Args:
            screen: Pygame screen surface
            game_over: Whether the game is over (reveals all mines)
        """
        # Draw cell background
        self._draw_background(screen)

        # Draw cell border
        self._draw_border(screen)

        # Draw cell content
        if self.cell.is_hidden and not game_over:
            self._draw_hidden_cell(screen)
        elif self.cell.is_flagged:
            self._draw_flag(screen)
        elif self.cell.is_revealed:
            self._draw_revealed_cell(screen, game_over)

    def _draw_background(self, screen: pygame.Surface) -> None:
        """Draw the cell background."""
        color = COLOR_HIDDEN if self.cell.is_hidden else COLOR_REVEALED
        pygame.draw.rect(screen, color, self.rect)

    def _draw_border(self, screen: pygame.Surface) -> None:
        """Draw the cell border."""
        pygame.draw.rect(screen, COLOR_BORDER, self.rect, 1)

    def _draw_hidden_cell(self, screen: pygame.Surface) -> None:
        """Draw a hidden cell (empty, just background)."""
        pass  # Background is already drawn

    def _draw_flag(self, screen: pygame.Surface) -> None:
        """Draw a flag on the cell."""
        # Draw flag pole
        pole_x = self.x + self.width // 3
        pole_top = self.y + self.height // 6
        pole_bottom = self.y + 5 * self.height // 6
        pygame.draw.line(screen, COLOR_TEXT, (pole_x, pole_top), (pole_x, pole_bottom), 2)

        # Draw flag
        flag_size = self.width // 3
        flag_rect = pygame.Rect(
            pole_x,
            self.y + self.height // 6,
            flag_size,
            flag_size
        )
        pygame.draw.rect(screen, COLOR_FLAG, flag_rect)
        pygame.draw.rect(screen, COLOR_TEXT, flag_rect, 1)

    def _draw_revealed_cell(self, screen: pygame.Surface, game_over: bool) -> None:
        """Draw a revealed cell."""
        if self.cell.is_mine:
            self._draw_mine(screen, game_over)
        elif self.cell.adjacent_mines > 0:
            self._draw_number(screen)

    def _draw_mine(self, screen: pygame.Surface, game_over: bool) -> None:
        """Draw a mine."""
        color = COLOR_MINE if game_over else COLOR_TEXT
        center_x = self.x + self.width // 2
        center_y = self.y + self.height // 2
        radius = self.width // 4

        # Draw mine as a circle
        pygame.draw.circle(screen, color, (center_x, center_y), radius)

        # Draw mine spikes (only if game is over or mine is revealed)
        if game_over or self.cell.is_revealed:
            spike_length = radius // 2
            for angle in range(0, 360, 45):
                rad_angle = angle * 3.14159 / 180
                spike_x = center_x + int(radius * 1.2 * pygame.math.Vector2(1, 0).rotate(angle).x)
                spike_y = center_y + int(radius * 1.2 * pygame.math.Vector2(1, 0).rotate(angle).y)
                end_x = center_x + int((radius + spike_length) * pygame.math.Vector2(1, 0).rotate(angle).x)
                end_y = center_y + int((radius + spike_length) * pygame.math.Vector2(1, 0).rotate(angle).y)
                pygame.draw.line(screen, color, (spike_x, spike_y), (end_x, end_y), 2)

    def _draw_number(self, screen: pygame.Surface) -> None:
        """Draw the number of adjacent mines."""
        if not self.font:
            return

        # Get color based on number
        color = self._get_number_color(self.cell.adjacent_mines)

        # Render number text
        text = str(self.cell.adjacent_mines)
        text_surface = self.font.render(text, True, color)
        text_rect = text_surface.get_rect(center=self.rect.center)

        # Draw text
        screen.blit(text_surface, text_rect)

    def _get_number_color(self, number: int) -> Tuple[int, int, int]:
        """Get the color for a number based on standard minesweeper colors."""
        colors = {
            1: COLOR_NUMBER_1,
            2: COLOR_NUMBER_2,
            3: COLOR_NUMBER_3,
            4: COLOR_NUMBER_4,
            5: COLOR_NUMBER_5,
            6: COLOR_NUMBER_6,
            7: COLOR_NUMBER_7,
            8: COLOR_NUMBER_8,
        }
        return colors.get(number, COLOR_TEXT)

    def is_point_inside(self, pos: Tuple[int, int]) -> bool:
        """Check if a point is inside the cell.

        Args:
            pos: (x, y) position

        Returns:
            True if point is inside cell
        """
        return self.rect.collidepoint(pos)

    def get_screen_position(self) -> Tuple[int, int]:
        """Get the screen position of the cell.

        Returns:
            (x, y) position on screen
        """
        return (self.x, self.y)

    def get_cell_position(self) -> Tuple[int, int]:
        """Get the logical position of the cell.

        Returns:
            (row, col) position in grid
        """
        return (self.cell.row, self.cell.col)


class CellRendererFactory:
    """Factory for creating cell renderers."""

    def __init__(self, cell_size: int = CELL_SIZE, cell_padding: int = CELL_PADDING):
        """Initialize the factory.

        Args:
            cell_size: Size of each cell in pixels
            cell_padding: Padding between cells
        """
        self.cell_size = cell_size
        self.cell_padding = cell_padding
        self.font = None
        self._initialize_font()

    def _initialize_font(self) -> None:
        """Initialize the font for rendering numbers."""
        try:
            self.font = pygame.font.Font(None, FONT_SIZE_MEDIUM)
        except pygame.error:
            # Fallback if font loading fails
            self.font = None

    def create_renderer(self, cell: Cell, row: int, col: int, offset_x: int = 0, offset_y: int = 0) -> CellRenderer:
        """Create a cell renderer for the given cell.

        Args:
            cell: The cell to render
            row: Row position in grid
            col: Column position in grid
            offset_x: X offset for the entire grid
            offset_y: Y offset for the entire grid

        Returns:
            CellRenderer instance
        """
        x = offset_x + col * (self.cell_size + self.cell_padding)
        y = offset_y + row * (self.cell_size + self.cell_padding)

        renderer = CellRenderer(cell, x, y)
        renderer.set_font(self.font)
        return renderer
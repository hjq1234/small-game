"""Dropdown UI component for difficulty selection."""

import pygame
from typing import List, Tuple, Optional, Callable
from game.difficulty import DifficultyPreset


class DropdownOption:
    """Represents a single option in the dropdown."""

    def __init__(self, key: str, display_name: str, description: str = ""):
        """Initialize dropdown option.

        Args:
            key: Internal key for the option
            display_name: Text to display
            description: Optional description text
        """
        self.key = key
        self.display_name = display_name
        self.description = description


class Dropdown:
    """Dropdown menu component for selecting options."""

    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        font: pygame.font.Font,
        options: List[DropdownOption],
        on_select: Optional[Callable[[str], None]] = None
    ):
        """Initialize dropdown component.

        Args:
            x: X position on screen
            y: Y position on screen
            width: Dropdown width
            height: Dropdown height
            font: Font for rendering text
            options: List of dropdown options
            on_select: Callback function when option is selected
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font = font

        self.options = options
        self.on_select = on_select

        self.is_open = False
        self.hovered_index = -1

        self.border_radius = 3
        self.option_height = 30

        from config import (
            COLOR_HIDDEN, COLOR_REVEALED, COLOR_BORDER,
            COLOR_TEXT, COLOR_BG_HOVER
        )
        self.COLOR_HIDDEN = COLOR_HIDDEN
        self.COLOR_REVEALED = COLOR_REVEALED
        self.COLOR_BORDER = COLOR_BORDER
        self.COLOR_TEXT = COLOR_TEXT
        self.COLOR_BG_HOVER = COLOR_BG_HOVER

        self.main_rect = pygame.Rect(x, y, width, height)

    def handle_event(self, event: pygame.event.Event) -> Optional[str]:
        """Handle pygame events.

        Args:
            event: Pygame event

        Returns:
            Selected option key if selection occurred, None otherwise
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            return self._handle_click(event.pos)
        elif event.type == pygame.MOUSEMOTION:
            self._handle_hover(event.pos)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE and self.is_open:
                self.close()
                return None

        return None

    def _handle_click(self, pos: Tuple[int, int]) -> Optional[str]:
        """Handle click events.

        Args:
            pos: Mouse position

        Returns:
            Selected option key if selection occurred, None otherwise
        """
        if not self.is_open:
            if self.main_rect.collidepoint(pos):
                self.toggle()
            return None

        option_rects = self._get_option_rects()
        for i, rect in enumerate(option_rects):
            if rect.collidepoint(pos):
                selected_key = self.options[i].key
                self.close()
                if self.on_select:
                    self.on_select(selected_key)
                return selected_key

        if not self.main_rect.collidepoint(pos):
            self.close()

        return None

    def _handle_hover(self, pos: Tuple[int, int]) -> None:
        """Handle hover events.

        Args:
            pos: Mouse position
        """
        if not self.is_open:
            return

        option_rects = self._get_option_rects()
        self.hovered_index = -1

        for i, rect in enumerate(option_rects):
            if rect.collidepoint(pos):
                self.hovered_index = i
                break

    def _get_option_rects(self) -> List[pygame.Rect]:
        """Get rectangles for all option positions.

        Returns:
            List of pygame.Rect objects
        """
        rects = []
        for i in range(len(self.options)):
            rect = pygame.Rect(
                self.x,
                self.y + self.height + (i * self.option_height),
                self.width,
                self.option_height
            )
            rects.append(rect)
        return rects

    def toggle(self) -> None:
        """Toggle dropdown open/closed."""
        self.is_open = not self.is_open
        self.hovered_index = -1

    def open(self) -> None:
        """Open dropdown."""
        self.is_open = True
        self.hovered_index = -1

    def close(self) -> None:
        """Close dropdown."""
        self.is_open = False
        self.hovered_index = -1

    def render(self, screen: pygame.Surface) -> None:
        """Render dropdown on screen.

        Args:
            screen: Pygame screen surface
        """
        self._render_main_button(screen)

        if self.is_open:
            self._render_options(screen)

    def _render_main_button(self, screen: pygame.Surface) -> None:
        """Render the main dropdown button.

        Args:
            screen: Pygame screen surface
        """
        pygame.draw.rect(screen, self.COLOR_HIDDEN, self.main_rect)
        pygame.draw.rect(screen, self.COLOR_BORDER, self.main_rect, 1)

        text = "Select Difficulty"
        if self.options:
            text = self.options[0].display_name

        text_surface = self.font.render(text, True, self.COLOR_TEXT)
        text_rect = text_surface.get_rect(center=self.main_rect.center)
        screen.blit(text_surface, text_rect)

        arrow_x = self.main_rect.right - 15
        arrow_y = self.main_rect.centery

        arrow_points = [
            (arrow_x - 5, arrow_y - 3),
            (arrow_x + 5, arrow_y - 3),
            (arrow_x, arrow_y + 3)
        ]
        pygame.draw.polygon(screen, self.COLOR_TEXT, arrow_points)

    def _render_options(self, screen: pygame.Surface) -> None:
        """Render dropdown options.

        Args:
            screen: Pygame screen surface
        """
        option_rects = self._get_option_rects()

        for i, (option, rect) in enumerate(zip(self.options, option_rects)):
            bg_color = self.COLOR_REVEALED
            if i == self.hovered_index:
                bg_color = self.COLOR_BG_HOVER

            pygame.draw.rect(screen, bg_color, rect)
            pygame.draw.rect(screen, self.COLOR_BORDER, rect, 1)

            text = option.display_name
            text_surface = self.font.render(text, True, self.COLOR_TEXT)
            text_rect = text_surface.get_rect(midleft=(rect.x + 10, rect.centery))
            screen.blit(text_surface, text_rect)


class DifficultyDropdown(Dropdown):
    """Dropdown specifically for difficulty selection."""

    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        font: pygame.font.Font,
        on_difficulty_select: Optional[Callable[[str, dict], None]] = None
    ):
        """Initialize difficulty dropdown.

        Args:
            x: X position on screen
            y: Y position on screen
            width: Dropdown width
            height: Dropdown height
            font: Font for rendering text
            on_difficulty_select: Callback when difficulty is selected
        """
        options = self._create_difficulty_options()
        self.on_difficulty_select = on_difficulty_select

        def handle_select(key: str) -> None:
            difficulty_config = self._get_difficulty_config(key)
            if self.on_difficulty_select and difficulty_config:
                self.on_difficulty_select(key, difficulty_config)

        super().__init__(x, y, width, height, font, options, handle_select)

    def _create_difficulty_options(self) -> List[DropdownOption]:
        """Create difficulty dropdown options.

        Returns:
            List of DropdownOption objects
        """
        return [
            DropdownOption(
                "beginner",
                "Beginner (9×9, 10 mines)"
            ),
            DropdownOption(
                "intermediate",
                "Intermediate (16×16, 40 mines)"
            ),
            DropdownOption(
                "advanced",
                "Advanced (30×16, 99 mines)"
            ),
            DropdownOption(
                "custom",
                "Custom..."
            )
        ]

    def _get_difficulty_config(self, key: str) -> Optional[dict]:
        """Get difficulty configuration by key.

        Args:
            key: Difficulty key

        Returns:
            Difficulty configuration dictionary or None
        """
        configs = {
            "beginner": DifficultyPreset.BEGINNER.level.__dict__,
            "intermediate": DifficultyPreset.INTERMEDIATE.level.__dict__,
            "advanced": DifficultyPreset.ADVANCED.level.__dict__,
            "custom": None
        }
        return configs.get(key)

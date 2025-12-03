"""Main game window and rendering for minesweeper game."""

import pygame
import sys
from typing import Optional, Tuple, Dict, Any
from game.game_state import GameSession, GameState, create_game_session
from game.difficulty import DifficultyPreset
from ui.cell_renderer import CellRendererFactory
from ui.input_handler import InputHandler
from config import (
    WINDOW_TITLE, WINDOW_WIDTH, WINDOW_HEIGHT, FPS_TARGET,
    COLOR_TEXT, COLOR_HIDDEN, FONT_SIZE_MEDIUM, FONT_SIZE_LARGE
)


class GameWindow:
    """Main game window and rendering manager."""

    def __init__(self):
        """Initialize the game window."""
        pygame.init()
        pygame.font.init()

        # Screen setup
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(WINDOW_TITLE)

        # Game state
        self.game_session: Optional[GameSession] = None
        self.cell_renderers: Dict[Tuple[int, int], 'CellRenderer'] = {}
        self.cell_renderer_factory = CellRendererFactory()

        # UI components
        self.font_medium = pygame.font.Font(None, FONT_SIZE_MEDIUM)
        self.font_large = pygame.font.Font(None, FONT_SIZE_LARGE)
        self.input_handler = InputHandler()

        # Game settings
        self.board_offset_x = 50
        self.board_offset_y = 100
        self.status_bar_height = 80

        # Game loop
        self.clock = pygame.time.Clock()
        self.running = True

    def start_new_game(self, difficulty_name: str = "beginner", **custom_settings) -> None:
        """Start a new game with the specified difficulty.

        Args:
            difficulty_name: Name of the difficulty level
            **custom_settings: Custom settings for custom difficulty
        """
        self.game_session = create_game_session(difficulty_name, **custom_settings)
        self._create_cell_renderers()

    def _create_cell_renderers(self) -> None:
        """Create cell renderers for the current game board."""
        if not self.game_session:
            return

        self.cell_renderers.clear()
        board = self.game_session.board

        for row in range(board.height):
            for col in range(board.width):
                cell = board.cells[row][col]
                renderer = self.cell_renderer_factory.create_renderer(
                    cell, row, col, self.board_offset_x, self.board_offset_y
                )
                self.cell_renderers[(row, col)] = renderer

    def run(self) -> None:
        """Run the main game loop."""
        # Start with beginner difficulty by default
        self.start_new_game("beginner")

        while self.running:
            self._handle_events()
            self._update_game()
            self._render()
            self.clock.tick(FPS_TARGET)

        pygame.quit()
        sys.exit()

    def _handle_events(self) -> None:
        """Handle pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False
            else:
                self._handle_game_event(event)

    def _handle_game_event(self, event: pygame.event.Event) -> None:
        """Handle game-specific events.

        Args:
            event: Pygame event
        """
        action = self.input_handler.handle_events(event)
        if not action or not self.game_session:
            return

        action_type = action['type']

        if action_type == 'left_click':
            self._handle_left_click(action['position'])
        elif action_type == 'right_click':
            self._handle_right_click(action['position'])
        elif action_type == 'double_click':
            self._handle_double_click(action['position'])
        elif action_type == 'pause_resume':
            self._toggle_pause()
        elif action_type == 'restart':
            self._restart_game()
        elif action_type == 'new_game':
            self._show_difficulty_menu()
        elif action_type == 'set_difficulty':
            self.start_new_game(action['difficulty'])

    def _handle_left_click(self, position: Tuple[int, int]) -> None:
        """Handle left mouse click.

        Args:
            position: Mouse position (x, y)
        """
        if not self.game_session or self.game_session.is_game_over():
            return

        grid_pos = self.input_handler.screen_to_grid(
            position, self.cell_renderer_factory.cell_size,
            self.board_offset_x, self.board_offset_y
        )

        if grid_pos:
            row, col = grid_pos
            try:
                self.game_session.make_move(row, col, 'reveal')
            except ValueError:
                # Invalid move (e.g., flagged cell)
                pass

    def _handle_right_click(self, position: Tuple[int, int]) -> None:
        """Handle right mouse click.

        Args:
            position: Mouse position (x, y)
        """
        if not self.game_session or self.game_session.is_game_over():
            return

        grid_pos = self.input_handler.screen_to_grid(
            position, self.cell_renderer_factory.cell_size,
            self.board_offset_x, self.board_offset_y
        )

        if grid_pos:
            row, col = grid_pos
            try:
                self.game_session.make_move(row, col, 'flag')
            except ValueError:
                # Invalid move
                pass

    def _handle_double_click(self, position: Tuple[int, int]) -> None:
        """Handle double mouse click.

        Args:
            position: Mouse position (x, y)
        """
        if not self.game_session or self.game_session.is_game_over():
            return

        grid_pos = self.input_handler.screen_to_grid(
            position, self.cell_renderer_factory.cell_size,
            self.board_offset_x, self.board_offset_y
        )

        if grid_pos:
            row, col = grid_pos
            try:
                self.game_session.expand_adjacent(row, col)
            except ValueError:
                # Invalid expansion
                pass

    def _toggle_pause(self) -> None:
        """Toggle game pause state."""
        if not self.game_session:
            return

        if self.game_session.state == GameState.PLAYING:
            self.game_session.pause_game()
        elif self.game_session.state == GameState.PAUSED:
            self.game_session.resume_game()

    def _restart_game(self) -> None:
        """Restart the current game."""
        if self.game_session:
            self.game_session.reset_game()
            self._create_cell_renderers()

    def _show_difficulty_menu(self) -> None:
        """Show difficulty selection menu."""
        # For now, just cycle through difficulties
        # In a full implementation, this would show a proper menu
        if not self.game_session:
            return

        current_difficulty = self.game_session.difficulty.name.lower()
        difficulties = ['beginner', 'intermediate', 'advanced']

        try:
            current_index = difficulties.index(current_difficulty)
            next_index = (current_index + 1) % len(difficulties)
            self.start_new_game(difficulties[next_index])
        except ValueError:
            # Current difficulty not in list (custom), start with beginner
            self.start_new_game('beginner')

    def _update_game(self) -> None:
        """Update game state."""
        # Game state updates are handled by the game session
        pass

    def _render(self) -> None:
        """Render the game."""
        # Clear screen
        self.screen.fill(COLOR_HIDDEN)

        # Render status bar
        self._render_status_bar()

        # Render game board
        if self.game_session:
            self._render_board()

        # Update display
        pygame.display.flip()

    def _render_status_bar(self) -> None:
        """Render the status bar with game information."""
        if not self.game_session:
            return

        stats = self.game_session.get_statistics()

        # Game state text
        state_text = f"State: {stats['state'].title()}"
        state_surface = self.font_medium.render(state_text, True, COLOR_TEXT)
        self.screen.blit(state_surface, (10, 10))

        # Difficulty text
        difficulty_text = f"Difficulty: {stats['difficulty']}"
        difficulty_surface = self.font_medium.render(difficulty_text, True, COLOR_TEXT)
        self.screen.blit(difficulty_surface, (10, 35))

        # Mines remaining
        mines_remaining = stats['mine_count'] - stats['flagged_count']
        mines_text = f"Mines: {mines_remaining}"
        mines_surface = self.font_medium.render(mines_text, True, COLOR_TEXT)
        self.screen.blit(mines_surface, (200, 10))

        # Time elapsed
        duration = stats.get('duration', 0) or 0
        time_text = f"Time: {int(duration)}s"
        time_surface = self.font_medium.render(time_text, True, COLOR_TEXT)
        self.screen.blit(time_surface, (200, 35))

        # Game over message
        if self.game_session.is_game_over():
            if self.game_session.state == GameState.WON:
                message = "You Win! Press R to restart or N for new game"
            else:
                message = "Game Over! Press R to restart or N for new game"

            message_surface = self.font_large.render(message, True, COLOR_TEXT)
            message_rect = message_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 30))
            self.screen.blit(message_surface, message_rect)

        # Controls help
        controls_text = "Controls: Left-click reveal, Right-click flag, Double-click expand, Space pause, ESC quit"
        controls_surface = self.font_medium.render(controls_text, True, COLOR_TEXT)
        controls_rect = controls_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 60))
        self.screen.blit(controls_surface, controls_rect)

    def _render_board(self) -> None:
        """Render the game board."""
        if not self.game_session:
            return

        game_over = self.game_session.is_game_over()

        # Render each cell
        for renderer in self.cell_renderers.values():
            renderer.render(self.screen, game_over)

    def get_game_stats(self) -> Optional[Dict[str, Any]]:
        """Get current game statistics.

        Returns:
            Game statistics dictionary or None if no game active
        """
        if not self.game_session:
            return None

        return self.game_session.get_statistics()


def main():
    """Main entry point for the game."""
    try:
        game = GameWindow()
        game.run()
    except KeyboardInterrupt:
        print("\nGame interrupted by user")
    except Exception as e:
        print(f"Error running game: {e}")
        pygame.quit()
        sys.exit(1)


if __name__ == "__main__":
    main()
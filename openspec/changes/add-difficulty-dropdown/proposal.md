# Change: Add Dropdown Difficulty Selection

## Why
Currently, users can only change game difficulty using keyboard shortcuts (1, 2, 3 keys). While functional, this isn't intuitive for new users who expect a visual dropdown menu to select difficulty. Adding a dropdown UI component will improve user experience by making difficulty selection more accessible and discoverable.

## What Changes
- Add a dropdown component for difficulty selection in the game UI
- Replace the current `_show_difficulty_menu()` method which only cycles through difficulties
- Display all available difficulty options (Beginner, Intermediate, Advanced, Custom) in an easy-to-select format
- Make the dropdown clickable with visual feedback
- Ensure dropdown integrates seamlessly with existing UI

## Impact
- Affected specs: `ui` capability
- Affected code:
  - `src/ui/game_window.py` - Main UI rendering
  - `src/ui/dropdown.py` - New dropdown component (will be created)
  - `src/ui/input_handler.py` - Handle dropdown selection
- Breaking changes: None
- Backward compatibility: Keyboard shortcuts (1, 2, 3) remain functional

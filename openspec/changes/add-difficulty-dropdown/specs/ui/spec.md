## ADDED Requirements
### Requirement: Dropdown Difficulty Selection
The game SHALL provide a visual dropdown menu for selecting difficulty levels.

#### Scenario: Open dropdown menu
- **WHEN** user presses 'N' key or clicks on difficulty selector
- **THEN** a dropdown menu displays with all available difficulty options

#### Scenario: Select difficulty from dropdown
- **WHEN** user clicks on a difficulty option in the dropdown
- **THEN** the game starts a new game with the selected difficulty
- **AND** the dropdown closes
- **AND** the selected difficulty is displayed in the status bar

#### Scenario: View available difficulty options
- **WHEN** dropdown is open
- **THEN** the following options are displayed:
  - Beginner (9×9, 10 mines)
  - Intermediate (16×16, 40 mines)
  - Advanced (30×16, 99 mines)
  - Custom...

#### Scenario: Click outside to close dropdown
- **WHEN** user clicks anywhere outside the dropdown
- **THEN** the dropdown closes without changing the difficulty

#### Scenario: Keyboard shortcuts still work
- **WHEN** user presses '1', '2', or '3' keys
- **THEN** the difficulty changes immediately
- **AND** the dropdown is not affected

### Requirement: Dropdown Visual Design
The dropdown SHALL integrate with the existing game UI and provide clear visual feedback.

#### Scenario: Dropdown appearance
- **WHEN** dropdown is rendered
- **THEN** it displays:
  - A bordered rectangular container
  - Each option as a separate clickable area
  - Highlighted option on hover
  - Clear text labels for each difficulty

#### Scenario: Custom difficulty option
- **WHEN** user clicks "Custom..." option
- **THEN** a custom settings dialog appears
- **OR** the game prompts for custom board parameters

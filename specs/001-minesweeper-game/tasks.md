# Tasks: Minesweeper Game

**Input**: Design documents from `/specs/001-minesweeper-game/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create project structure per implementation plan
- [ ] T002 Initialize Python project with pygame dependency
- [ ] T003 [P] Configure pytest for testing framework
- [ ] T004 Create base configuration file in src/config.py

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T005 Create Cell entity with state pattern in src/game/cell.py
- [ ] T006 [P] Implement CellState classes (HiddenState, RevealedState, FlaggedState)
- [ ] T007 Create Board entity in src/game/board.py with basic grid management
- [ ] T008 Implement mine generation algorithm in src/game/board.py
- [ ] T009 Create GameSession entity in src/game/game_state.py
- [ ] T010 Implement difficulty level configurations in src/game/difficulty.py
- [ ] T011 Create board validation logic in src/game/validator.py
- [ ] T012 Setup basic Pygame window in src/ui/game_window.py
- [ ] T013 Configure game constants and colors in src/config.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Play Classic Minesweeper (Priority: P1) 🎯 MVP

**Goal**: Implement core minesweeper gameplay with cell revealing and mine detection

**Independent Test**: Start a new game, click cells to reveal them, verify numbers show correct adjacent mine counts. Game should be fully playable as basic minesweeper.

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

- [ ] T014 [P] [US1] Unit test for cell reveal logic in tests/unit/test_cell.py
- [ ] T015 [P] [US1] Unit test for adjacent mine calculation in tests/unit/test_board.py
- [ ] T016 [P] [US1] Integration test for game flow in tests/integration/test_game_flow.py

### Implementation for User Story 1

- [ ] T017 [P] [US1] Implement cell reveal logic in src/game/cell.py
- [ ] T018 [P] [US1] Implement adjacent mine calculation in src/game/board.py
- [ ] T019 [US1] Create cell rendering system in src/ui/cell_renderer.py
- [ ] T020 [US1] Implement left-click input handling in src/ui/input_handler.py
- [ ] T021 [US1] Add game state transitions (NEW → PLAYING → WON/LOST) in src/game/game_state.py
- [ ] T022 [US1] Implement first-click safety (no mine on first click) in src/game/board.py
- [ ] T023 [US1] Add visual feedback for revealed cells in src/ui/cell_renderer.py
- [ ] T024 [US1] Implement game over detection and display in src/ui/game_window.py

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Flag Mines with Right-Click (Priority: P2)

**Goal**: Implement flagging system for strategic mine marking

**Independent Test**: Right-click cells to add/remove flags, verify flagged cells cannot be accidentally revealed by left-clicking.

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [ ] T025 [P] [US2] Unit test for flag toggle logic in tests/unit/test_cell.py
- [ ] T026 [P] [US2] Unit test for flag prevention logic in tests/unit/test_board.py

### Implementation for User Story 2

- [ ] T027 [P] [US2] Implement flag toggle logic in src/game/cell.py
- [ ] T028 [US2] Add flag rendering in src/ui/cell_renderer.py
- [ ] T029 [US2] Implement right-click input handling in src/ui/input_handler.py
- [ ] T030 [US2] Add flag count tracking in src/game/game_state.py
- [ ] T031 [US2] Implement flag prevention for left-clicks in src/game/board.py
- [ ] T032 [US2] Add visual flag icon display in src/ui/cell_renderer.py

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Use Preset Difficulty Levels (Priority: P2)

**Goal**: Implement three preset difficulty configurations

**Independent Test**: Select each difficulty level and verify board dimensions and mine counts match expected values.

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [ ] T033 [P] [US3] Unit test for difficulty configurations in tests/unit/test_difficulty.py
- [ ] T034 [P] [US3] Integration test for difficulty selection in tests/integration/test_game_flow.py

### Implementation for User Story 3

- [ ] T035 [P] [US3] Implement difficulty selection UI in src/ui/game_window.py
- [ ] T036 [US3] Add difficulty presets (Beginner/Intermediate/Advanced) in src/game/difficulty.py
- [ ] T037 [US3] Implement board generation for each difficulty in src/game/board.py
- [ ] T038 [US3] Add difficulty selection menu in src/ui/game_window.py
- [ ] T039 [US3] Connect difficulty selection to game initialization in src/main.py

**Checkpoint**: At this point, User Stories 1, 2 AND 3 should all work independently

---

## Phase 6: User Story 4 - Auto-Expand Safe Areas (Priority: P3)

**Goal**: Implement double-click auto-expansion for faster gameplay

**Independent Test**: Double-click revealed cells with correct number of adjacent flags and verify safe adjacent cells are automatically revealed.

### Tests for User Story 4 (OPTIONAL - only if tests requested) ⚠️

- [ ] T040 [P] [US4] Unit test for auto-expansion logic in tests/unit/test_board.py
- [ ] T041 [P] [US4] Integration test for double-click behavior in tests/integration/test_game_flow.py

### Implementation for User Story 4

- [ ] T042 [US4] Implement double-click detection in src/ui/input_handler.py
- [ ] T043 [US4] Add auto-expansion logic in src/game/board.py
- [ ] T044 [US4] Implement adjacent cell checking for expansion in src/game/board.py
- [ ] T045 [US4] Add visual feedback for auto-expansion in src/ui/cell_renderer.py

**Checkpoint**: All user stories should now be independently functional

---

## Phase 7: User Story 5 - Custom Board Configuration (Priority: P3)

**Goal**: Implement custom board size and mine count configuration

**Independent Test**: Enter custom dimensions and mine counts, verify game creates board matching specifications.

### Tests for User Story 5 (OPTIONAL - only if tests requested) ⚠️

- [ ] T046 [P] [US5] Unit test for custom validation in tests/unit/test_validator.py
- [ ] T047 [P] [US5] Integration test for custom settings in tests/integration/test_game_flow.py

### Implementation for User Story 5

- [ ] T048 [US5] Add custom settings UI in src/ui/game_window.py
- [ ] T049 [US5] Implement custom validation logic in src/game/validator.py
- [ ] T050 [US5] Add custom settings form in src/ui/game_window.py
- [ ] T051 [US5] Connect custom settings to game initialization in src/main.py
- [ ] T052 [US5] Add error handling for invalid custom settings in src/ui/game_window.py

**Checkpoint**: All user stories should now be independently functional with custom configuration support

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T053 [P] Add game timer display in src/ui/game_window.py
- [ ] T054 [P] Implement mine counter in src/ui/game_window.py
- [ ] T055 [P] Add keyboard shortcuts (Space=Pause, R=Restart, N=New) in src/ui/input_handler.py
- [ ] T056 [P] Create game assets (cell sprites, icons) in src/ui/assets/
- [ ] T057 [P] Add sound effects (optional) in src/ui/assets/
- [ ] T058 [P] Implement high score tracking in src/game/game_state.py
- [ ] T059 [P] Add help/instructions screen in src/ui/game_window.py
- [ ] T060 [P] Performance optimization and memory profiling
- [ ] T061 [P] Code cleanup and documentation updates
- [ ] T062 Run quickstart.md validation

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Integrates with US1 cell revealing
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - Uses same board generation as US1
- **User Story 4 (P3)**: Can start after US1/US2 complete - Requires flagging and revealing logic
- **User Story 5 (P3)**: Can start after Foundational (Phase 2) - Extends board generation with validation

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before UI components
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together (if tests requested):
Task: "Unit test for cell reveal logic in tests/unit/test_cell.py"
Task: "Unit test for adjacent mine calculation in tests/unit/test_board.py"
Task: "Integration test for game flow in tests/integration/test_game_flow.py"

# Launch all models for User Story 1 together:
Task: "Implement cell reveal logic in src/game/cell.py"
Task: "Implement adjacent mine calculation in src/game/board.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 → Test independently → Deploy/Demo
6. Add User Story 5 → Test independently → Deploy/Demo
7. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (Core gameplay)
   - Developer B: User Story 2 (Flagging system)
   - Developer C: User Story 3 (Difficulty levels)
3. After US1-3 complete:
   - Developer A: User Story 4 (Auto-expansion)
   - Developer B: User Story 5 (Custom settings)
   - Developer C: Polish phase
4. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
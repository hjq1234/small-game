"""Difficulty level configurations for minesweeper game."""

from enum import Enum
from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class DifficultyLevel:
    """Represents a difficulty level configuration."""
    name: str
    width: int
    height: int
    mines: int


class DifficultyPreset(Enum):
    """Predefined difficulty levels."""
    BEGINNER = DifficultyLevel("Beginner", 9, 9, 10)
    INTERMEDIATE = DifficultyLevel("Intermediate", 16, 16, 40)
    ADVANCED = DifficultyLevel("Advanced", 30, 16, 99)

    @property
    def level(self) -> DifficultyLevel:
        """Get the difficulty level configuration."""
        return self.value

    @classmethod
    def get_all_levels(cls) -> Dict[str, DifficultyLevel]:
        """Get all difficulty levels as a dictionary."""
        return {
            preset.name.lower(): preset.level
            for preset in cls
        }

    @classmethod
    def get_by_name(cls, name: str) -> DifficultyLevel:
        """Get difficulty level by name."""
        name_lower = name.lower()
        for preset in cls:
            if preset.name.lower() == name_lower:
                return preset.level
        raise ValueError(f"Unknown difficulty level: {name}")

    @classmethod
    def validate_custom_settings(cls, width: int, height: int, mines: int) -> bool:
        """Validate custom board settings."""
        from .validator import validate_board_settings
        return validate_board_settings(width, height, mines)


def create_custom_difficulty(width: int, height: int, mines: int) -> DifficultyLevel:
    """Create a custom difficulty level."""
    DifficultyPreset.validate_custom_settings(width, height, mines)
    return DifficultyLevel("Custom", width, height, mines)


def get_difficulty_recommendations() -> Dict[str, Any]:
    """Get difficulty level recommendations and constraints."""
    return {
        "min_width": 9,
        "max_width": 30,
        "min_height": 9,
        "max_height": 30,
        "min_mines": 1,
        "max_mine_density": 0.25,  # 25%
        "presets": {
            "beginner": {"width": 9, "height": 9, "mines": 10},
            "intermediate": {"width": 16, "height": 16, "mines": 40},
            "advanced": {"width": 30, "height": 16, "mines": 99}
        }
    }
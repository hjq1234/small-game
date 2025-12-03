"""Unit tests for difficulty level configurations."""

import pytest
from src.game.difficulty import DifficultyLevel, DifficultyPreset, create_custom_difficulty, get_difficulty_recommendations
from src.game.validator import validate_board_settings


class TestDifficultyLevel:
    """Test DifficultyLevel dataclass."""

    def test_difficulty_level_creation(self):
        """Test creating a difficulty level."""
        level = DifficultyLevel("Test", 15, 20, 25)
        assert level.name == "Test"
        assert level.width == 15
        assert level.height == 20
        assert level.mines == 25

    def test_difficulty_level_equality(self):
        """Test difficulty level equality."""
        level1 = DifficultyLevel("Test", 10, 10, 10)
        level2 = DifficultyLevel("Test", 10, 10, 10)
        level3 = DifficultyLevel("Different", 10, 10, 10)

        assert level1 == level2
        assert level1 != level3


class TestDifficultyPreset:
    """Test predefined difficulty levels."""

    def test_beginner_preset(self):
        """Test beginner difficulty preset."""
        preset = DifficultyPreset.BEGINNER
        level = preset.level

        assert level.name == "Beginner"
        assert level.width == 9
        assert level.height == 9
        assert level.mines == 10

    def test_intermediate_preset(self):
        """Test intermediate difficulty preset."""
        preset = DifficultyPreset.INTERMEDIATE
        level = preset.level

        assert level.name == "Intermediate"
        assert level.width == 16
        assert level.height == 16
        assert level.mines == 40

    def test_advanced_preset(self):
        """Test advanced difficulty preset."""
        preset = DifficultyPreset.ADVANCED
        level = preset.level

        assert level.name == "Advanced"
        assert level.width == 30
        assert level.height == 16
        assert level.mines == 99

    def test_get_all_levels(self):
        """Test getting all difficulty levels."""
        levels = DifficultyPreset.get_all_levels()

        assert "beginner" in levels
        assert "intermediate" in levels
        assert "advanced" in levels

        assert levels["beginner"] == DifficultyPreset.BEGINNER.level
        assert levels["intermediate"] == DifficultyPreset.INTERMEDIATE.level
        assert levels["advanced"] == DifficultyPreset.ADVANCED.level

    def test_get_by_name_valid(self):
        """Test getting difficulty by valid name."""
        beginner = DifficultyPreset.get_by_name("beginner")
        assert beginner == DifficultyPreset.BEGINNER.level

        intermediate = DifficultyPreset.get_by_name("intermediate")
        assert intermediate == DifficultyPreset.INTERMEDIATE.level

        advanced = DifficultyPreset.get_by_name("advanced")
        assert advanced == DifficultyPreset.ADVANCED.level

        # Test case insensitive
        beginner_upper = DifficultyPreset.get_by_name("BEGINNER")
        assert beginner_upper == DifficultyPreset.BEGINNER.level

    def test_get_by_name_invalid(self):
        """Test getting difficulty by invalid name."""
        with pytest.raises(ValueError, match="Unknown difficulty level"):
            DifficultyPreset.get_by_name("invalid")

        with pytest.raises(ValueError, match="Unknown difficulty level"):
            DifficultyPreset.get_by_name("")

    def test_validate_custom_settings_valid(self):
        """Test validating valid custom settings."""
        # Valid settings
        assert DifficultyPreset.validate_custom_settings(15, 15, 30) is True
        assert DifficultyPreset.validate_custom_settings(20, 20, 50) is True

    def test_validate_custom_settings_invalid(self):
        """Test validating invalid custom settings."""
        # Invalid dimensions
        with pytest.raises(ValueError):
            DifficultyPreset.validate_custom_settings(5, 15, 10)

        # Invalid mine count
        with pytest.raises(ValueError):
            DifficultyPreset.validate_custom_settings(15, 15, 100)


class TestCustomDifficulty:
    """Test custom difficulty creation."""

    def test_create_custom_difficulty_valid(self):
        """Test creating valid custom difficulty."""
        custom = create_custom_difficulty(20, 25, 75)

        assert custom.name == "Custom"
        assert custom.width == 20
        assert custom.height == 25
        assert custom.mines == 75

    def test_create_custom_difficulty_invalid(self):
        """Test creating invalid custom difficulty."""
        # Invalid dimensions
        with pytest.raises(ValueError):
            create_custom_difficulty(5, 15, 10)

        # Invalid mine count
        with pytest.raises(ValueError):
            create_custom_difficulty(15, 15, 100)


class TestDifficultyRecommendations:
    """Test difficulty recommendations."""

    def test_get_difficulty_recommendations(self):
        """Test getting difficulty recommendations."""
        recommendations = get_difficulty_recommendations()

        assert "min_width" in recommendations
        assert "max_width" in recommendations
        assert "min_height" in recommendations
        assert "max_height" in recommendations
        assert "min_mines" in recommendations
        assert "max_mine_density" in recommendations
        assert "presets" in recommendations

        assert recommendations["min_width"] == 9
        assert recommendations["max_width"] == 30
        assert recommendations["min_height"] == 9
        assert recommendations["max_height"] == 30
        assert recommendations["min_mines"] == 1
        assert recommendations["max_mine_density"] == 0.25

        presets = recommendations["presets"]
        assert "beginner" in presets
        assert "intermediate" in presets
        assert "advanced" in presets

        assert presets["beginner"]["width"] == 9
        assert presets["beginner"]["height"] == 9
        assert presets["beginner"]["mines"] == 10

        assert presets["intermediate"]["width"] == 16
        assert presets["intermediate"]["height"] == 16
        assert presets["intermediate"]["mines"] == 40

        assert presets["advanced"]["width"] == 30
        assert presets["advanced"]["height"] == 16
        assert presets["advanced"]["mines"] == 99
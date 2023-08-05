"""
Test `rlmusician.environment.scoring` module.

Author: Nikolay Lysenko
"""


from typing import Dict

import numpy as np
import pytest

from rlmusician.environment.scoring import (
    score_absence_of_outer_notes,
    score_absence_of_stalled_notes,
    score_conjunct_motion,
    score_consonances,
    score_contrary_motion,
    score_noncyclicity,
    score_number_of_simultaneously_played_notes,
    score_usage_of_tonic
)


@pytest.mark.parametrize(
    "roll, scale, tonic_position, expected",
    [
        (
            # `roll`
            np.array([
                [0, 0, 0],
                [0, 0, 1],
                [1, 0, 0],
                [0, 1, 0],
                [0, 0, 0],
                [0, 1, 0],
                [1, 0, 1],
                [0, 0, 0],
                [1, 0, 0],
                [0, 0, 0],
                [0, 0, 0],
                [0, 0, 0],
            ]),
            # `scale`
            'major',
            # `tonic_position`
            4,
            # `expected`
            -3
        ),
        (
            # `roll`
            np.array([
                [0, 0, 0],
                [0, 0, 1],
                [1, 0, 0],
                [0, 1, 0],
                [0, 0, 0],
                [0, 1, 0],
                [1, 0, 1],
                [0, 0, 0],
                [1, 0, 0],
                [0, 0, 0],
                [0, 0, 0],
                [0, 0, 0],
            ]),
            # `scale`
            'minor',
            # `tonic_position`
            0,
            # `expected`
            -2
        ),
        (
            # `roll`
            np.array([
                [0, 0, 0],
                [0, 0, 1],
                [1, 0, 0],
                [0, 1, 0],
                [0, 0, 0],
                [0, 1, 0],
                [1, 0, 1],
            ]),
            # `scale`
            'major',
            # `tonic_position`
            2,
            # `expected`
            -4
        )
    ]
)
def test_score_absence_of_outer_notes(
        roll: np.ndarray, scale: str, tonic_position: int, expected: float
) -> None:
    """Test `score_absence_of_outer_notes` function."""
    result = score_absence_of_outer_notes(roll, scale, tonic_position)
    assert result == expected


@pytest.mark.parametrize(
    "roll, max_n_time_steps, expected",
    [
        (
            # `roll`,
            np.array([
                [1, 1, 1, 1],
                [0, 1, 0, 1],
                [0, 0, 0, 0],
            ]),
            # `max_n_time_steps`
            3,
            # expected`
            -1
        ),
        (
            # `roll`,
            np.array([
                [1, 1, 1, 1],
                [0, 1, 0, 1],
                [1, 1, 0, 0],
            ]),
            # `max_n_time_steps`
            2,
            # expected`
            -2
        ),
        (
            # `roll`,
            np.array([
                [1, 1, 1, 1],
                [0, 1, 0, 1],
                [1, 1, 0, 0],
            ]),
            # `max_n_time_steps`
            1,
            # expected`
            -4
        ),
    ]
)
def test_score_absence_of_stalled_notes(
        roll: np.ndarray, max_n_time_steps: int, expected: int
) -> None:
    """Test `score_absence_of_stalled_notes` function."""
    result = score_absence_of_stalled_notes(roll, max_n_time_steps)
    assert result == expected


@pytest.mark.parametrize(
    "roll, max_n_semitones, max_n_time_steps, expected",
    [
        (
            # `roll`
            np.array([
                [1, 0, 0, 0],
                [0, 1, 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1],
            ]),
            # `max_n_semitones`
            1,
            # `max_n_time_steps`
            1,
            # `expected`
            3
        ),
        (
            # `roll`
            np.array([
                [1, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1],
                [0, 0, 0, 0],
                [0, 1, 0, 1],
            ]),
            # `max_n_semitones`
            1,
            # `max_n_time_steps`
            1,
            # `expected`
            1
        ),
        (
            # `roll`
            np.array([
                [1, 0, 0, 0],
                [0, 0, 0, 1],
                [0, 0, 1, 0],
                [0, 0, 0, 1],
            ]),
            # `max_n_semitones`
            1,
            # `max_n_time_steps`
            1,
            # `expected`
            2
        ),
        (
            # `roll`
            np.array([
                [1, 0, 0, 0],
                [0, 0, 1, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1],
            ]),
            # `max_n_semitones`
            1,
            # `max_n_time_steps`
            2,
            # `expected`
            2
        ),
        (
            # `roll`
            np.array([
                [1, 0, 0, 0],
                [0, 0, 0, 1],
                [0, 1, 0, 0],
                [0, 0, 1, 1],
            ]),
            # `max_n_semitones`
            2,
            # `max_n_time_steps`
            1,
            # `expected`
            3
        ),
        (
            # `roll`
            np.array([
                [1, 1, 1, 1],
                [0, 1, 0, 1],
                [0, 0, 1, 0],
                [0, 1, 0, 1],
            ]),
            # `max_n_semitones`
            3,
            # `max_n_time_steps`
            3,
            # `expected`
            5
        ),
    ]
)
def test_score_conjunct_motion(
        roll: np.ndarray, max_n_semitones: int, max_n_time_steps: int,
        expected: int
) -> None:
    """Test `score_conjunct_motion` function."""
    result = score_conjunct_motion(roll, max_n_semitones, max_n_time_steps)
    assert result == expected


@pytest.mark.parametrize(
    "roll, interval_consonances, distance_weights, expected",
    [
        (
            # `roll`
            np.array([
                [0, 0, 0, 0, 0],
                [1, 1, 0, 0, 0],
                [0, 0, 0, 0, 1],
                [1, 1, 1, 0, 0]
            ]),
            # `interval_consonances`
            {1: -1, 2: -0.5, 3: 0},
            # `distance_weights`
            {0: 1, 1: 1, 2: 0.5, 3: 0.25},
            # `expected`
            -3.75
        ),
        (
            # `roll`
            np.array([
                [0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0],
                [1, 0, 1, 0, 0],
                [0, 0, 0, 0, 1]
            ]),
            # `interval_consonances`
            {1: -1, 2: -0.5, 3: 0},
            # `distance_weights`
            {0: 1, 1: 1, 2: 0.5, 3: 0.25},
            # `expected`
            -2.25
        ),
        (
            # `roll`
            np.array([
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0]
            ]),
            # `interval_consonances`
            {1: -1, 2: -0.5, 3: 0},
            # `distance_weights`
            {0: 1, 1: 1, 2: 0.5, 3: 0.25},
            # `expected`
            0
        ),
        (
            # `roll`
            np.array([
                [0, 1, 0, 1, 0],
                [0, 1, 1, 0, 0],
                [1, 0, 0, 1, 0],
                [0, 1, 0, 0, 1]
            ]),
            # `interval_consonances`
            {1: -1, 2: -0.5, 3: 0},
            # `distance_weights`
            {0: 1, 1: 1, 2: 0.5, 3: 0.25},
            # `expected`
            -11.75
        ),
    ]
)
def test_score_consonances(
        roll: np.ndarray, interval_consonances: Dict[int, float],
        distance_weights: Dict[int, float], expected: float
) -> None:
    """Test `score_consonances` function."""
    result = score_consonances(roll, interval_consonances, distance_weights)
    assert result == expected


@pytest.mark.parametrize(
    "roll, expected",
    [
        (
            # `roll`
            np.array([
                [0, 0, 0, 0, 0],
                [0, 1, 0, 0, 0],
                [1, 0, 1, 0, 1],
                [0, 0, 0, 1, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 1],
                [0, 0, 0, 1, 0],
                [1, 0, 0, 0, 0],
                [0, 1, 1, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
            ]),
            # `expected`
            3
        ),
        (
            # `roll`
            np.array([
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [1, 0, 0, 0, 1],
                [0, 1, 0, 1, 0],
                [0, 0, 1, 0, 0],
                [1, 0, 1, 0, 1],
                [0, 1, 0, 1, 0],
                [0, 0, 0, 1, 0],
                [0, 0, 1, 0, 1],
                [0, 1, 0, 0, 0],
                [1, 0, 0, 0, 0],
            ]),
            # `expected`
            5
        )
    ]
)
def test_score_contrary_motion(roll: np.ndarray, expected: float) -> None:
    """Test `score_contrary_motion` function."""
    result = score_contrary_motion(roll)
    assert result == expected


@pytest.mark.parametrize(
    "roll, max_n_time_steps, max_share, expected",
    [
        (
            # `roll`
            np.array([
                [1, 0, 1, 0, 1, 0],
                [0, 1, 0, 1, 0, 1],
            ]),
            # `max_n_time_steps`
            1,
            # `max_share`
            0.5,
            # `expected`
            1
        ),
        (
            # `roll`
            np.array([
                [1, 0, 1, 0, 1, 0],
                [0, 1, 0, 1, 0, 1],
            ]),
            # `max_n_time_steps`
            2,
            # `max_share`
            0.5,
            # `expected`
            1 / 3
        ),
        (
            # `roll`
            np.array([
                [1, 0, 1, 0, 1, 0],
                [0, 1, 0, 1, 0, 1],
                [0, 1, 1, 0, 0, 1],
            ]),
            # `max_n_time_steps`
            3,
            # `max_share`
            1,
            # `expected`
            5 / 18
        ),
    ]
)
def test_score_noncyclicity(
        roll: np.ndarray, max_n_time_steps: int, max_share: float,
        expected: float
) -> None:
    """Test `score_noncyclicity` function."""
    result = score_noncyclicity(roll, max_n_time_steps, max_share)
    assert result == expected


@pytest.mark.parametrize(
    "roll, n_lines, expected",
    [
        (
            # `roll`
            np.array([
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [1, 0, 1, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 1, 0, 0, 1],
                [1, 0, 0, 1, 1],
                [0, 0, 0, 1, 1],
                [0, 0, 1, 1, 1],
                [0, 0, 0, 0, 0],
                [1, 0, 0, 0, 0],
                [0, 1, 0, 0, 0],
                [0, 0, 0, 0, 0],
            ]),
            # `n_lines`
            3,
            # `expected`
            -3
        )
    ]
)
def test_score_number_of_simultaneously_played_notes(
        roll: np.ndarray, n_lines: int, expected: float
) -> None:
    """Test `score_number_of_simultaneously_played_notes` function."""
    result = score_number_of_simultaneously_played_notes(roll, n_lines)
    assert result == expected


@pytest.mark.parametrize(
    "roll, tonic_position, min_share, max_share, expected",
    [
        (
            # `roll`
            np.array([
                [0, 0, 0],
                [0, 0, 1],
                [1, 0, 0],
                [0, 1, 0],
                [0, 0, 0],
                [0, 1, 0],
                [1, 0, 1],
                [0, 0, 0],
                [1, 0, 0],
                [0, 0, 0],
                [0, 0, 0],
                [0, 0, 0],
                [0, 1, 1],
            ]),
            # `tonic_position`
            0,
            # `min_share`
            0.6,
            # `max_share`
            0.7,
            # `expected`
            1
        ),
        (
            # `roll`
            np.array([
                [1, 0, 0],
                [0, 0, 1],
                [0, 0, 0],
                [0, 1, 0],
                [0, 0, 0],
                [0, 1, 0],
                [0, 0, 1],
                [0, 0, 0],
                [0, 0, 0],
                [0, 0, 0],
                [0, 0, 0],
                [0, 0, 0],
                [0, 1, 1],
            ]),
            # `tonic_position`
            0,
            # `min_share`
            0.6,
            # `max_share`
            0.7,
            # `expected`
            0
        ),
    ]
)
def test_score_usage_of_tonic(
        roll: np.ndarray, tonic_position: int,
        min_share: float, max_share: float, expected: float
) -> None:
    """Test `score_usage_of_tonic` function."""
    result = score_usage_of_tonic(roll, tonic_position, min_share, max_share)
    assert result == expected

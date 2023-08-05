"""
Score a musical composition represented as a piano roll.

Here, a piano roll is a `numpy` 2D-array with rows corresponding to notes,
columns corresponding to time steps, and cells containing zeros and ones
and indicating whether a note is played.

References:
    https://en.wikipedia.org/wiki/Piano_roll#In_digital_audio_workstations

Author: Nikolay Lysenko
"""


from typing import Any, Callable, Dict, Optional

import numpy as np

from rlmusician.utils import (
    apply_rolling_aggregation, shift_horizontally, shift_vertically
)


N_SEMITONES_PER_OCTAVE = 12
DEFAULT_TONIC_POSITION = 4


def score_absence_of_outer_notes(
        roll: np.ndarray,
        scale: str = 'major',
        tonic_position: Optional[int] = None
) -> float:
    """
    Score composition based on absence of notes not from specified scale.

    :param roll:
        piano roll
    :param scale:
        name of scale
    :param tonic_position:
        number of the row (from bottom) that corresponds to the tonic
    :return:
        number of played notes not from the specified scale
        (with negative sign)
    """
    if tonic_position is None:
        tonic_position = DEFAULT_TONIC_POSITION  # pragma: no cover
    scale_to_wrong_notes = {
        'major': [0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0],
        'minor': [0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1]
    }
    mask = np.array(scale_to_wrong_notes[scale][::-1]).reshape((-1, 1))
    mask = np.tile(mask, (int(np.ceil(roll.shape[0] / mask.shape[0])), 1))
    mask = np.roll(mask, -tonic_position)
    mask = mask[-roll.shape[0]:, :]
    score = -np.sum(mask * roll).item()
    return score


def score_absence_of_stalled_notes(
        roll: np.ndarray, max_n_time_steps: int = 4
) -> float:
    """
    Score composition based on absence of notes played for too long time.

    It is a proxy of how non-trivial composition is.

    :param roll:
        piano roll
    :param max_n_time_steps:
        maximum duration of note in time steps, all that is longer is penalized
    :return:
        number of cells where sound event exceeds maximum allowed duration
        (with negative sign)
    """
    rolling_min_roll = apply_rolling_aggregation(
        roll, max_n_time_steps, fn_name='min'
    )
    ends_of_long_notes = np.minimum(roll, rolling_min_roll)
    score = -np.sum(ends_of_long_notes).item()
    return score


def score_conjunct_motion(
        roll: np.ndarray,
        max_n_semitones: int = 2,
        max_n_time_steps: int = 1
) -> float:
    """
    Score composition based on presence of small changes in pitch over time.

    :param roll:
        piano roll
    :param max_n_semitones:
        maximum number of semitones to consider change in pitch as small
    :param max_n_time_steps:
        maximum number of time steps for finding previous notes of close pitch
    :return:
        number of small changes in pitch
    """
    rolling_max_roll = apply_rolling_aggregation(
        roll, max_n_time_steps, fn_name='max'
    )
    altered_rolls = [
        shift_vertically(rolling_max_roll, i).reshape(roll.shape + (1,))
        for i in range(-max_n_semitones, max_n_semitones + 1)
        if i != 0
    ]
    altered_roll = np.concatenate(altered_rolls, axis=2)
    close_notes_roll = np.max(altered_roll, axis=2)
    starting_notes_roll = np.clip(roll - shift_horizontally(roll, 1), 0, None)
    matches = np.minimum(starting_notes_roll, close_notes_roll)
    score = np.sum(matches).item()
    return score


def compute_consonance_score_between_note_and_roll(
        note_timeline: np.ndarray,
        upper_roll: np.ndarray,
        interval_consonances: Dict[int, float]
) -> float:
    """
    Compute consonance score for a note's timeline and a roll of higher notes.

    It is a helper function for `score_consonances` function.

    :param note_timeline:
        array of shape (1, n_time_steps) with cells containing
        zeros if the note is not played and ones if it is played
    :param upper_roll:
        array of shape (n_higher_notes, n_time_steps) with rows corresponding
        to all notes that are higher than the note from `note_timeline`
    :param interval_consonances:
        mapping from interval in semitones to its score of consonance;
        keys must be all integers from 0 to 11, necessary number of octaves
        is subtracted for intervals higher than octave or equal to it
    :return:
        consonance score for the note and roll of all upper notes
    """
    intervals = ((note_timeline + upper_roll) > 1).astype(int)
    scores = [
        interval_consonances[n_semitones % N_SEMITONES_PER_OCTAVE]
        for n_semitones in range(intervals.shape[0], 0, -1)
    ]
    scores = np.array(scores).reshape((-1, 1))
    score = np.sum(scores * intervals).item()
    return score


def score_consonances(
        roll: np.ndarray,
        interval_consonances: Dict[int, float],
        distance_weights: Dict[int, float]
) -> float:
    """
    Score composition based on its consonances.

    It is a proxy of how pleasant to ear music is.

    :param roll:
        piano roll
    :param interval_consonances:
        mapping from interval in semitones to its score of consonance;
        keys must be all integers from 0 to 11, necessary number of octaves
        is subtracted for intervals greater than octave or equal to it
    :param distance_weights:
        mapping from distance in time steps between played notes and
        relative weights for averaging consonance scores;
        if distance is absent, consonance score between these notes is not
        accounted
    :return:
        weighted sum of consonance scores with summation over pairs of
        played notes that are close enough (according to `distance_weights`)
    """
    score = 0
    distances = list(distance_weights.keys())
    signed_distances = set(distances + [-x for x in distances])
    distance_weights = {k: distance_weights[abs(k)] for k in signed_distances}
    for note_position in range(1, roll.shape[0]):
        upper_roll = roll[:note_position, :]
        note_timeline = roll[note_position, :].reshape((1, -1))
        for distance, weight in distance_weights.items():
            shifted_timeline = shift_horizontally(note_timeline, distance)
            curr_score = compute_consonance_score_between_note_and_roll(
                shifted_timeline, upper_roll, interval_consonances
            )
            score += weight * curr_score
    return score


def score_contrary_motion(roll: np.ndarray) -> float:
    """
    Score composition based on number of time steps with contrary motion.

    Here, a time step has contrary motion if there are at least two lines
    moving in opposite directions.

    :param roll:
        piano roll
    :return:
        number of time steps with contrary motion
    """
    diff = np.diff(roll, axis=1, prepend=0)[:, 1:]
    cum_sums = np.cumsum(diff, axis=0)
    moves_down_penalty = np.abs(np.max(cum_sums, axis=0) - 1)
    moves_up_penalty = np.abs(np.min(cum_sums, axis=0) + 1)
    score = -np.sum((moves_down_penalty + moves_up_penalty) > 0).item()
    score += roll.shape[1]  # For the sake of interpretation.
    return score


def score_noncyclicity(
        roll: np.ndarray, max_n_time_steps: int = 8, max_share: float = 0.125
) -> float:
    """
    Score composition based on absence of cyclically repeated parts.

    It is a proxy of how non-trivial composition is.

    :param roll:
        piano roll
    :param max_n_time_steps:
        maximum duration of a fragment to be tested on cyclical repetitiveness
    :param max_share:
        upper limit on share of filled non-cyclically cells;
        values that are higher, are clipped
    :return:
        score from 0 to 1 that indicates how many cells are filled
        non-cyclically
    """
    upper_limit = max_share * roll.shape[0] * roll.shape[1]
    scores = []
    for shift in range(1, max_n_time_steps + 1):
        shifted_roll = shift_horizontally(roll, shift)
        diff = np.clip(roll - shifted_roll, a_min=0, a_max=None)
        score = min(np.sum(diff) / upper_limit, 1)
        scores.append(score)
    score = min(scores)
    return score


def score_number_of_simultaneously_played_notes(
        roll: np.ndarray, n_lines: int = 3
) -> float:
    """
    Score composition based on number of simultaneously played notes.

    It is a proxy for presence of desired number of melodic lines.

    :param roll:
        piano roll
    :param n_lines:
        desired number of melodic lines
    :return:
        negative sum over all time steps of absolute deviations
        of number of simultaneously played notes from the desired number
    """
    score = -np.sum(np.abs((np.sum(roll, axis=0) - n_lines))).item()
    return score


def score_usage_of_tonic(
        roll: np.ndarray,
        tonic_position: Optional[int] = None,
        min_share: float = 0.2,
        max_share: float = 0.4
) -> float:
    """
    Score composition based on proper usage of tonic in the lowest line.

    :param roll:
        piano roll
    :param tonic_position:
        number of the row (from bottom) that corresponds to the tonic
    :param min_share:
        minimum share of time steps with played in the lowest line tonic
        to consider the tonic actively used there
    :param max_share:
        maximum share of time steps with played in the lowest line tonic
        to consider the tonic excessively used there
    :return:
        binary indicator of whether tonic is used actively, but not excessively
        in the lowest line
    """
    if tonic_position is None:
        tonic_position = DEFAULT_TONIC_POSITION  # pragma: no cover

    cum_summed = np.cumsum(roll, axis=0)
    summed = np.sum(roll, axis=0).reshape((1, -1))
    not_above_lowest_line = cum_summed == summed
    lowest_line_roll = np.minimum(roll, not_above_lowest_line)

    remainder = (roll.shape[0] - 1) % N_SEMITONES_PER_OCTAVE
    tonic_indices = [
        x for x in range(roll.shape[0])
        if (x + tonic_position) % N_SEMITONES_PER_OCTAVE == remainder
    ]
    share = np.mean(np.max(lowest_line_roll[tonic_indices, :], axis=0)).item()
    score = 1 if min_share <= share <= max_share else 0
    return score


def get_scoring_functions_registry() -> Dict[str, Callable]:
    """
    Get mapping from names of scoring functions to scoring functions.

    :return:
        registry of scoring functions
    """
    registry = {
        'absence_of_outer_notes': score_absence_of_outer_notes,
        'absence_of_stalled_notes': score_absence_of_stalled_notes,
        'conjunct_motion': score_conjunct_motion,
        'consonances': score_consonances,
        'contrary_motion': score_contrary_motion,
        'lines': score_number_of_simultaneously_played_notes,
        'noncyclicity': score_noncyclicity,
        'usage_of_tonic': score_usage_of_tonic
    }
    return registry


def evaluate(
        roll: np.ndarray,
        scoring_coefs: Dict[str, float],
        scoring_fn_params: Dict[str, Any],
        verbose: bool = False
) -> float:
    """
    Evaluate piano roll.

    :param roll:
        piano roll
    :param scoring_coefs:
        mapping from scoring function names to their weights in final score
    :param scoring_fn_params:
        mapping from scoring function names to their parameters
    :param verbose:
        if it is set to `True`, scores by all functions are printed separately
    :return:
        overall score of piano roll quality
    """
    score = 0
    registry = get_scoring_functions_registry()
    for fn_name, weight in scoring_coefs.items():
        fn = registry[fn_name]
        curr_score = weight * fn(roll, **scoring_fn_params.get(fn_name, {}))
        if verbose:
            print(f'{fn_name:>25}: {curr_score}')  # pragma: no cover
        score += curr_score
    return score

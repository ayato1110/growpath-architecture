from datetime import date

import pytest

from app.schemas.profile import ProfileRequest
from app.services.profile import completeness_pct
from app.services.recommendation import CriterionScore, build_plan
from app.services.scoring import (
    ScoringError,
    round_score,
    score_answer,
    segment_for,
    weighted_average,
)

SINGLE_RULE = {
    "type": "single_choice",
    "options": [
        {"code": "low", "label": "Rendah", "points": 20},
        {"code": "high", "label": "Tinggi", "points": 100},
    ],
}

MULTI_RULE = {
    "type": "multi_select",
    "options": [
        {"code": "a", "label": "A", "points": 25},
        {"code": "b", "label": "B", "points": 25},
        {"code": "c", "label": "C", "points": 60},
        {"code": "none", "label": "Belum ada", "points": 0},
    ],
    "exclusive_codes": ["none"],
}

NUMERIC_RULE = {
    "type": "numeric",
    "unit": "orang",
    "buckets": [
        {"min": 0, "max": 1, "points": 0},
        {"min": 1, "max": 3, "points": 25},
        {"min": 3, "max": 6, "points": 50},
        {"min": 11, "points": 100},
    ],
}

SEGMENTS = [
    (1, "S1", 0.0, 30.0),
    (2, "S2", 30.0, 55.0),
    (3, "S3", 55.0, 80.0),
    (4, "S4", 80.0, 100.0),
]


def test_single_choice_returns_option_points():
    result = score_answer("enum", SINGLE_RULE, {"option": "high"})
    assert result.score == 100
    assert result.raw_value == {"option": "high"}


def test_single_choice_rejects_unknown_option():
    with pytest.raises(ScoringError):
        score_answer("enum", SINGLE_RULE, {"option": "missing"})


def test_multi_select_sums_points_and_caps_at_100():
    result = score_answer("multi_select", MULTI_RULE, {"options": ["a", "b", "c"]})
    assert result.score == 100


def test_multi_select_rejects_empty_selection():
    with pytest.raises(ScoringError):
        score_answer("multi_select", MULTI_RULE, {"options": []})


def test_multi_select_exclusive_option_cannot_mix():
    with pytest.raises(ScoringError):
        score_answer("multi_select", MULTI_RULE, {"options": ["none", "a"]})


def test_numeric_bucket_lower_bound_inclusive_upper_exclusive():
    assert score_answer("number", NUMERIC_RULE, {"value": 0}).score == 0
    assert score_answer("number", NUMERIC_RULE, {"value": 1}).score == 25
    assert score_answer("number", NUMERIC_RULE, {"value": 2.9}).score == 25
    assert score_answer("number", NUMERIC_RULE, {"value": 3}).score == 50
    assert score_answer("number", NUMERIC_RULE, {"value": 30}).score == 100


def test_numeric_rejects_negative_value():
    with pytest.raises(ScoringError):
        score_answer("number", NUMERIC_RULE, {"value": -1})


def test_boolean_scores_100_or_0():
    assert score_answer("boolean", {}, {"value": True}).score == 100
    assert score_answer("boolean", {}, {"value": False}).score == 0


def test_weighted_average_ignores_unweighted_gap():
    assert weighted_average([(1, 100), (1, 0)]) == 50
    assert weighted_average([(2, 100), (1, 40)]) == 80
    assert weighted_average([]) == 0


def test_round_score_uses_two_decimals():
    assert round_score(33.333333) == 33.33
    assert round_score(79.995) == 80.0


@pytest.mark.parametrize(
    ("score", "expected"),
    [
        (0, "S1"),
        (29.99, "S1"),
        (30, "S2"),
        (54.99, "S2"),
        (55, "S3"),
        (79.99, "S3"),
        (80, "S4"),
        (100, "S4"),
    ],
)
def test_segment_boundaries_are_lower_inclusive(score, expected):
    assert segment_for(score, SEGMENTS)[1] == expected


def test_segment_raises_outside_range():
    with pytest.raises(ScoringError):
        segment_for(100.01, SEGMENTS)


def test_completeness_counts_ten_demographic_fields():
    payload = ProfileRequest(
        business_name="Puding Coklat",
        owner_name="Hambali",
        sector="kuliner",
        established_year=2018,
        operation_months=60,
    )
    assert completeness_pct(payload) == 50.0


def test_plan_picks_three_lowest_scores_in_order():
    plan = build_plan(
        [
            CriterionScore(1, "PAS-01", "Branding", "Pasar", 80, 1),
            CriterionScore(2, "PAS-07", "Pesaing", "Pasar", 25, 7),
            CriterionScore(3, "PSY-01", "Motif", "Psikografi", 20, 1),
            CriterionScore(4, "PAS-03", "Cakupan", "Pasar", 25, 3),
        ],
        scored_on=date(2026, 11, 27),
    )
    assert [item.title for item in plan] == [
        "Tegaskan tujuan usaha",
        "Perluas cakupan pasar bertahap",
        "Riset tiga pesaing terdekat",
    ]
    assert [item.due_date for item in plan] == [
        date(2026, 12, 11),
        date(2026, 12, 25),
        date(2027, 1, 8),
    ]

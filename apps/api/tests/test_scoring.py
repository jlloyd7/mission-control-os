from app.services.scoring_service import weighted_part_score


def test_weighted_score_is_deterministic():
    value = weighted_part_score(8, 8, 7, 7, 5, 3, 4)
    expected = round(
        8 * 1.5 + 8 * 1.3 + 7 * 1.0 + 7 * 1.2 + 5 * 0.8 - 3 * 1.2 - 4 * 0.8, 2
    )
    assert value == expected


def test_high_risk_lowers_score():
    low_risk = weighted_part_score(8, 8, 7, 7, 5, 1, 4)
    high_risk = weighted_part_score(8, 8, 7, 7, 5, 10, 4)
    assert high_risk < low_risk


def test_high_user_value_raises_score():
    low = weighted_part_score(1, 5, 5, 5, 5, 5, 5)
    high = weighted_part_score(10, 5, 5, 5, 5, 5, 5)
    assert high > low

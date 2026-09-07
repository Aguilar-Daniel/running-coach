from app.services.pr_matching import match_distance_category

def test_exact_distance_match():
    assert match_distance_category(5000) == '5k'
    assert match_distance_category(42195) == 'marathon'

def test_inside_tolerance_band():
    assert match_distance_category(4901) == '5k'
    assert match_distance_category(5088) == '5k'

def test_outside_tolerance_band():
    assert match_distance_category(4000) is None
    assert match_distance_category(6437) is None


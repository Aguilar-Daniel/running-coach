import pytest
from app.services.pace import calculate_pace_seconds_per_km

def test_calculates_correct_pace():
    assert calculate_pace_seconds_per_km(5000, 1500) == 300

def test_does_not_accept_zero_distance():
    with pytest.raises(ValueError):
        calculate_pace_seconds_per_km(0, 1500)
    

def test_does_not_accept_negative_distance():
    with pytest.raises(ValueError):
        calculate_pace_seconds_per_km(-15, 1500)
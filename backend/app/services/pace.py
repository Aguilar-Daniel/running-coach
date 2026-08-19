def calculate_pace_seconds_per_km(distance_meters, duration_seconds):
    if distance_meters <= 0 or duration_seconds <= 0:
        raise ValueError('Invalid distance or time')
    km = distance_meters / 1000
    return duration_seconds / km


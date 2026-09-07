distance_categories = {
        '1mi': 1609,
        '2mi': 3218,
        '5k': 5000,
        '10k': 10000,
        'half_marathon': 21097,
        'marathon': 42195
    }

def match_distance_category(distance_meters):
    for category, distance in distance_categories.items():
        lower_limit = distance - distance * 0.02 
        upper_limit = distance + distance * 0.02    
        if distance_meters <= upper_limit and distance_meters >= lower_limit:
            return category
        
    return None    
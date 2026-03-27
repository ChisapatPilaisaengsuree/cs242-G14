def rank_results(restrooms):
    priority = {"low": 1, "medium": 2, "high": 3}
    return sorted(restrooms, key=lambda x: priority.get(x.crowd_level, 3))
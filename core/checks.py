import math

def distance(p1, p2):
    return math.sqrt(
        (p1.x - p2.x) ** 2 +
        (p1.y - p2.y) ** 2 +
        (p1.z - p2.z) ** 2
    )

def spatial_conflict(p1, p2, safe_dist):
    return distance(p1, p2) < safe_dist

def temporal_overlap(t1, t2, threshold=1.0):
    return abs(t1 - t2) <= threshold

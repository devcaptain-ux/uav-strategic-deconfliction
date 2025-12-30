from core.checks import temporal_overlap, distance

def check_conflicts(primary_traj, other_drones, safe_dist=10.0):
    closest_conflict = None
    min_distance = float("inf")

    for drone in other_drones:
        for p in primary_traj:
            for q in drone["trajectory"]:
                if temporal_overlap(p.t, q.t):
                    dist = distance(p, q)

                    if dist < safe_dist and dist < min_distance:
                        min_distance = dist
                        closest_conflict = {
                            "time": p.t,
                            "location": (p.x, p.y, p.z),
                            "with": drone["id"],
                            "distance": round(dist, 2)
                        }

    if closest_conflict:
        return "CONFLICT", [closest_conflict]

    return "CLEAR", None

import json
from core.trajectory import Waypoint, build_trajectory
from core.conflict_engine import check_conflicts
from visualization.animate_3d_pro import animate_3d_pro

with open("data/simulated_flights.json") as f:
    data = json.load(f)

drones = []
for d in data["drones"]:
    wps = [Waypoint(**wp) for wp in d["waypoints"]]
    drones.append({
        "id": d["id"],
        "trajectory": build_trajectory(wps)
    })

primary = drones[0]
others = drones[1:]

status, conflicts = check_conflicts(primary["trajectory"], others)

print("MISSION STATUS:", status)
if conflicts:
    for c in conflicts:
        print(c)

animate_3d_pro(primary, others, conflicts)

from dataclasses import dataclass

@dataclass
class Waypoint:
    x: float
    y: float
    z: float
    t: float

def interpolate(wp1, wp2, step=1.0):
    traj = []
    steps = int((wp2.t - wp1.t) / step)
    for i in range(steps + 1):
        a = i / steps if steps else 0
        traj.append(Waypoint(
            x=wp1.x + a * (wp2.x - wp1.x),
            y=wp1.y + a * (wp2.y - wp1.y),
            z=wp1.z + a * (wp2.z - wp1.z),
            t=wp1.t + a * (wp2.t - wp1.t)
        ))
    return traj

def build_trajectory(waypoints):
    traj = []
    for i in range(len(waypoints) - 1):
        traj.extend(interpolate(waypoints[i], waypoints[i + 1]))
    return traj

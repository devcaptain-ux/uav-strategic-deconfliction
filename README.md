#  UAV Strategic Deconfliction System (4D)

This project implements a **4D (3D + Time) UAV Strategic Deconfliction System** that verifies whether a drone mission is safe to execute in shared airspace by detecting spatio-temporal conflicts with other drones.

---

##  Features
- Waypoint-based UAV mission planning
- 3D trajectory interpolation
- Time-aware conflict detection
- Safety buffer enforcement
- Conflict explanation (time, location, distance, drone ID)
- Professional 4D animated visualization
- MP4 video export using FFmpeg

---

##  Conflict Detection Logic
Conflicts are detected when:
- Two drones occupy overlapping time windows, and
- Their 3D Euclidean distance falls below a safety threshold

---

##  Visualization
- Animated 3D trajectories
- Safety spheres
- Conflict markers
- CLEAR / CONFLICT status indicators

---

##  Installation

```bash
pip install -r requirements.txt

FFmpeg (for MP4 export)

Download and install FFmpeg from:
https://www.gyan.dev/ffmpeg/builds/

Ensure ffmpeg.exe path is correctly set in animate_3d_pro.py.

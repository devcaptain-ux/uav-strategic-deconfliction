import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.patches import FancyBboxPatch
import matplotlib.patches as mpatches

class Point:
    def __init__(self, x, y, z, t=0):
        self.x = x
        self.y = y
        self.z = z
        self.t = t

def create_smooth_trajectory(waypoints, num_points=100):
    """Create smooth trajectory using cubic interpolation"""
    t = np.linspace(0, 1, len(waypoints))
    t_new = np.linspace(0, 1, num_points)
    
    x = np.array([p.x for p in waypoints])
    y = np.array([p.y for p in waypoints])
    z = np.array([p.z for p in waypoints])
    
    x_smooth = np.interp(t_new, t, x)
    y_smooth = np.interp(t_new, t, y)
    z_smooth = np.interp(t_new, t, z)
    
    return [Point(x_smooth[i], y_smooth[i], z_smooth[i], i) for i in range(num_points)]

def detect_conflicts(primary, others, safe_radius, time_window=5):
    """Detect potential conflicts between drones"""
    conflicts = []
    
    for frame in range(min(len(primary), min(len(d["trajectory"]) for d in others))):
        p = primary[frame]
        for drone in others:
            if frame < len(drone["trajectory"]):
                o = drone["trajectory"][frame]
                dist = np.sqrt((p.x - o.x)**2 + (p.y - o.y)**2 + (p.z - o.z)**2)
                
                if dist < safe_radius * 1.5:
                    conflicts.append({
                        "time": frame,
                        "location": [(p.x + o.x)/2, (p.y + o.y)/2, (p.z + o.z)/2],
                        "distance": dist,
                        "drone_id": drone["id"]
                    })
    
    return conflicts

def animate_3d_pro(primary, others, conflicts=None, safe_radius=10, save_video=False):
    """
    Professional 4D UAV Strategic Deconfliction Animation
    
    Parameters:
    - primary: dict with 'trajectory' (list of Point objects)
    - others: list of dicts, each with 'id' and 'trajectory'
    - conflicts: list of conflict events (optional, auto-detected if None)
    - safe_radius: safety bubble radius in meters
    - save_video: whether to save as MP4 (requires ffmpeg)
    """
    
    # Auto-detect conflicts if not provided
    if conflicts is None:
        conflicts = detect_conflicts(primary["trajectory"], others, safe_radius)
    
    # Setup figure with dark theme for professional look
    plt.style.use('dark_background')
    fig = plt.figure(figsize=(14, 10), facecolor='#0a0a0a')
    ax = fig.add_subplot(111, projection='3d', facecolor='#0a0a0a')
    
    # Axis configuration
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.set_zlim(0, 40)
    
    ax.set_xlabel("X Position (m)", fontsize=10, color='white', labelpad=10)
    ax.set_ylabel("Y Position (m)", fontsize=10, color='white', labelpad=10)
    ax.set_zlabel("Altitude (m)", fontsize=10, color='white', labelpad=10)
    
    # Grid styling
    ax.grid(True, alpha=0.2, linestyle='--', linewidth=0.5)
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    
    # Title
    title = ax.text2D(0.5, 0.97, "4D UAV Strategic Deconfliction System", 
                      transform=ax.transAxes, ha='center', fontsize=16, 
                      color='cyan', weight='bold')
    
    # Primary drone elements
    p_traj = primary["trajectory"]
    p_line, = ax.plot([], [], [], lw=3, color="#00BFFF", label="Primary UAV", alpha=0.8)
    p_dot = ax.scatter([], [], [], s=150, color="#00BFFF", marker='o', 
                       edgecolors='white', linewidth=2, depthshade=False)
    
    # Trail fade effect
    p_trail, = ax.plot([], [], [], lw=1.5, color="#00BFFF", alpha=0.3)
    
    # Safety sphere
    u, v = np.mgrid[0:2*np.pi:30j, 0:np.pi:15j]
    
    # Other drones with distinct colors
    colors = ['#FF1493', '#00FF00', '#FFD700', '#FF4500', '#9370DB']
    o_lines = []
    o_dots = []
    o_trails = []
    
    for i, d in enumerate(others):
        color = colors[i % len(colors)]
        line, = ax.plot([], [], [], lw=2.5, color=color, label=d["id"], alpha=0.7)
        trail, = ax.plot([], [], [], lw=1, color=color, alpha=0.2)
        dot = ax.scatter([], [], [], s=100, color=color, marker='o', 
                        edgecolors='white', linewidth=1.5, depthshade=False)
        o_lines.append(line)
        o_dots.append(dot)
        o_trails.append(trail)
    
    # Conflict warning marker
    conflict_dot = ax.scatter([], [], [], s=300, color="red", marker="X", 
                             edgecolors='yellow', linewidth=2, alpha=0, depthshade=False)
    
    # Legend
    ax.legend(loc='upper left', fontsize=9, framealpha=0.7)
    
    # Info text
    info_text = ax.text2D(0.02, 0.02, "", transform=ax.transAxes, 
                         fontsize=10, color='white', verticalalignment='bottom',
                         bbox=dict(boxstyle='round', facecolor='black', alpha=0.5))
    
    # Status indicator
    status_text = ax.text2D(0.98, 0.95, "", transform=ax.transAxes, 
                           fontsize=11, color='lime', verticalalignment='top',
                           horizontalalignment='right', weight='bold')
    
    def update(frame):
        trail_length = 20  # How many frames to show in trail
        
        # Primary drone trajectory
        px = [p.x for p in p_traj[:frame+1]]
        py = [p.y for p in p_traj[:frame+1]]
        pz = [p.z for p in p_traj[:frame+1]]
        
        p_line.set_data(px, py)
        p_line.set_3d_properties(pz)
        
        # Trail effect
        trail_start = max(0, frame - trail_length)
        trail_px = [p.x for p in p_traj[trail_start:frame+1]]
        trail_py = [p.y for p in p_traj[trail_start:frame+1]]
        trail_pz = [p.z for p in p_traj[trail_start:frame+1]]
        p_trail.set_data(trail_px, trail_py)
        p_trail.set_3d_properties(trail_pz)
        
        # Primary drone current position
        if frame < len(p_traj):
            p = p_traj[frame]
            p_dot._offsets3d = ([p.x], [p.y], [p.z])
            
            # Safety sphere (draw every 3 frames for performance)
            if frame % 3 == 0:
                xs = safe_radius * np.cos(u) * np.sin(v) + p.x
                ys = safe_radius * np.sin(u) * np.sin(v) + p.y
                zs = safe_radius * np.cos(v) + p.z
                
                # Remove old sphere
                for collection in ax.collections[len(others)+2:]:
                    collection.remove()
                
                ax.plot_wireframe(xs, ys, zs, color="cyan", alpha=0.12, 
                                linewidth=0.5, linestyle=':')
        
        # Other drones
        for i, d in enumerate(others):
            traj = d["trajectory"]
            ox = [pt.x for pt in traj[:frame+1]]
            oy = [pt.y for pt in traj[:frame+1]]
            oz = [pt.z for pt in traj[:frame+1]]
            
            o_lines[i].set_data(ox, oy)
            o_lines[i].set_3d_properties(oz)
            
            # Trail
            trail_start = max(0, frame - trail_length)
            trail_ox = [pt.x for pt in traj[trail_start:frame+1]]
            trail_oy = [pt.y for pt in traj[trail_start:frame+1]]
            trail_oz = [pt.z for pt in traj[trail_start:frame+1]]
            o_trails[i].set_data(trail_ox, trail_oy)
            o_trails[i].set_3d_properties(trail_oz)
            
            if frame < len(d["trajectory"]):
                pt = d["trajectory"][frame]
                o_dots[i]._offsets3d = ([pt.x], [pt.y], [pt.z])
        
        # Conflict detection and warning
        active_conflict = False
        conflict_info = ""
        
        for c in conflicts:
            if abs(c["time"] - frame) < 8:
                active_conflict = True
                # Pulsing effect
                pulse = 0.5 + 0.5 * np.sin(frame * 0.5)
                conflict_dot._offsets3d = (
                    [c["location"][0]],
                    [c["location"][1]],
                    [c["location"][2]]
                )
                conflict_dot.set_alpha(pulse * 0.8)
                
                if abs(c["time"] - frame) < 3:
                    conflict_info = f"⚠ CONFLICT ALERT\nDistance: {c['distance']:.1f}m\nDrone: {c['drone_id']}"
                    status_text.set_text("⚠ CONFLICT")
                    status_text.set_color('red')
                break
        
        if not active_conflict:
            conflict_dot.set_alpha(0)
            status_text.set_text("✓ CLEAR")
            status_text.set_color('lime')
        
        # Update info text
        progress = (frame / len(p_traj)) * 100
        info_text.set_text(
            f"Time: {frame}/{len(p_traj)} frames\n"
            f"Progress: {progress:.1f}%\n"
            f"Active UAVs: {len(others) + 1}\n"
            f"{conflict_info}"
        )
        
        # Smooth camera rotation
        elevation = 25 + 5 * np.sin(frame * 0.02)
        azimuth = frame * 0.3
        ax.view_init(elev=elevation, azim=azimuth)
        
        return [p_line, p_dot, p_trail, info_text, status_text, conflict_dot] + o_lines + o_dots + o_trails
    
    # Create animation
    frames = len(p_traj)
    ani = FuncAnimation(
        fig,
        update,
        frames=frames,
        interval=50,  # 20 FPS
        blit=False,
        repeat=True
    )
    
    # Save video if requested
    if save_video:
        print("Saving animation... This may take a few minutes.")
        ani.save(
            "uav_4d_deconfliction_PRO.mp4",
            writer="ffmpeg",
            fps=20,
            dpi=150,
            bitrate=5000
        )
        print("Animation saved as 'uav_4d_deconfliction_PRO.mp4'")
    
    plt.tight_layout()
    plt.show()
    
    return ani


# Example usage with demo data
if __name__ == "__main__":
    # Create sample trajectories
    primary_waypoints = [
        Point(10, 10, 5),
        Point(30, 25, 15),
        Point(50, 50, 25),
        Point(70, 70, 20),
        Point(90, 85, 10)
    ]
    
    primary = {
        "trajectory": create_smooth_trajectory(primary_waypoints, num_points=150)
    }
    
    # Other drones
    others = [
        {
            "id": "UAV-Alpha",
            "trajectory": create_smooth_trajectory([
                Point(80, 20, 10),
                Point(60, 40, 20),
                Point(45, 55, 25),
                Point(30, 70, 15),
                Point(15, 80, 8)
            ], num_points=150)
        },
        {
            "id": "UAV-Beta",
            "trajectory": create_smooth_trajectory([
                Point(20, 80, 12),
                Point(40, 60, 18),
                Point(55, 45, 22),
                Point(75, 30, 25),
                Point(90, 20, 15)
            ], num_points=150)
        }
    ]
    
    # Run animation
    animate_3d_pro(primary, others, safe_radius=12, save_video=False)
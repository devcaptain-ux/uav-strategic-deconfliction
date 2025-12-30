import matplotlib.pyplot as plt

def plot_2d(primary, others, conflicts):
    plt.figure(figsize=(8, 8))

    px = [p.x for p in primary["trajectory"]]
    py = [p.y for p in primary["trajectory"]]
    plt.plot(px, py, 'b-', linewidth=3, label="Primary Drone")

    for d in others:
        ox = [p.x for p in d["trajectory"]]
        oy = [p.y for p in d["trajectory"]]
        plt.plot(ox, oy, '--', label=d["id"])

    if conflicts:
        cx = [c["location"][0] for c in conflicts]
        cy = [c["location"][1] for c in conflicts]
        plt.scatter(cx, cy, c='red', s=100, label="Conflict")

    plt.title("UAV Strategic Deconfliction (2D)")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.legend()
    plt.grid()
    plt.show()

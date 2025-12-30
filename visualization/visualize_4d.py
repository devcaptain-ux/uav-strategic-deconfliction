import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def plot_4d(primary, others, conflicts):
    fig = plt.figure(figsize=(9, 7))
    ax = fig.add_subplot(111, projection='3d')

    for d in [primary] + others:
        xs = [p.x for p in d["trajectory"]]
        ys = [p.y for p in d["trajectory"]]
        zs = [p.z for p in d["trajectory"]]
        ax.plot(xs, ys, zs, label=d["id"])

    if conflicts:
        cx = [c["location"][0] for c in conflicts]
        cy = [c["location"][1] for c in conflicts]
        cz = [c["location"][2] for c in conflicts]
        ax.scatter(cx, cy, cz, c='red', s=80, label="Conflict")

    ax.set_title("4D UAV Deconfliction (3D Space + Time)")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Altitude")
    ax.legend()
    plt.show()

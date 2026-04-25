#!/usr/bin/env python3
import numpy as np


def plot_packing(extra_data):
    import matplotlib.pyplot as plt
    from matplotlib.patches import Circle, Rectangle

    centers = np.asarray(extra_data["centers"], dtype=float)
    radii = np.asarray(extra_data["radii"], dtype=float)
    reported_sum = float(extra_data["reported_sum"])

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.add_patch(Rectangle((0, 0), 1, 1, fill=False, edgecolor="black", linewidth=1.5))

    for i, (center, radius) in enumerate(zip(centers, radii)):
        ax.add_patch(Circle(center, radius, alpha=0.5))
        ax.text(center[0], center[1], str(i), ha="center", va="center", fontsize=7)

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect("equal")
    ax.grid(True, alpha=0.2)
    ax.set_title(f"Circle Packing (n={len(radii)}, sum={reported_sum:.6f})")
    fig.tight_layout()
    return [(fig, "packing")]

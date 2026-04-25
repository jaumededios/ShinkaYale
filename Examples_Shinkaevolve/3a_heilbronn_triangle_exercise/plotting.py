#!/usr/bin/env python3
import itertools

import numpy as np


SQRT3 = np.sqrt(3.0)
TRIANGLE_HEIGHT = SQRT3 / 2.0


def triangle_area(points, combo):
    a, b, c = points[list(combo)]
    doubled_area = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
    return float(abs(doubled_area) / 2.0)


def close_triangles(points, tolerance=0.05):
    triangles = [
        (combo, triangle_area(points, combo))
        for combo in itertools.combinations(range(len(points)), 3)
    ]
    min_area = min(area for _, area in triangles)
    cutoff = min_area * (1.0 + tolerance)
    return [(combo, area) for combo, area in triangles if area <= cutoff], min_area


def plot_heilbronn(extra_data):
    import matplotlib.pyplot as plt
    from matplotlib.patches import Polygon

    points = np.asarray(extra_data["points"], dtype=float)
    boundary = np.array([[0.0, 0.0], [1.0, 0.0], [0.5, TRIANGLE_HEIGHT], [0.0, 0.0]])
    triangles, min_area = close_triangles(points)

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.plot(boundary[:, 0], boundary[:, 1], color="black", linewidth=1.5)

    for combo, area in triangles:
        is_smallest = abs(area - min_area) < 1e-12
        ax.add_patch(
            Polygon(
                points[list(combo)],
                closed=True,
                facecolor=(1.0, 0.0, 0.0, 0.25 if is_smallest else 0.08),
                edgecolor=(1.0, 0.0, 0.0, 1.0 if is_smallest else 0.35),
                linewidth=2.0 if is_smallest else 1.0,
                zorder=1,
            )
        )

    ax.scatter(points[:, 0], points[:, 1], color="C1", s=40, zorder=3)

    ax.set_aspect("equal")
    ax.set_xlim(-0.02, 1.02)
    ax.set_ylim(-0.02, TRIANGLE_HEIGHT + 0.02)
    ax.axis("off")
    fig.tight_layout()
    return [(fig, "heilbronn_points")]

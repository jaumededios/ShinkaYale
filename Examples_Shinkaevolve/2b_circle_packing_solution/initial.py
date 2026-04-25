# EVOLVE-BLOCK-START
"""Simple deterministic baseline for packing 26 circles in a unit square."""

import numpy as np


def construct_packing(seed: int = 0):
    """
    Place circles on four fixed rows with a small shared radius.
    The seed is accepted for compatibility but unused by this baseline.
    """
    _ = seed
    rows = [
        (0.12, np.linspace(0.08, 0.92, 7)),
        (0.37, np.linspace(0.15, 0.85, 6)),
        (0.63, np.linspace(0.15, 0.85, 6)),
        (0.88, np.linspace(0.08, 0.92, 7)),
    ]
    centers = np.array([(x, y) for y, xs in rows for x in xs], dtype=float)
    radii = np.full(26, 0.02, dtype=float)
    return centers, radii



# EVOLVE-BLOCK-END


def verify_packing(centers, radii, atol: float = 1e-12):
    """Helper function that returns whether the packing is admissible."""
    centers = np.asarray(centers, dtype=float)
    radii = np.asarray(radii, dtype=float)

    if centers.shape != (26, 2) or radii.shape != (26,):
        return False
    if not (np.all(np.isfinite(centers)) and np.all(np.isfinite(radii))):
        return False
    if np.any(radii < 0.0):
        return False
    if np.any(centers[:, 0] - radii < -atol) or \
       np.any(centers[:, 0] + radii > 1.0 + atol) or \
       np.any(centers[:, 1] - radii < -atol) or \
       np.any(centers[:, 1] + radii > 1.0 + atol):
        return False

    for i in range(len(centers)):
        for j in range(i + 1, len(centers)):
            distance = np.linalg.norm(centers[i] - centers[j])
            if distance < radii[i] + radii[j] - atol:
                return False
    return True


def run_packing(seed: int = 0):
    """Stable evaluator entrypoint for this deterministic starter."""
    centers, radii = construct_packing(seed=seed)
    return centers, radii, np.sum(radii)

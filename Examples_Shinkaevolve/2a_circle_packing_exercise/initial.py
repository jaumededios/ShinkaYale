# EVOLVE-BLOCK-START
"""Simple deterministic baseline for packing 26 circles in a unit square."""

import numpy as np


def construct_packing(seed: int = 0):
    """
    Place circles on four fixed rows with a small shared radius.
    The seed is accepted for compatibility but unused by this baseline.
    """
    pass


# EVOLVE-BLOCK-END


def verify_packing(centers, radii, atol: float = 1e-12):
    """Helper function that returns whether the packing is admissible."""
    pass


def run_packing(seed: int = 0):
    """Stable evaluator entrypoint for this deterministic starter."""
    centers, radii = construct_packing(seed=seed)
    return centers, radii, np.sum(radii)

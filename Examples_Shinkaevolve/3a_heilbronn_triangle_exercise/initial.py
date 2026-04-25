import itertools

import numpy as np

# EVOLVE-BLOCK-START


def search_points(
    seed: int = 0,
    num_points: int = 11,
    num_candidates: int = 300,
):
    """
    Write a construction that returns:
    - `points`: an array of shape (num_points, 2) inside the triangle
    - `score`: the corresponding normalized minimum triangle area

    A simple random-search baseline is enough to get started: sample valid
    point sets in the triangle, score them with
    `min_triangle_area_normalized(points)`, and keep the best one.
    """
    pass


# EVOLVE-BLOCK-END


SQRT3 = np.sqrt(3.0)
TRIANGLE_AREA = SQRT3 / 4.0


def sample_points_in_triangle(rng, num_points: int) -> np.ndarray:
    """Uniform points in the triangle with vertices (0, 0), (1, 0), (0.5, sqrt(3)/2)."""
    uv = rng.random((num_points, 2))
    mask = np.sum(uv, axis=1) > 1.0
    uv[mask] = 1.0 - uv[mask]

    x = uv[:, 0] + 0.5 * uv[:, 1]
    y = 0.5 * SQRT3 * uv[:, 1]
    return np.column_stack([x, y])


def triangle_area(a, b, c) -> float:
    pass


def min_triangle_area_normalized(points) -> float:
    pass


def run_heilbronn(seed: int = 0, num_points: int = 11):
    """Stable evaluator entrypoint."""
    return search_points(seed=seed, num_points=num_points)


if __name__ == "__main__":
    points, score = run_heilbronn()
    print(f"n_points={len(points)} normalized_min_area={score:.6f}")

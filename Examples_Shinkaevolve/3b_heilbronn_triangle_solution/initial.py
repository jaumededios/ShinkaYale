import itertools

import numpy as np

# EVOLVE-BLOCK-START


def search_points(
    seed: int = 0,
    num_points: int = 11,
    num_candidates: int = 300,
):
    """Sample random point sets and keep the one with the largest minimum area."""
    rng = np.random.default_rng(seed)
    best_points = sample_points_in_triangle(rng, num_points)
    best_score = min_triangle_area_normalized(best_points)

    for _ in range(num_candidates - 1):
        points = sample_points_in_triangle(rng, num_points)
        score = min_triangle_area_normalized(points)
        if score > best_score:
            best_points = points
            best_score = score

    return best_points, best_score


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
    doubled_area = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
    return float(abs(doubled_area) / 2.0)


def min_triangle_area_normalized(points) -> float:
    points = np.asarray(points, dtype=float)
    min_area = min(triangle_area(a, b, c) for a, b, c in itertools.combinations(points, 3))
    return float(min_area / TRIANGLE_AREA)


def run_heilbronn(seed: int = 0, num_points: int = 11):
    """Stable evaluator entrypoint."""
    return search_points(seed=seed, num_points=num_points)


if __name__ == "__main__":
    points, score = run_heilbronn()
    print(f"n_points={len(points)} normalized_min_area={score:.6f}")

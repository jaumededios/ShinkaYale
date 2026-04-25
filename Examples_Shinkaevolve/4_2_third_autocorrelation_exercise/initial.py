import numpy as np

# EVOLVE-BLOCK-START

def search_function(
    seed: int = 0,
    num_points: int = 400,
    num_blocks: int = 8,
    num_candidates: int = 400,
):
    """
    Simple baseline: random search over signed piecewise-constant step functions.
    """
    rng = np.random.default_rng(seed)
    best_values = np.ones(num_points, dtype=float)
    best_c3 = compute_c3(best_values)

    for _ in range(num_candidates):
        block_values = rng.uniform(-1.0, 1.0, size=num_blocks)
        values = expand_blocks(block_values, num_points)
        c3 = compute_c3(values)
        if np.isfinite(c3) and c3 < best_c3:
            best_values = values
            best_c3 = c3

    return best_values, best_c3


# EVOLVE-BLOCK-END


def expand_blocks(block_values, num_points: int) -> np.ndarray:
    block_values = np.asarray(block_values, dtype=float)
    counts = np.full(len(block_values), num_points // len(block_values), dtype=int)
    counts[: num_points % len(block_values)] += 1
    return np.repeat(block_values, counts)


def compute_c3(f_values) -> float:
    f_values = np.asarray(f_values, dtype=float)
    dx = 0.5 / len(f_values)
    integral = float(np.sum(f_values) * dx)

    if abs(integral) < 1e-12:
        return float("inf")

    conv = np.convolve(f_values, f_values, mode="full") * dx
    return float(np.max(np.abs(conv)) / (integral**2))


def run_autocorrelation(seed: int = 0, num_points: int = 400):
    """Stable evaluator entrypoint."""
    return search_function(seed=seed, num_points=num_points)


if __name__ == "__main__":
    f_values, c3 = run_autocorrelation()
    print(f"n_points={len(f_values)} c3={c3:.6f}")

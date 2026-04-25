import numpy as np

# EVOLVE-BLOCK-START

def search_function(
    seed: int = 0,
    num_points: int = 400,
    num_blocks: int = 8,
    num_candidates: int = 400,
):
    """
    Simple baseline: random search over NON-NEGATIVE piecewise-constant
    step functions. This is the same kind of search as in the (signed)
    third-autocorrelation problem, but we clamp the block values to be
    non-negative so the problem is the proper Sidon-like analogue.
    """
    rng = np.random.default_rng(seed)
    best_values = np.ones(num_points, dtype=float)
    best_c1 = compute_c1(best_values)

    for _ in range(num_candidates):
        block_values = rng.uniform(0.0, 1.0, size=num_blocks)
        values = expand_blocks(block_values, num_points)
        c1 = compute_c1(values)
        if np.isfinite(c1) and c1 < best_c1:
            best_values = values
            best_c1 = c1

    return best_values, best_c1


# EVOLVE-BLOCK-END


def expand_blocks(block_values, num_points: int) -> np.ndarray:
    block_values = np.asarray(block_values, dtype=float)
    counts = np.full(len(block_values), num_points // len(block_values), dtype=int)
    counts[: num_points % len(block_values)] += 1
    return np.repeat(block_values, counts)


def compute_c1(f_values) -> float:
    f_values = np.asarray(f_values, dtype=float)
    dx = 0.5 / len(f_values)
    integral = float(np.sum(f_values) * dx)

    if abs(integral) < 1e-12:
        return float("inf")

    conv = np.convolve(f_values, f_values, mode="full") * dx
    return float(np.max(conv) / (integral**2))


def run_autocorrelation(seed: int = 0, num_points: int = 400):
    """Stable evaluator entrypoint."""
    return search_function(seed=seed, num_points=num_points)


if __name__ == "__main__":
    f_values, c1 = run_autocorrelation()
    print(f"n_points={len(f_values)} c1={c1:.6f}")

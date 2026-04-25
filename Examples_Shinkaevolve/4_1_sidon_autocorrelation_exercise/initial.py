import numpy as np

# EVOLVE-BLOCK-START

def search_function(
    seed: int = 0,
    num_points: int = 400,
    num_blocks: int = 8,
    num_candidates: int = 400,
):
    """
    Write a construction that returns:
    - `f_values`: a 1D array of step-function values
    - `c1`: the ratio max(f * f) / (integral(f) ** 2)

    The key constraint for this exercise is that `f_values` must be
    non-negative. A simple block-based search is enough to get started:
    sample a few non-negative piecewise-constant candidates, score them,
    and keep the best one.
    """
    pass


# EVOLVE-BLOCK-END


def expand_blocks(block_values, num_points: int) -> np.ndarray:
    block_values = np.asarray(block_values, dtype=float)
    counts = np.full(len(block_values), num_points // len(block_values), dtype=int)
    counts[: num_points % len(block_values)] += 1
    return np.repeat(block_values, counts)


def compute_c1(f_values) -> float:
    pass


def run_autocorrelation(seed: int = 0, num_points: int = 400):
    """Stable evaluator entrypoint."""
    return search_function(seed=seed, num_points=num_points)


if __name__ == "__main__":
    f_values, c1 = run_autocorrelation()
    print(f"n_points={len(f_values)} c1={c1:.6f}")

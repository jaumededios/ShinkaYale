import math
# You may import additional standard libraries if needed
# such as numpy, scipy etc...

# EVOLVE-BLOCK-START

def search_algorithm(
    seed: int = 0, 
    initial_guess: tuple[float, float] = (0.0, 0.0),
    bounds: tuple[float, float] = (-5.0, 5.0),
):
    """
    Simplest possible baseline: return the initial guess.
    Your algorithm must be deterministic given the same seed and parameters.
    You may define new optional parameters if structurally relevant.
    """
    x, y = initial_guess
    return x, y, objective(x, y)


# EVOLVE-BLOCK-END

# The code outside of the evolve blocks is immutable scaffolding.

def objective(x: float, y: float) -> float:
    """Fixed two-variable objective used by the evaluator."""
    return float(math.sin(x) * math.cos(y) + math.sin(x * y) + (x**2 + y**2) / 20.0)


def run_search(
    seed: int = 0,
    iterations: int = 250,
    bounds: tuple[float, float] = (-5.0, 5.0),
):
    """Stable entrypoint used by the evaluator."""
    return search_algorithm(seed=seed, bounds=bounds)



# This lets you run "python initial.py" to test the code locally.
if __name__ == "__main__":
    x, y, value = run_search()
    print(f"x={x:.6f} y={y:.6f} value={value:.6f}")

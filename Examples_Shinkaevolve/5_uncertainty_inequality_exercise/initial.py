import numpy as np
from scipy.special import hermite


# EVOLVE-BLOCK-START

def search_coefficients(seed: int = 0, num_coeffs: int = 3, num_candidates: int = 250):
    """
    Write a construction that returns:
    - `coeffs`: coefficients for H_0, H_4, H_8, ...
    - `c4_bound`: the value r_max^2 / (2*pi)
    - `r_max`: the largest positive sign-changing root of P(x) / x^2

    A simple coefficient search is enough to get started: try a few small
    Hermite coefficient vectors, score them, and keep the best one.
    Preserve the return signature `(coeffs, c4_bound, r_max)`.
    """
    pass


# EVOLVE-BLOCK-END


def hermite_basis(num_coeffs: int):
    pass


def polynomial_coefficients(coeffs):
    pass


def numeric_c4(coeffs):
    pass


def run_uncertainty(seed: int = 0):
    """Stable evaluator entrypoint."""
    return search_coefficients(seed=seed)


if __name__ == "__main__":
    coeffs, c4, rmax = run_uncertainty()
    print(f"num_coeffs={len(coeffs)} c4={c4:.8f} r_max={rmax:.8f}")
    print(coeffs)

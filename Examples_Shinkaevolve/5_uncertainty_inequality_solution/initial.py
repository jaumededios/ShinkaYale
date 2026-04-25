import numpy as np
from scipy.special import hermite


# EVOLVE-BLOCK-START

def search_coefficients(seed: int = 0, num_coeffs: int = 3, num_candidates: int = 250):
    """
    Small baseline: sample Hermite coefficients, force P(0)=0, and keep the
    candidate with the smallest verified numerical C4 estimate.
    """
    rng = np.random.default_rng(seed)

    starting_points = [
        np.array([1.0, -0.01, -0.0001]),
        np.array([1.0, -0.02, 0.0001]),
        np.array([1.0, 0.0, 0.0]),
    ]

    best_coeffs = starting_points[0]
    best_c4, best_rmax = numeric_c4(best_coeffs)

    scales = 10.0 ** np.arange(num_coeffs)
    for candidate in starting_points[1:]:
        c4, rmax = numeric_c4(candidate)
        if np.isfinite(c4) and c4 < best_c4:
            best_coeffs, best_c4, best_rmax = candidate, c4, rmax

    for _ in range(num_candidates):
        coeffs = rng.normal(size=num_coeffs) / scales
        c4, rmax = numeric_c4(coeffs)
        if np.isfinite(c4) and c4 < best_c4:
            best_coeffs, best_c4, best_rmax = coeffs, c4, rmax

    return best_coeffs, best_c4, best_rmax


# EVOLVE-BLOCK-END


def hermite_basis(num_coeffs: int):
    degrees = [4 * k for k in range(num_coeffs + 1)]
    polynomials = [hermite(degree) for degree in degrees]
    max_degree = degrees[-1]

    basis = []
    values_at_zero = []
    for poly in polynomials:
        coeffs = np.zeros(max_degree + 1)
        coeffs[max_degree - poly.order :] = poly.coef
        basis.append(coeffs)
        values_at_zero.append(float(poly(0.0)))

    return np.asarray(basis), np.asarray(values_at_zero)


def polynomial_coefficients(coeffs):
    coeffs = np.asarray(coeffs, dtype=float)
    basis, values_at_zero = hermite_basis(len(coeffs))
    forced = -float(np.dot(coeffs, values_at_zero[:-1])) / values_at_zero[-1]

    all_coeffs = np.concatenate([coeffs, [forced]])
    poly = np.sum(all_coeffs[:, None] * basis, axis=0)
    if poly[0] < 0:
        poly = -poly
    return poly


def numeric_c4(coeffs):
    """Fast floating-point companion to the exact evaluator."""
    poly = polynomial_coefficients(coeffs)
    quotient = poly[:-2]

    roots = np.roots(quotient)
    real_roots = roots[np.isreal(roots)].real
    positive_roots = np.sort(real_roots[real_roots > 1e-8])
    if len(positive_roots) == 0:
        return float("inf"), float("inf")

    r_max = None
    for root in positive_roots:
        eps = 1e-6 * max(1.0, abs(root))
        if np.polyval(quotient, root - eps) * np.polyval(quotient, root + eps) < 0:
            r_max = float(root)

    if r_max is None:
        return float("inf"), float("inf")
    return float(r_max * r_max / (2.0 * np.pi)), r_max


def run_uncertainty(seed: int = 0):
    """Stable evaluator entrypoint."""
    return search_coefficients(seed=seed)


if __name__ == "__main__":
    coeffs, c4, rmax = run_uncertainty()
    print(f"num_coeffs={len(coeffs)} c4={c4:.8f} r_max={rmax:.8f}")
    print(coeffs)

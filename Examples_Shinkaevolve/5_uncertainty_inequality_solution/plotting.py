#!/usr/bin/env python3
import numpy as np
from scipy.special import hermite


def _polynomial_coefficients(coeffs):
    coeffs = np.asarray(coeffs, dtype=float)
    degrees = [4 * k for k in range(len(coeffs) + 1)]
    polynomials = [hermite(degree) for degree in degrees]
    max_degree = degrees[-1]

    basis = []
    values_at_zero = []
    for poly in polynomials:
        padded = np.zeros(max_degree + 1)
        padded[max_degree - poly.order :] = poly.coef
        basis.append(padded)
        values_at_zero.append(float(poly(0.0)))

    forced = -float(np.dot(coeffs, values_at_zero[:-1])) / values_at_zero[-1]
    all_coeffs = np.concatenate([coeffs, [forced]])
    poly = np.sum(all_coeffs[:, None] * np.asarray(basis), axis=0)
    if poly[0] < 0:
        poly = -poly
    return poly


def plot_uncertainty(extra_data):
    import matplotlib.pyplot as plt

    coeffs = np.asarray(extra_data["coeffs"], dtype=float)
    c4 = float(extra_data["c4_bound"])
    r_max = float(extra_data["r_max"])

    poly = _polynomial_coefficients(coeffs)
    xs = np.linspace(0.0, max(1.0, 1.15 * r_max), 800)
    ys = np.polyval(poly, xs)

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.axhline(0.0, color="black", linewidth=0.8)
    ax.axvline(r_max, color="tab:red", linestyle="--", label=f"r_max={r_max:.4f}")
    ax.plot(xs, ys, label=f"P(x), C4={c4:.6f}")
    ax.set_xlabel("x")
    ax.set_ylabel("P(x)")
    ax.legend()
    fig.tight_layout()

    return [(fig, "uncertainty_polynomial")]

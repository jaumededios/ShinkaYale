#!/usr/bin/env python3
import argparse
import os

import numpy as np
import sympy as sp

from plotting import plot_uncertainty
from shinka.core import run_shinka_eval


MAX_COEFFS = 6
X = sp.symbols("x")


def hermite_4k_polys(count: int):
    return [sp.polys.orthopolys.hermite_poly(4 * k, x=X, polys=False) for k in range(count)]


def construct_polynomial(coeffs) -> sp.Expr:
    """Build P from user coefficients and one extra coefficient forcing P(0)=0."""
    coeffs = np.asarray(coeffs, dtype=float)
    if coeffs.ndim != 1 or not (1 <= len(coeffs) <= MAX_COEFFS):
        raise ValueError(f"coeffs must be a 1D array with 1 to {MAX_COEFFS} entries.")
    if not np.all(np.isfinite(coeffs)):
        raise ValueError("coeffs contain non-finite values.")
    if np.max(np.abs(coeffs)) < 1e-14:
        raise ValueError("coeffs are all too close to zero.")

    hs = hermite_4k_polys(len(coeffs) + 1)
    partial = sum(sp.Rational(str(float(c))) * h for c, h in zip(coeffs, hs[:-1]))
    forced = -partial.subs(X, 0) / hs[-1].subs(X, 0)
    poly = sp.expand(partial + forced * hs[-1])

    # All degrees are multiples of 4, so the sign at infinity is well-defined.
    if sp.LC(sp.Poly(poly, X)) < 0:
        poly = -poly
    return sp.expand(poly)


def largest_positive_root(poly: sp.Expr) -> float:
    quotient, remainder = sp.div(poly, X**2, domain=sp.QQ)
    if remainder != 0:
        raise ValueError("P(x) is not divisible by x^2.")

    roots = sp.real_roots(quotient, X)
    best = None
    for root in roots:
        approx = root.eval_rational(n=120)
        if approx <= 0:
            continue
        eps = sp.Rational(1, 10**80)
        left = quotient.subs(X, approx - eps)
        right = quotient.subs(X, approx + eps)
        if left * right < 0 and (best is None or approx > best):
            best = approx

    if best is None:
        raise ValueError("No positive sign-changing root found for P(x)/x^2.")
    return float(best)


def compute_c4(coeffs) -> tuple[float, float]:
    poly = construct_polynomial(coeffs)
    r_max = largest_positive_root(poly)
    return float(r_max * r_max / (2.0 * np.pi)), float(r_max)


def validate_output(run_output, atol: float = 1e-8):
    try:
        coeffs, reported_c4, reported_rmax = run_output
    except (TypeError, ValueError):
        return False, "run_uncertainty must return (coeffs, c4_bound, r_max)."

    coeffs = np.asarray(coeffs, dtype=float)
    reported_c4 = float(reported_c4)
    reported_rmax = float(reported_rmax)

    if not (np.all(np.isfinite(coeffs)) and np.isfinite(reported_c4) and np.isfinite(reported_rmax)):
        return False, "Output contains non-finite values."

    try:
        c4, r_max = compute_c4(coeffs)
    except Exception as exc:
        return False, str(exc)

    if abs(c4 - reported_c4) > atol:
        return False, f"Reported C4 does not match recomputed value: {reported_c4:.12g} vs {c4:.12g}."
    if abs(r_max - reported_rmax) > atol:
        return False, f"Reported r_max does not match recomputed value: {reported_rmax:.12g} vs {r_max:.12g}."

    return True, None


def get_experiment_kwargs(run_index: int) -> dict:
    return {"seed": 0}


def aggregate_metrics(results) -> dict:
    if not results:
        return {"combined_score": 0.0}

    c4_values = [float(c4) for _, c4, _ in results]
    mean_c4 = sum(c4_values) / len(c4_values)
    best_coeffs, best_c4, best_rmax = min(results, key=lambda item: float(item[1]))

    return {
        "combined_score": 1.0 / max(mean_c4, 1e-12),
        "public": {
            "c4_bound": mean_c4,
            "r_max": float(best_rmax),
        },
        "private": {
            "best_c4_bound": float(best_c4),
        },
        "extra_data": {
            "coeffs": np.asarray(best_coeffs, dtype=float),
            "c4_bound": float(best_c4),
            "r_max": float(best_rmax),
        },
    }


def main(program_path: str, results_dir: str):
    os.makedirs(results_dir, exist_ok=True)

    metrics, correct, error_msg = run_shinka_eval(
        program_path=program_path,
        results_dir=results_dir,
        experiment_fn_name="run_uncertainty",
        num_runs=1,
        get_experiment_kwargs=get_experiment_kwargs,
        validate_fn=validate_output,
        aggregate_metrics_fn=aggregate_metrics,
        plotting_fn=plot_uncertainty,
    )

    print(f"Evaluated program: {program_path}")
    print(f"Results saved to: {results_dir}")
    print(f"Correct: {correct}")
    if error_msg:
        print(f"Error: {error_msg}")
    print(f"Combined score: {metrics.get('combined_score', 0.0):.6f}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate the uncertainty inequality example")
    parser.add_argument("--program_path", type=str, default="initial.py")
    parser.add_argument("--results_dir", type=str, default="results")
    args = parser.parse_args()
    main(args.program_path, args.results_dir)

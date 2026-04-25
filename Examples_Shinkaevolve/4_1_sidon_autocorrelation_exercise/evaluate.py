#!/usr/bin/env python3
import argparse
import os

import numpy as np

from plotting import plot_autocorrelation
from shinka.core import run_shinka_eval


# Old folkloric value attached to this problem (roughly the Schinzel-Schmidt
# era belief about the extremal function). Scoring above 1 means you have
# found an f that beats this value - i.e. you have numerically disproved
# the old conjecture. The best modern constructions (Matolcsi & Vinuesa,
# arXiv:0907.1379) reach around 1.5053, giving a score near pi / 3.0106.
BENCHMARK = float(np.pi / 2)


def compute_c1(f_values) -> float:
    f_values = np.asarray(f_values, dtype=float)
    dx = 0.5 / len(f_values)
    integral = float(np.sum(f_values) * dx)

    if abs(integral) < 1e-12:
        return float("inf")

    conv = np.convolve(f_values, f_values, mode="full") * dx
    return float(np.max(conv) / (integral**2))


def validate_output(run_output, atol: float = 1e-6):
    try:
        f_values, reported_c1 = run_output
    except (TypeError, ValueError):
        return False, "run_autocorrelation must return (f_values, c1)."

    f_values = np.asarray(f_values, dtype=float)
    reported_c1 = float(reported_c1)

    if f_values.ndim != 1 or len(f_values) == 0:
        return False, "f_values must be a non-empty 1D array."
    if not (np.all(np.isfinite(f_values)) and np.isfinite(reported_c1)):
        return False, "Output contains non-finite values."
    if np.any(f_values < -1e-8):
        return False, "f must be non-negative (negative values detected)."

    actual_c1 = compute_c1(np.maximum(f_values, 0.0))
    if not np.isfinite(actual_c1):
        return False, "The integral of f is too close to zero."
    if abs(actual_c1 - reported_c1) > atol:
        return False, "Reported C1 does not match the recomputed value."

    return True, None


def get_experiment_kwargs(run_index: int) -> dict:
    return {"seed": 0, "num_points": 400}


def aggregate_metrics(results) -> dict:
    if not results:
        return {"combined_score": 0.0}

    c1_values = [float(c1) for _, c1 in results]
    mean_c1 = sum(c1_values) / len(c1_values)
    best_values, best_c1 = min(results, key=lambda item: float(item[1]))

    return {
        "combined_score": BENCHMARK / mean_c1,
        "public": {
            "c1": mean_c1,
            "benchmark_ratio": BENCHMARK / mean_c1,
            "n_points": len(best_values),
        },
        "private": {
            "best_c1": float(best_c1),
        },
        "extra_data": {
            "f_values": np.asarray(best_values, dtype=float),
            "c1": float(best_c1),
        },
    }


def main(program_path: str, results_dir: str):
    os.makedirs(results_dir, exist_ok=True)

    metrics, correct, error_msg = run_shinka_eval(
        program_path=program_path,
        results_dir=results_dir,
        experiment_fn_name="run_autocorrelation",
        num_runs=1,
        get_experiment_kwargs=get_experiment_kwargs,
        validate_fn=validate_output,
        aggregate_metrics_fn=aggregate_metrics,
        plotting_fn=plot_autocorrelation,
    )

    print(f"Evaluated program: {program_path}")
    print(f"Results saved to: {results_dir}")
    print(f"Correct: {correct}")
    if error_msg:
        print(f"Error: {error_msg}")
    print(f"Combined score: {metrics.get('combined_score', 0.0):.6f}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate the Sidon autocorrelation example")
    parser.add_argument("--program_path", type=str, default="initial.py")
    parser.add_argument("--results_dir", type=str, default="results")
    args = parser.parse_args()
    main(args.program_path, args.results_dir)

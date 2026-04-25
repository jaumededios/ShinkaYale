#!/usr/bin/env python3
import argparse
import os

import numpy as np

from plotting import plot_autocorrelation
from shinka.core import run_shinka_eval


BENCHMARK = 1.4556427953745406


def compute_c3(f_values) -> float:
    f_values = np.asarray(f_values, dtype=float)
    dx = 0.5 / len(f_values)
    integral = float(np.sum(f_values) * dx)

    if abs(integral) < 1e-12:
        return float("inf")

    conv = np.convolve(f_values, f_values, mode="full") * dx
    return float(np.max(np.abs(conv)) / (integral**2))


def validate_output(run_output, atol: float = 1e-6):
    pass


def get_experiment_kwargs(run_index: int) -> dict:
    return {"seed": 0, "num_points": 400}


def aggregate_metrics(results) -> dict:
    if not results:
        return {"combined_score": 0.0}

    # do any computations you have to do
    extra_data = {
        # any other data you may want to save
    }

    return {
        "combined_score": None,  # Fill out with your score
        "public": {
            # any other information you may want to save
        },
        "private": {},
        "extra_data": extra_data,
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
    parser = argparse.ArgumentParser(description="Evaluate the third autocorrelation example")
    parser.add_argument("--program_path", type=str, default="initial.py")
    parser.add_argument("--results_dir", type=str, default="results")
    args = parser.parse_args()
    main(args.program_path, args.results_dir)

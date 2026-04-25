#!/usr/bin/env python3
import argparse
import itertools
import os

import numpy as np

from plotting import plot_heilbronn
from shinka.core import run_shinka_eval


BENCHMARK = 0.036529889880030156
NUM_POINTS = 11
SQRT3 = np.sqrt(3.0)
TRIANGLE_AREA = SQRT3 / 4.0


def check_inside_triangle(points, atol: float = 1e-6) -> bool:
    pass


def triangle_area(a, b, c) -> float:
    pass


def min_triangle_area_normalized(points) -> float:
    pass


def validate_output(run_output, atol: float = 1e-8):
    pass


def get_experiment_kwargs(run_index: int) -> dict:
    return {"seed": 0, "num_points": NUM_POINTS}


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
        experiment_fn_name="run_heilbronn",
        num_runs=1,
        get_experiment_kwargs=get_experiment_kwargs,
        validate_fn=validate_output,
        aggregate_metrics_fn=aggregate_metrics,
        plotting_fn=plot_heilbronn,
    )

    print(f"Evaluated program: {program_path}")
    print(f"Results saved to: {results_dir}")
    print(f"Correct: {correct}")
    if error_msg:
        print(f"Error: {error_msg}")
    print(f"Combined score: {metrics.get('combined_score', 0.0):.6f}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate the Heilbronn triangle example")
    parser.add_argument("--program_path", type=str, default="initial.py")
    parser.add_argument("--results_dir", type=str, default="results")
    args = parser.parse_args()
    main(args.program_path, args.results_dir)

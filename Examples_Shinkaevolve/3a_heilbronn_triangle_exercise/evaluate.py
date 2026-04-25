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
    x = points[:, 0]
    y = points[:, 1]
    return bool(
        np.all(y >= -atol)
        and np.all(SQRT3 * x <= SQRT3 - y + atol)
        and np.all(y <= SQRT3 * x + atol)
    )


def triangle_area(a, b, c) -> float:
    return float(abs(a[0] * (b[1] - c[1]) + b[0] * (c[1] - a[1]) + c[0] * (a[1] - b[1])) / 2.0)


def min_triangle_area_normalized(points) -> float:
    min_area = min(triangle_area(a, b, c) for a, b, c in itertools.combinations(points, 3))
    return float(min_area / TRIANGLE_AREA)


def validate_output(run_output, atol: float = 1e-8):
    try:
        points, reported_score = run_output
    except (TypeError, ValueError):
        return False, "run_heilbronn must return (points, min_area_normalized)."

    points = np.asarray(points, dtype=float)
    reported_score = float(reported_score)

    if points.shape != (NUM_POINTS, 2):
        return False, f"Expected points with shape ({NUM_POINTS}, 2), got {points.shape}."
    if not (np.all(np.isfinite(points)) and np.isfinite(reported_score)):
        return False, "Output contains non-finite values."
    if not check_inside_triangle(points):
        return False, "At least one point lies outside the triangle."

    actual_score = min_triangle_area_normalized(points)
    if abs(actual_score - reported_score) > atol:
        return False, "Reported normalized area does not match the geometry."

    return True, None


def get_experiment_kwargs(run_index: int) -> dict:
    return {"seed": 0, "num_points": NUM_POINTS}


def aggregate_metrics(results) -> dict:
    if not results:
        return {"combined_score": 0.0}

    scores = [float(score) for _, score in results]
    mean_score = sum(scores) / len(scores)
    best_points, best_score = max(results, key=lambda item: float(item[1]))

    return {
        "combined_score": mean_score / BENCHMARK,
        "public": {
            "min_area_normalized": mean_score,
            "benchmark_ratio": mean_score / BENCHMARK,
        },
        "private": {
            "best_min_area_normalized": float(best_score),
        },
        "extra_data": {
            "points": np.asarray(best_points, dtype=float),
            "min_area_normalized": float(best_score),
        },
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

#!/usr/bin/env python3
import argparse
import os

import numpy as np

from shinka.core import run_shinka_eval
from plotting import plot_packing


N_CIRCLES = 26


def validate_packing(run_output, atol: float = 1E-6) -> tuple[bool, str]:
    pass


def format_centers(centers) -> str:
    return "\n".join(
        f"  centers[{i}] = ({x:.4f}, {y:.4f})" for i, (x, y) in enumerate(centers)
    )


def get_experiment_kwargs(run_index: int) -> dict:
    return {"seed": run_index}


def aggregate_metrics(results, results_dir: str) -> dict:
    if not results:
        return {"combined_score": 0.0}

    
    # do any computations you have to do
    extra_data = {
        # any other data you may want to save
    }

    metrics = {
        "combined_score": None, #Fill out with your score
        "public": {
            #any other information you may want to save
        },
        "private": {},
        "extra_data": extra_data,
    }

    try:
        np.savez(
            os.path.join(results_dir, "extra.npz"),
            **extra_data,
        )
    except Exception as exc:
        metrics["extra_npz_save_error"] = str(exc)

    return metrics


def main(program_path: str, results_dir: str):
    os.makedirs(results_dir, exist_ok=True)

    metrics, correct, error_msg = run_shinka_eval(
        program_path=program_path,
        results_dir=results_dir,
        experiment_fn_name="run_packing",
        num_runs=1,
        get_experiment_kwargs=get_experiment_kwargs,
        validate_fn=validate_packing,
        aggregate_metrics_fn=lambda results: aggregate_metrics(results, results_dir),
        plotting_fn=plot_packing,
    )

    print(f"Evaluated program: {program_path}")
    print(f"Results saved to: {results_dir}")
    print(f"Correct: {correct}")
    if error_msg:
        print(f"Error: {error_msg}")
    print(f"Combined score: {metrics.get('combined_score', 0.0):.6f}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate the circle packing example")
    parser.add_argument("--program_path", type=str, default="initial.py")
    parser.add_argument("--results_dir", type=str, default="results")
    args = parser.parse_args()
    main(args.program_path, args.results_dir)

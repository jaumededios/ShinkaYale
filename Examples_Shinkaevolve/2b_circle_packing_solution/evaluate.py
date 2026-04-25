#!/usr/bin/env python3
import argparse
import os

import numpy as np

from shinka.core import run_shinka_eval
from plotting import plot_packing


N_CIRCLES = 26


def validate_packing(run_output, atol: float = 1E-6) -> tuple[bool, str]:
    try:
        centers, radii, reported_sum = run_output
    except (TypeError, ValueError):
        return False, "run_packing must return (centers, radii, reported_sum)."

    centers = np.asarray(centers, dtype=float)
    radii = np.asarray(radii, dtype=float)
    reported_sum = float(reported_sum)

    if centers.shape != (N_CIRCLES, 2) or radii.shape != (N_CIRCLES,):
        return False, f"Expected centers with shape ({N_CIRCLES}, 2) and radii with shape ({N_CIRCLES},), got {centers.shape} and {radii.shape}."
    if not (np.all(np.isfinite(centers)) and np.all(np.isfinite(radii)) and np.isfinite(reported_sum)):
        return False, "Packing contains non-finite values or negative radii."
    if np.any(radii < 0.0):
        return False, "Packing contains non-finite values or negative radii."
    if not np.isclose(np.sum(radii), reported_sum, atol=atol):
        return False, "Reported sum of radii does not match the actual sum."

    if np.any(centers[:, 0] - radii < -atol) or \
       np.any(centers[:, 0] + radii > 1.0 + atol) or \
       np.any(centers[:, 1] - radii < -atol) or \
       np.any(centers[:, 1] + radii > 1.0 + atol):
        return False, "Circles are outside the unit square."

    for i in range(len(centers)):
        for j in range(i + 1, len(centers)):
            distance = np.linalg.norm(centers[i] - centers[j])
            if distance < radii[i] + radii[j] - atol:
                return False, f"Circles {i} and {j} overlap."

    return True, "Valid packing."


def format_centers(centers) -> str:
    return "\n".join(
        f"  centers[{i}] = ({x:.4f}, {y:.4f})" for i, (x, y) in enumerate(centers)
    )


def get_experiment_kwargs(run_index: int) -> dict:
    return {"seed": run_index}


def aggregate_metrics(results, results_dir: str) -> dict:
    if not results:
        return {"combined_score": 0.0}

    centers, radii, reported_sum = results[0]
    centers = np.asarray(centers, dtype=float)
    radii = np.asarray(radii, dtype=float)
    reported_sum = float(reported_sum)
    extra_data = {
        "centers": centers,
        "radii": radii,
        "reported_sum": reported_sum,
    }

    metrics = {
        "combined_score": reported_sum,
        "public": {
            "num_circles": len(radii),
            "sum_radii": reported_sum,
            "centers_str": format_centers(centers),
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

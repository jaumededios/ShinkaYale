#!/usr/bin/env python3
import argparse
import math
import os

from shinka.core import run_shinka_eval


BOUNDS = (-5.0, 5.0)
SEEDS = [0, 1, 42] 

# This is a "fake" exercise, so we know the global minimum. 
GLOBAL_MIN_X = -1.704
GLOBAL_MIN_Y = 0.678
GLOBAL_MIN_VALUE = -1.519

# 1. Define the "Objective" function.

def objective(x: float, y: float) -> float:
    return float(math.sin(x) * math.cos(y) + math.sin(x * y) + (x**2 + y**2) / 20.0)




# 2. Check that a search result is valid.

def validate_search_result(run_output, atol: float = 1e-6):
    try:
        x, y, value = (float(v) for v in run_output)
    except (TypeError, ValueError):
        return False, "run_search must return (x, y, value)."

    if not all(math.isfinite(v) for v in (x, y, value)):
        return False, "run_search returned non-finite values."

    low, high = BOUNDS
    if not (low <= x <= high and low <= y <= high):
        return False, "Returned point is outside the search bounds."

    if abs(objective(x, y) - value) > atol:
        return False, "Reported value does not match the objective."

    return True, None





# 3. Build the success metric

def aggregate_search_metrics(results: list[tuple[float, float, float]]) -> dict:
    if not results:
        return {"combined_score": 0.0}

    xs = [float(x) for x, _, _ in results]
    ys = [float(y) for _, y, _ in results]
    values = [float(value) for _, _, value in results]

    # Score 1: How low does $f(x*, y*)$ get?
    mean_value = sum(values) / len(values)
    value_score = -mean_value  # ShinkaEvolve Maximizes!!

    # Score 2: How close are the returned points to the known minimum?
    mean_distance = sum(
        math.sqrt((x - GLOBAL_MIN_X) ** 2 + (y - GLOBAL_MIN_Y) ** 2)
        for x, y in zip(xs, ys)
    ) / len(results)
    distance_score = - mean_distance

    # Score 3: How reliably does the algorithm fail?
    reliability_score = len(results) / len(SEEDS)

    # Combine the scores with some weights, this is more art than science...
    combined_score = (
        value_score + 0.3 * distance_score + 0.3 * reliability_score
    )

    return {
        "combined_score": combined_score,
        "public": {
            "mean_value": mean_value,
            "mean_distance_to_known_minimum": mean_distance,
            "successful_runs": len(results),
        },
        "private": {
            "value_score": value_score,
            "distance_score": distance_score,
            "reliability_score": reliability_score,
        },
    }



def get_experiment_kwargs(run_index: int) -> dict:
    return {"seed": SEEDS[run_index], 
            "bounds": BOUNDS}


def main(program_path: str, results_dir: str):
    os.makedirs(results_dir, exist_ok=True)

    metrics, correct, error_msg = run_shinka_eval(
        program_path=program_path,
        results_dir=results_dir,
        experiment_fn_name="run_search",
        num_runs=len(SEEDS),
        run_workers=1,
        get_experiment_kwargs=get_experiment_kwargs,
        validate_fn=validate_search_result,
        aggregate_metrics_fn=aggregate_search_metrics,
    )

    print(f"Evaluated program: {program_path}")
    print(f"Results saved to: {results_dir}")
    print(f"Correct: {correct}")
    if error_msg:
        print(f"Error: {error_msg}")
    print(f"Combined score: {metrics.get('combined_score', 0.0):.6f}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Evaluate the minimal two-variable optimization example"
    )
    parser.add_argument("--program_path", type=str, default="initial.py")
    parser.add_argument("--results_dir", type=str, default="results")
    args = parser.parse_args()
    main(args.program_path, args.results_dir)

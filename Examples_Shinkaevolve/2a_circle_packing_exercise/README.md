# Circle Packing Exercise

## The problem

Place 26 disks inside the closed unit square `[0, 1]^2` so that no two disks
overlap, and **maximize the sum of their radii**.

$$
\max \; \sum_{i=1}^{26} r_i
\quad \text{subject to} \quad
\overline{D(c_i, r_i)} \subset [0, 1]^2,
\quad \| c_i - c_j \| \ge r_i + r_j \ \text{for } i \ne j,
\quad r_i \ge 0.
$$

Unlike the more familiar problem of packing equal disks, here the radii are
free and the objective is $\sum r_i$. There is no closed-form optimum for
general $n$; for $n = 26$ the current best-known value is around $2.635$.
The exercise is to produce a configuration, measure its score, and let
Shinka iterate on it.

## What you fill in

There are two small holes to plug before Shinka can run:

- In `initial.py`, write a `construct_packing()` that returns centers and
  radii for 26 admissible disks. Anything valid is fine to start with — a
  loose grid of tiny disks is enough to get the pipeline moving.
- In `evaluate.py`, write the `validate_packing()` check (does the
  configuration actually satisfy the three conditions above?) and set the
  score to $\sum r_i$ inside `aggregate_metrics()`.

The rest of the folder (`prompt.txt`, `shinka.yaml`, `run_evo.py`) is
scaffolding. You will write a short prompt describing the problem to the
LLM in `prompt.txt`, but you do not have to touch the launcher.

## Running it

From this folder:

```bash
python3 initial.py                                           # sanity check
python3 evaluate.py --program_path initial.py --results_dir smoke_test
python3 run_evo.py                                           # launch Shinka
```

## Notes

- Shinka only rewrites code between the `EVOLVE-BLOCK-START` /
  `EVOLVE-BLOCK-END` markers in `initial.py`. Helpers you want kept fixed
  should live outside that block.
- For a worked version with a reference construction, plotting, and larger
  run presets, see `../2b_circle_packing_solution`.

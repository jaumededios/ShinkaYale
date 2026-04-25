# Circle Packing — worked solution

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

This folder is the **worked solution** to the exercise in
`../2a_circle_packing_exercise`. The two small holes (the starter
construction and the validator) are filled in, and everything is ready to
run against Shinka straight away.

## Running it

From this folder:

```bash
python3 evaluate.py --program_path initial.py --results_dir smoke_test
python3 run_evo.py
python3 run_evo.py --config-fname shinka_medium.yaml
python3 run_evo.py --config-fname shinka_large.yaml
```

The default `shinka.yaml` is a small development run; `shinka_medium.yaml`
and `shinka_large.yaml` increase the budget (more generations, larger
populations) and give Shinka more room to refine the configuration.

## Extra remarks

- **The starter is a structured grid.** It uses four fixed rows with a
  small shared radius. The configuration is valid but loose on purpose —
  it leaves plenty of room for Shinka to propose richer layouts.
- **What tends to work.** In practice the best results come from mixing
  (i) a structured initial layout (rows, hexagonal-ish patterns, circles
  snapped to corners and edges), (ii) symmetry in the $x \leftrightarrow
  1 - x$ direction, and (iii) a numerical refinement step — typically a
  nonlinear program solved with `scipy.optimize` that relaxes the
  non-overlap and containment constraints into smooth penalties. The
  prompt in `prompt.txt` nudges the LLM in these directions.
- **Scoring.** The evaluator returns `combined_score = sum(radii)`, so
  the score reads directly as an absolute sum; you can compare it against
  the $\approx 2.635$ benchmark yourself.
- **Plotting.** `plotting.py` draws the final packing with indexed
  circles; the artifact lands in `results/plots/`.
- **For the plain problem statement only,** see
  `../2a_circle_packing_exercise`.

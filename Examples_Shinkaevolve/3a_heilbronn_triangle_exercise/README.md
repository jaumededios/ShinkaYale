# Heilbronn Triangle Exercise

## The problem

Given $n$ points in a convex region $\Omega$, every triple determines a
triangle, so there are $\binom{n}{3}$ triangles in total. The **Heilbronn
problem** asks:

$$
H(n) \; = \; \sup_{\{p_1, \dots, p_n\} \subset \Omega}
\; \min_{1 \le i < j < k \le n} \mathrm{area}\bigl(\triangle p_i p_j p_k\bigr).
$$

That is, place the points so that **the smallest of all these triangles is
as large as possible**. The quantity $H(n)$ is usually normalised by
$\mathrm{area}(\Omega)$ so it is independent of the shape's scale.

In this exercise $\Omega$ is the equilateral triangle with vertices
$(0, 0)$, $(1, 0)$, and $\bigl(\tfrac{1}{2}, \tfrac{\sqrt{3}}{2}\bigr)$ (so
$\mathrm{area}(\Omega) = \tfrac{\sqrt{3}}{4}$), and $n = 11$.

The score reported back to Shinka is the **normalised** minimum triangle
area

$$
\frac{\min_{i<j<k} \mathrm{area}(\triangle p_i p_j p_k)}{\mathrm{area}(\Omega)},
$$

and we are trying to **maximise** it. The current best-known value for
$n = 11$ in the equilateral triangle is roughly $0.0365$ — the evaluator
reports your score as a ratio against this benchmark.

## What you fill in

- In `initial.py`, write `search_points()` so it returns 11 points inside
  the triangle together with the corresponding normalised minimum triangle
  area. Any valid construction is acceptable as a starting point; a small
  random search or a simple symmetric hand-built layout is enough to get
  the pipeline moving. The helper `sample_points_in_triangle()` is
  provided, but the area / scoring helpers are left for you to fill in.
- In `evaluate.py`, fill in the geometry helpers
  (`check_inside_triangle()`, `triangle_area()`,
  `min_triangle_area_normalized()`), then write `validate_output()` so it
  checks the returned points really lie inside the triangle and the
  reported score matches the geometry. Finally, fill in
  `aggregate_metrics()` so the score reported back to Shinka is the
  benchmark ratio.
- Write a short prompt in `prompt.txt` describing the problem to the LLM
  and any ideas you want it to try (symmetry, boundary placements, jittered
  lattices, gradient-style refinement, and so on).

Only the basic constants, sampling scaffold, and plotting code are
provided. `plotting.py` will draw the configuration with the critical
smallest triangle highlighted once the evaluator is wired up.

## Running it

From this folder, after you fill in `search_points()`, the holes in
`evaluate.py`, and `prompt.txt`:

```bash
python3 initial.py                                           # sanity check
python3 evaluate.py --program_path initial.py --results_dir smoke_test
python3 run_evo.py                                           # launch Shinka
```

## Notes

- Shinka only rewrites code inside the `EVOLVE-BLOCK-START` /
  `EVOLVE-BLOCK-END` markers in `initial.py`.
- Points are accepted if they lie on or inside the triangle (with a small
  numerical tolerance). The reported score must agree with the score
  recomputed from the points.

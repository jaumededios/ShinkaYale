# Heilbronn Triangle — worked solution

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

In this example $\Omega$ is the equilateral triangle with vertices
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

This folder is the **worked solution** to the exercise in
`../3a_heilbronn_triangle_exercise`.

## Running it

From this folder:

```bash
python3 evaluate.py --program_path initial.py --results_dir smoke_test
python3 run_evo.py
```

## Extra remarks

- **The starter is a seeded random search.** `search_points()` draws
  several hundred uniform random configurations inside the triangle and
  keeps the one with the largest minimum triangle area. This is a valid,
  non-trivial baseline — a random-search lower bound that Shinka then
  tries to improve on.
- **What tends to work.** The best Heilbronn constructions exploit
  symmetries of the triangle (the $120^\circ$ rotation and reflections),
  push a few points onto the boundary to "use" the area efficiently, and
  then polish the configuration with a continuous optimiser. Formulating
  the min-area objective as a smooth proxy (e.g. a soft-min or
  log-sum-exp over triangle areas) makes the refinement step
  differentiable. The prompt in `prompt.txt` steers the LLM towards these
  ideas.
- **Plotting.** `plotting.py` highlights the critical smallest triangle
  in solid red and every triangle within $5\%$ of that area in
  translucent red. Seeing a cluster of near-minimal triangles usually
  means you are close to a local optimum — at the true optimum, many
  triangles are tied for smallest. The artifact is saved under
  `results/plots/`.
- **Scoring.** `combined_score = normalised_min_area / benchmark`, so a
  score of $1$ means you matched the best-known value.
- **For the plain problem statement only,** see
  `../3a_heilbronn_triangle_exercise`.

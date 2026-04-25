# 5 &mdash; An uncertainty inequality

This is the Shinka port of AlphaEvolve's Appendix B.4 "An uncertainty
inequality". Like problem 4.1, it is a problem about **real-valued
functions on the line**, and our strategy is to reduce it to a
finite-dimensional numerical search by picking a Gaussian-times-
polynomial Ansatz that diagonalises the Fourier transform.

## The continuous problem

For a function $f: \mathbb{R} \to \mathbb{R}$, let
$\hat f(\xi) := \int_{\mathbb{R}} f(x)\, e^{-2\pi i x\xi}\, dx$ be its
Fourier transform, and define the *positivity radius*

$$
A(f) \; := \; \inf \bigl\{\, r > 0 \;:\; f(x) \ge 0 \text{ for all } |x| \ge r \,\bigr\}.
$$

The **uncertainty constant $C_4$** is the largest constant such that

$$
A(f) \cdot A(\hat f) \; \ge \; C_4
$$

for every even $f$ with $\max\bigl(f(0), \hat f(0)\bigr) < 0$. In words:
if both $f$ and $\hat f$ are negative at the origin, they cannot both
become positive too early — the product of their "positivity radii" is
bounded below.

The best known bounds (Gonçalves–Oliveira–Steinerberger 2017) are

$$
0.2025 \;\le\; C_4 \;\le\; 0.3523,
$$

and AlphaEvolve tightened the upper bound to $C_4 \le 0.3521$ using the
Hermite Ansatz described below, and further to $C_4 \le 0.3216$ using a
different (Laguerre-based, Cohn–Gonçalves 2019) Ansatz. The true value
of $C_4$ is open.

## Discretising: the Fourier-self-dual Hermite Ansatz

Searching over all Schwartz $f$ is impossible, so we restrict to test
functions of the form

$$
f(x) \; = \; P\!\left(\sqrt{2\pi}\, x\right) e^{-\pi x^2},
$$

where $P$ is an even polynomial. The Gaussian $e^{-\pi x^2}$ is the
unique fixed point of the Fourier transform $\hat f(\xi) = \int f(x)\,
e^{-2\pi i x\xi}\, dx$, and the rescaling by $\sqrt{2\pi}$ is exactly
what makes the Hermite functions

$$
h_n(x) \; = \; H_n\!\left(\sqrt{2\pi}\, x\right) e^{-\pi x^2}
$$

into eigenfunctions of this Fourier transform with eigenvalue $(-i)^n$.
For $n = 4k$ the eigenvalue is $+1$, so the subspace

$$
P(x) \;=\; \sum_{k=0}^{m} c_k\, H_{4k}(x)
\qquad \Longrightarrow \qquad
f \;=\; \hat f
$$

consists entirely of **Fourier-self-dual** functions. On this subspace,
$\hat f = f$, so $A(f) = A(\hat f)$ and the constraint
$A(f) \cdot A(\hat f) \ge C_4$ collapses to $A(f)^2 \ge C_4$. We also
need $f(0) < 0$; the evaluator simplifies this by forcing $P(0) = 0$
(double zero at the origin, since $P$ is even) and choosing signs so
that $f < 0$ on a neighbourhood of the origin and $f > 0$ at infinity.

The last piece: the root $r_{\max}$ of $P(x)/x^2$ (the largest positive
sign-changing root) lives in the **Hermite coordinate**, not in
physical $x$. Translating back through the $\sqrt{2\pi}$ rescaling gives
$A(f) = r_{\max}/\sqrt{2\pi}$, hence

$$
C_4 \;\le\; A(f)^2 \;=\; \frac{r_{\max}^2}{2\pi}.
$$

That is the formula the evaluator scores on.

## What you fill in

`initial.py` contains `search_coefficients()`, which returns
`(coeffs, c4_bound, r_max)`. The baseline is a very simple random
search around a few hand-picked starting points; it scores well below
even the 1970s-era bounds. Your job (with Shinka's help) is to find
structured coefficient choices — with gradient-style local refinement,
targeted parameterisations, etc. — that push $C_4$ towards the
AlphaEvolve Hermite ceiling $\approx 0.3521$.

`evaluate.py` rebuilds $P$ with SymPy's exact rational arithmetic,
recomputes $r_{\max}$ by certified sign changes, and rejects any
mismatch between reported and recomputed values. `plotting.py` draws
$P$ together with its largest positive root.

## Running it

From this folder:

```bash
python3 initial.py                                           # sanity check
python3 evaluate.py --program_path initial.py --results_dir smoke_test
python3 run_evo.py                                           # launch Shinka
```

## Extra remarks

- **The benchmark and what it means.** The evaluator currently uses
  $0.3215872333529007$, which is AlphaEvolve's improved bound from the
  *Laguerre / Cohn–Gonçalves* formulation (a different basis than the
  one used here). With the Hermite formulation actually implemented in
  `initial.py`, the ceiling is $\approx 0.3521$ (AlphaEvolve) or
  $\approx 0.3523$ (Gonçalves–Oliveira–Steinerberger 2017), so scores
  above $\approx 0.913$ are *not* reachable without changing the
  Ansatz. Think of this benchmark as a stretch target from a richer
  parameterisation, not as "score 1.0 is the goal of this search". If
  you want scores centred around 1.0 inside the Hermite regime,
  replace the benchmark with $0.3521$ or $0.3523$.

- **Cap on coefficients.** The evaluator accepts at most 6 user
  coefficients (`MAX_COEFFS = 6`), so the Hermite degree involved is at
  most $24$. The AlphaEvolve Hermite result uses only 3 coefficients
  (i.e. $H_0, H_4, H_8, H_{12}$), so the cap is generous.

- **Coefficient magnitudes.** $H_{4k}(0)$ grows fast ($H_{12}(0) =
  665{,}280$), so the $c_k$ that matter are extremely small for large
  $k$. The starter uses `rng.normal() / 10**k` to keep proposals in a
  sensible range. For reference, the AlphaEvolve Hermite-regime result
  uses $(c_0, c_1, c_2) \approx (0.329,\ -0.0116,\ -8.92 \times
  10^{-5})$.

- **Why the double zero at the origin.** $P$ is even, so any zero at
  $x = 0$ has even multiplicity. Forcing $P(0) = 0$ therefore forces a
  *double* zero, which is why the evaluator divides by $x^2$ before
  looking for the largest positive sign change. The condition
  $f(0) < 0$ in the problem statement is encoded by this double zero
  together with the sign-normalisation at infinity.

- The plot artifact is saved under `results/plots/`.

# 5 &mdash; An uncertainty inequality (exercise)

Like the previous problems, we have a question about **real-valued
functions on the line** and we want to reduce it to a finite-dimensional
numerical search by picking the right Ansatz.

## The continuous problem

For $f: \mathbb{R} \to \mathbb{R}$, let $\hat f(\xi) :=
\int_{\mathbb{R}} f(x)\, e^{-2\pi i x\xi}\, dx$ and define the
*positivity radius*

$$
A(f) \; := \; \inf \bigl\{\, r > 0 \;:\; f(x) \ge 0 \text{ for all } |x| \ge r \,\bigr\}.
$$

The uncertainty constant $C_4$ is the largest constant such that

$$
A(f) \cdot A(\hat f) \;\ge\; C_4
$$

for every even $f$ with $\max\bigl(f(0), \hat f(0)\bigr) < 0$. In words:
if both $f$ and $\hat f$ are negative at the origin, they cannot both
become non-negative too early — the product of the two positivity radii
is bounded below by a universal constant.

Any explicit choice of $f$ gives an upper bound on $C_4$, namely
$C_4 \le A(f) \cdot A(\hat f)$, and smaller is better.

## Discretising: Fourier-self-dual Hermite Ansatz

We restrict to test functions of the form

$$
f(x) \; = \; P\!\left(\sqrt{2\pi}\, x\right) e^{-\pi x^2},
$$

where $P$ is an even polynomial. The Gaussian $e^{-\pi x^2}$ is the
fixed point of the Fourier transform (with the convention $\hat f(\xi) =
\int f(x)\, e^{-2\pi i x\xi}\, dx$), and the rescaling by $\sqrt{2\pi}$
makes each Hermite function

$$
H_n\!\left(\sqrt{2\pi}\, x\right) e^{-\pi x^2}
$$

an eigenfunction of the Fourier transform with eigenvalue $(-i)^n$.
Restricting $P$ to be a linear combination of $H_{4k}$ therefore picks
out a **Fourier-self-dual** subspace: on it, $\hat f = f$, so
$A(f) = A(\hat f)$ and the constraint $A(f) \cdot A(\hat f) \ge C_4$
simplifies to $A(f)^2 \ge C_4$.

So the Ansatz is

$$
P(x) \;=\; \sum_{k=0}^{m} c_k\, H_{4k}(x),
$$

with the two conditions:

- $P(0) = 0$ (since $P$ is even, this forces a *double* zero at the
  origin; the evaluator solves for the last $c_m$ automatically so you
  only supply $c_0, \dots, c_{m-1}$).
- The leading coefficient is positive (sign-normalised, done for you).

Let $r_{\max}$ be the largest positive sign-changing root of $P(x)/x^2$
in the Hermite coordinate. Translating back through the $\sqrt{2\pi}$
rescaling gives $A(f) = r_{\max}/\sqrt{2\pi}$, and hence

$$
C_4 \;\le\; A(f)^2 \;=\; \frac{r_{\max}^2}{2\pi}.
$$

That is the quantity the evaluator scores on. **Smaller is better.**

## What you fill in

- `initial.py`: write `search_coefficients()` so it returns a tuple
  `(coeffs, c4_bound, r_max)`. The starter returns the trivial vector
  $(1, 0, 0)$, which is valid but weak. You are free to change the
  number of coefficients (up to 6), the search strategy, and the
  starting points — the evaluator only cares about the returned tuple.
- `prompt.txt`: describe the problem, the Ansatz, and any search
  strategies you want the LLM to try (structured coefficient templates,
  random restarts, gradient-style local refinement, etc.).

`evaluate.py` and `plotting.py` are already in place. The evaluator
rebuilds $P$ using SymPy's exact rational arithmetic, recomputes
$r_{\max}$ by certified sign changes, and rejects any mismatch between
your reported $(c_4, r_{\max})$ and the recomputed ones — so the number
you return has to be correct.

## Running it

From this folder:

```bash
python3 initial.py                                           # sanity check
python3 evaluate.py --program_path initial.py --results_dir smoke_test
python3 run_evo.py                                           # launch Shinka
```

## Notes

- Shinka only rewrites code inside the `EVOLVE-BLOCK-START` /
  `EVOLVE-BLOCK-END` markers in `initial.py`.
- The evaluator caps the number of user coefficients at $6$
  (`MAX_COEFFS = 6`), giving a Hermite degree of at most $24$. This is
  a purely practical cap — SymPy's exact root-finding gets slow above
  it.
- $H_{4k}(0)$ grows fast ($H_{12}(0) = 665{,}280$), so meaningful $c_k$
  values shrink sharply with $k$. Scale-aware random search matters.
- For a worked version, see `../5_uncertainty_inequality_solution`.

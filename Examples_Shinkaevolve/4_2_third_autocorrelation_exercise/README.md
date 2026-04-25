# 4.2 &mdash; Third Autocorrelation Inequality Exercise

## The problem

For a real-valued integrable function $f$ supported on an interval of
length $\tfrac{1}{2}$, the **autoconvolution** is

$$
(f * f)(t) \; = \; \int f(x)\, f(t - x)\, dx,
$$

which is itself supported on an interval of length $1$. The *third
autocorrelation constant* is the sharp constant

$$
\min_{f \not\equiv 0} \; \frac{\|f * f\|_{\infty}}{\|f\|_2^2},
$$

where the minimum ranges over integrable functions on an interval of
width $\tfrac{1}{2}$. Pinning down this constant (and the analogous
constants for higher autoconvolutions) goes back to Schur and has been
refined by Martin, O'Bryant, Matolcsi, Vinuesa, and others. The best
known upper bound at the time of writing is about $1.4557$, and the true
value of the infimum is open.

**Our task** is to construct an $f$ that makes the ratio above **as small
as possible**. Note that $f$ is allowed to take negative values — in fact
constructions that take both signs usually do better, because
cancellations in $f * f$ can shrink $\|f * f\|_\infty$ faster than they
shrink the denominator. The problem is dilation-invariant in $x$, so the
specific width $\tfrac{1}{2}$ is just a convenient normalisation.

## Discretisation

We cannot let an LLM search over arbitrary integrable functions, so we
discretise: fix an integer $N$, split the interval into $N$ equal bins of
width $\delta = \tfrac{1}{2N}$, and take $f$ to be **piecewise constant**
on each bin $[n\delta, (n+1)\delta)$. Once that is done every integral
becomes a sum: $f$ is represented by a vector
$(f_1, \dots, f_N) \in \mathbb{R}^N$, and the autoconvolution becomes the
familiar discrete convolution
$(f * f)_k = \delta \sum_i f_i f_{k-i}$. The value of the ratio does not
depend on $\delta$, so $N$ just controls how fine a function you can
represent. The starter uses $N = 400$.

## What you fill in

`initial.py` contains a `search_function()` that returns a vector
$(f_1, \dots, f_N)$ together with its ratio. The baseline is a simple
random search over sign patterns: it occasionally finds something
non-trivial but is easily beaten. Your job (with Shinka's help) is to
find constructions — analytic, structured, or refined numerically — that
push the ratio below the baseline and towards the best-known value.

Write a short prompt in `prompt.txt` describing the mathematical problem,
the output contract, and whatever ideas you want the LLM to try.

`evaluate.py` recomputes the ratio from the returned vector and rejects
any mismatch, so you do not have to worry about gaming the score.
`plotting.py` visualises the step function and its autoconvolution.

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
- The evaluator returns the ratio `benchmark / your_ratio`, so larger is
  better; a score of $1$ means you matched the best-known construction.
- The plot is saved under `results/plots/`.
